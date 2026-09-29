"""
gacha. Pull, pity, guarantee 10x, dan dupe -> rank.

Satu-satunya tempat yang boleh mengubah pity / total_pulls / rank.
"""

import random

from .account import save_state
from .character import collection_menu, fmt_char
from .config import (DUPE_COIN_REFUND, GEM_PER_PULL, HARD_PITY_SSR, MAX_RANK,
                     RATES, RARITY_ORDER, RARITY_STAR, TENPULL_GUARANTEE)
from .data import T, CHARACTERS, species_of
from .ui import ask, ask_key, header, is_yes, pause

# ----------------------------------------------------------------------------
# GACHA
# ----------------------------------------------------------------------------
def roll_rarity(st, min_rarity=None):
    """Tentukan rarity satu pull, termasuk pity & debug force."""
    if st["force_next"]:
        r = st["force_next"]
        st["force_next"] = None
        return r
    if st["pity"] + 1 >= HARD_PITY_SSR:
        return "SSR"
    x = random.random()
    acc = 0.0
    result = "R"
    for rar in ("SSR", "SR", "R"):
        acc += RATES[rar]
        if x < acc:
            result = rar
            break
    if min_rarity and RARITY_ORDER[result] > RARITY_ORDER[min_rarity]:
        result = min_rarity
    return result


def do_pull(st, min_rarity=None):
    rar = roll_rarity(st, min_rarity)
    pool = [c for c in CHARACTERS if c["rarity"] == rar]
    char = random.choice(pool)

    st["total_pulls"] += 1
    st["pity"] = 0 if rar == "SSR" else st["pity"] + 1

    cid = char["id"]
    if cid not in st["owned"]:
        st["owned"][cid] = {"rank": 1, "lvl": 1}
        note = T("new")
    elif st["owned"][cid]["rank"] < MAX_RANK:
        st["owned"][cid]["rank"] += 1
        note = T("dupe_rank", st["owned"][cid]["rank"])
    else:
        refund = DUPE_COIN_REFUND[rar]
        st["coins"] += refund
        note = T("refund_max", refund)
    if st["active"] is None:
        st["active"] = cid
    return char, note


def run_pulls(st, n):
    """Jalankan n pull ke st. Return list (char, note)."""
    results = []
    for i in range(n):
        # slot terakhir 10x pull dijamin SR+ kalau belum ada SR+
        need_guar = (n == 10 and i == 9 and
                     not any(RARITY_ORDER[r[0]["rarity"]] <= RARITY_ORDER[TENPULL_GUARANTEE]
                             for r in results))
        results.append(do_pull(st, TENPULL_GUARANTEE if need_guar else None))
    return results


def print_results(results):
    print(T("pull_results"))
    for char, note in results:
        print(" " + T("fmt_char", RARITY_STAR[char["rarity"]], char["rarity"],
                      char["name"], char["object"], species_of(char), char["role"])
              + f"  <{note}>")


def pay_and_pull(st, n):
    """
    Tanya metode bayar (gems atau tiket), tarik, cetak hasil.
    Return True kalau pull terjadi, False kalau dibatalkan / dana kurang.
    """
    cost_gems = GEM_PER_PULL * n
    print(T("pay_what", n))
    print(T("pay_gems", cost_gems, st["gems"]))
    print(T("pay_tiket", n, st["tickets"]))
    print(T("cancel"))
    pay = ask(" > ")
    if pay == "1":
        if st["gems"] < cost_gems:
            print(T("gems_short", cost_gems, st["gems"]))
            pause()
            return False
        st["gems"] -= cost_gems
    elif pay == "2":
        if st["tickets"] < n:
            print(T("tiket_short", n, st["tickets"]))
            pause()
            return False
        st["tickets"] -= n
    else:
        return False
    before = set(st["owned"])
    print_results(run_pulls(st, n))
    save_state(st)
    pause()
    # Lanjutan flow: kalau barusan dapat karakter baru, jangan berhenti di menu
    # gacha -- tawarkan langsung buka Koleksi buat lihat/pilih unit.
    if set(st["owned"]) - before:
        if is_yes(ask(T("gacha_open_coll", T("yes_word")))):
            collection_menu(st)
    return True


def gacha_menu(st):
    while True:
        header(T("gacha_title"), st)
        print(T("gacha_pity", st["pity"], HARD_PITY_SSR, st["total_pulls"]))
        print(T("gacha_rate", RATES["SSR"] * 100, RATES["SR"] * 100,
                RATES["R"] * 100))
        print(T("gacha_tickets", st["tickets"]))
        print()
        print(T("pull_x1", GEM_PER_PULL))
        print(T("pull_x10", GEM_PER_PULL * 10, TENPULL_GUARANTEE))
        print(T("see_rates"))
        print(T("back"))
        # Dulu input salah di menu gacha dicetak ulang layar tanpa pesan apa
        # pun; sekarang keluar [!] lalu ditanya ulang di layar yang sama.
        c = ask_key({"0", "1", "2", "3"})
        if c == "0":
            return
        elif c in ("1", "2"):
            pay_and_pull(st, 1 if c == "1" else 10)
        elif c == "3":
            header(T("list_title"))
            for rar in ("SSR", "SR", "R"):
                for ch in CHARACTERS:
                    if ch["rarity"] == rar:
                        mark = "✓" if ch["id"] in st["owned"] else " "
                        print(f" [{mark}] {fmt_char(ch['id'])}")
            pause()
