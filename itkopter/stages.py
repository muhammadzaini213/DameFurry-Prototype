"""
stages. Daftar stage, unlock berurutan, dan layar hasil.

hadiah + material drop + unlock Main Story dicek di show_result().
"""

from .account import save_state
from .config import LOSE_COINS
from .data import (T, CHAR_BY_ID, MAIN_STORY, STAGES, chapter_title, mat_name,
                   diff_of, stage_name)
from .gameplay import run_gameplay
from .ui import ask_pick, header, pause

def stage_menu(st):
    while True:
        header(T("stage_title"), st)
        if st["active"] is None:
            print(T("no_active"))
            pause()
            return
        print(T("unit_line", CHAR_BY_ID[st["active"]]["name"]))
        unlocked = []
        for s in STAGES:
            is_open = s["id"] == 1 or (s["id"] - 1) in st["cleared"]
            done = "CLEAR" if s["id"] in st["cleared"] else "     "
            lock = T("locked") if not is_open else ""
            nm = stage_name(s)
            print(f" [{s['id']}] {nm:<24} {diff_of(s):<7} {done} {lock}")
            # Drop dicetak di daftar stage (bukan cuma setelah menang) biar
            # pemain tahu stage mana yang harus di-grind buat material tertentu.
            drops = s.get("drops", {})
            if drops:
                parts = [f"{mat_name(cid)} x{amt}"
                         + ("" if cid in st["owned"] else T("drop_unowned"))
                         for cid, amt in drops.items()]
                print(T("stage_drops", ", ".join(parts)))
            if is_open:
                unlocked.append(s["id"])
        print(T("back"))
        n = ask_pick("> ", 0, len(STAGES))
        if n == 0:
            return
        if n not in unlocked:
            print(T("stage_locked"))
            pause()
            continue
        stage = STAGES[n - 1]
        result = run_gameplay(stage, st["active"])
        if result is None:
            continue
        show_result(st, stage, result)


def show_result(st, stage, win):
    header(T("result_title"))
    if win:
        first = stage["id"] not in st["cleared"]
        gems = stage["gems"] + (stage["first_bonus"] if first else 0)
        coins = stage["coins"]
        st["gems"] += gems
        st["coins"] += coins
        st["wins"] += 1
        if first:
            st["cleared"].append(stage["id"])
        print(T("mission_ok"))
        print(T("reward", gems, coins))
        if first:
            print(T("first_bonus", stage["first_bonus"]))
            if stage["id"] < len(STAGES):
                print(T("next_open", stage["id"] + 1))
            else:
                print(T("all_done"))
        drops = grant_drops(st, stage)
        if drops:
            print(T("mat_drop"))
            for cid, n in drops:
                # Drop memang diberikan walau karakternya belum dimiliki; ini
                # cuma penanda di layar supaya tidak disangka sudah kepakai.
                mark = "" if cid in st["owned"] else T("drop_unowned")
                print(f"   {mat_name(cid)} +{n}{mark}")
        else:
            print(T("mat_drop_none"))
        # Cek unlock MAIN STORY (stage-based) di momen first-clear stage ini.
        if first:
            for ch in MAIN_STORY:
                if ch["unlock_stage"] == stage["id"]:
                    print(T("ms_unlocked", ch["id"], chapter_title(ch)))
        # Jangan berhenti di layar reward: kasih arah ke progression berikutnya.
        print()
        if drops:
            print(T("hint_after_reward"))
        print(T("hint_after_reward2"))
    else:
        st["coins"] += LOSE_COINS
        st["losses"] += 1
        print(T("mission_fail"))
        print(T("lose_cons", LOSE_COINS))
    save_state(st)
    pause()


def grant_drops(st, stage):
    """Tambah material hasil clear stage. Return list [(id, jumlah)]."""
    gained = []
    for cid, n in stage.get("drops", {}).items():
        if cid not in CHAR_BY_ID:
            continue
        st["mats"][cid] = st["mats"].get(cid, 0) + n
        gained.append((cid, n))
    return gained
