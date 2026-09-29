"""
debug. Menu debug tersembunyi [9] -- pemberi gems/coins/material/pity instan.

force_next disimpan ke save, jadi sisa paksaan bisa bocor ke sesi berikutnya.
"""

import os

from .account import save_path, save_state
from .config import HARD_PITY_SSR, MAX_LEVEL, MAX_RANK
from .data import T, CHARACTERS, STAGES
from .state import normalize_state
from .ui import ask, ask_key, header, is_yes

# ----------------------------------------------------------------------------
# DEBUG MENU
# ----------------------------------------------------------------------------
def debug_menu(st):
    while True:
        header(T("debug_title"), st)
        print(T("d_force", st["force_next"]))
        print(T("d1"))
        print(T("d2"))
        print(T("d3"))
        print(T("d4"))
        print(T("d5"))
        print(T("d6"))
        print(T("d7"))
        print(T("d8"))
        print(T("d9"))
        print(T("dA"))
        print(T("dB"))
        print(T("dC"))
        print(T("dD"))
        print(T("back"))
        c = ask_key(set("0123456789abABcdCD"))
        if c == "0":
            return
        elif c == "1":
            st["gems"] += 1600
            print(T("d_ok_gems", st["gems"]))
        elif c == "2":
            st["coins"] += 5000
            print(T("d_ok_coins", st["coins"]))
        elif c == "3":
            st["force_next"] = "SSR"
            print(T("d_ok_force", "SSR"))
        elif c == "4":
            st["force_next"] = "SR"
            print(T("d_ok_force", "SR"))
        elif c == "5":
            st["pity"] = HARD_PITY_SSR - 1
            print(T("d_ok_pity", st["pity"]))
        elif c == "6":
            st["cleared"] = [s["id"] for s in STAGES[:-1]]
            print(T("d_ok_clear", STAGES[-1]["id"] - 1))
        elif c == "7":
            st["cleared"] = []
            print(T("d_ok_reset"))
        elif c == "8":
            # Hanya rank. Level adalah sumbu terpisah yang datang dari
            # material; menimpa entri lama ke lvl 1 menghapus upgrade pemain.
            for ch in CHARACTERS:
                ent = st["owned"].setdefault(ch["id"], {"rank": 1, "lvl": 1})
                ent["rank"] = MAX_RANK
            if st["active"] is None:
                st["active"] = CHARACTERS[0]["id"]
            print(T("d_ok_rank"))
        elif c == "9":
            acct = st.get("account")
            if is_yes(ask(T("reset_q", T("yes_word")))):
                p = save_path(acct)
                st.clear()
                st.update(normalize_state({}, acct))
                if os.path.exists(p):
                    os.remove(p)
                print(T("reset_done"))
        elif c == "a" or c == "A":
            for ch in CHARACTERS:
                st["mats"][ch["id"]] = st["mats"].get(ch["id"], 0) + 999
            print(T("d_ok_mats"))
        elif c == "b" or c == "B":
            for ch in CHARACTERS:
                st["owned"].setdefault(ch["id"], {"rank": 1, "lvl": 1})
                st["owned"][ch["id"]]["lvl"] = MAX_LEVEL
            print(T("d_ok_level"))
        elif c == "c" or c == "C":
            st["tickets"] += 20
            print(T("d_ok_tiket", st["tickets"]))
        elif c == "d" or c == "D":
            # Sumber gift sementara biar flow Gift -> Affection bisa ditest.
            # Sumber ekonomi (shop/reward) masih TBD, lihat AGENTS.md.
            st["gifts"] = st.get("gifts", 0) + 10
            print(T("d_ok_gift", st["gifts"]))
        save_state(st)
