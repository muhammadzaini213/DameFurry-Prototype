"""
shop. Shop (tiket + material, pakai coins) dan topup (dummy Rupiah -> gems).

TIDAK PERNAH menjual karakter. Coins untuk shop, gems hanya dari topup.
"""

from .account import save_state
from .config import SHOP_MAT_PRICE, TICKET_PRICE, TOPUP_PACKS
from .data import T, CHAR_BY_ID, mat_name, sorted_by_rarity
from .ui import ask, ask_key, ask_pick, fmt_idr, header, is_yes, pause

# ----------------------------------------------------------------------------
# SHOP (tiket gacha + material, tanpa jual karakter)
# ----------------------------------------------------------------------------
def shop_menu(st):
    while True:
        header(T("shop_title"), st)
        print(T("tickets_owned", st["tickets"]))
        print()
        print(T("shop_tickets", TICKET_PRICE))
        print(T("shop_material"))
        print(T("back"))
        c = ask_key({"0", "1", "2"})
        if c == "0":
            return
        elif c == "1":
            buy_tickets(st)
        elif c == "2":
            shop_material_menu(st)


def buy_tickets(st):
    n = ask_pick(T("how_many_tiket", 99), 0, 99)
    if n == 0:
        return
    cost = TICKET_PRICE * n
    if st["coins"] < cost:
        print(T("coins_short", cost, st["coins"]))
        pause()
        return
    st["coins"] -= cost
    st["tickets"] += n
    print(T("got_tickets", n, st["tickets"]))
    save_state(st)
    pause()


def shop_material_menu(st):
    while True:
        header(T("mat_shop_title"), st)
        print(T("mat_shop_note1"))
        print(T("mat_shop_note2"))
        ids = sorted_by_rarity(CHAR_BY_ID.keys())
        for i, cid in enumerate(ids, 1):
            rar = CHAR_BY_ID[cid]["rarity"]
            have = st["mats"].get(cid, 0)
            own = f"Lv.{st['owned'][cid]['lvl']}" if cid in st["owned"] else "-"
            print(T("mat_line", i, mat_name(cid), rar, SHOP_MAT_PRICE[rar],
                    have, own))
        print(T("pick_mat"))
        n = ask_pick("> ", 0, len(ids))
        if n == 0:
            return
        cid = ids[n - 1]
        rar = CHAR_BY_ID[cid]["rarity"]
        price = SHOP_MAT_PRICE[rar]
        qty = ask_pick(T("buy_qty_q", mat_name(cid), price, 999), 0, 999)
        if qty == 0:
            continue
        cost = price * qty
        if st["coins"] < cost:
            print(T("coins_short", cost, st["coins"]))
            pause()
            continue
        st["coins"] -= cost
        st["mats"][cid] = st["mats"].get(cid, 0) + qty
        print(T("bought_mat", qty, mat_name(cid), cost))
        save_state(st)
        pause()


# ----------------------------------------------------------------------------
# TOPUP (dummy Rupiah -> gems, tanpa pembayaran asli)
# ----------------------------------------------------------------------------
def topup_menu(st):
    while True:
        header(T("topup_title"), st)
        for i, p in enumerate(TOPUP_PACKS, 1):
            bonus = T("topup_bonus", p["bonus"]) if p["bonus"] else ""
            total = p["gems"] + p["bonus"]
            print(f" [{i}] {fmt_idr(p['idr']):<14} -> {total} gems{bonus}")
        print(T("back"))
        n = ask_pick("> ", 0, len(TOPUP_PACKS))
        if n == 0:
            return
        p = TOPUP_PACKS[n - 1]
        total = p["gems"] + p["bonus"]
        if is_yes(ask(T("topup_confirm", p["name"], fmt_idr(p["idr"]), T("yes_word")))):
            st["gems"] += total
            st["topups"] += 1
            bonus_note = T("topup_bonus", p["bonus"]) if p["bonus"] else ""
            print(T("topup_ok", total, bonus_note, st["gems"]))
            save_state(st)
        else:
            print(T("topup_cancel"))
        pause()
