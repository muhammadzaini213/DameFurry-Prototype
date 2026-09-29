"""
character. Koleksi, per karakter: pilih unit, upgrade level, gift, character story.

Rank TIDAK disentuh di sini (rank hanya naik dari dupe gacha);
level hanya naik dari material milik karakter itu sendiri.
"""

from .config import (BASE_STATS, CHAR_STORY_LEVELS, GIFT_AFFECTION,
                     LEVEL_COST_BASE, LEVEL_COST_STEP, MAX_LEVEL, MAX_RANK,
                     POWER_W, RANK_BUFF, RARITY_STAR, STAT_PER_LEVEL)
from .account import save_state
from .data import (T, CHARACTERS, CHAR_BY_ID, affection_of, char_story_key,
                   char_story_open, mat_name, sorted_by_rarity, species_of)
from .ui import ask, ask_key, ask_pick, header, is_yes, pause

def fmt_char(cid, entry=None, stats=True):
    c = CHAR_BY_ID[cid]
    head = T("fmt_char", RARITY_STAR[c["rarity"]], c["rarity"], c["name"],
             c["object"], species_of(c), c["role"])
    if not entry or not stats:
        return head
    atk, dfn, hp = char_stats(cid, entry)
    return head + T("fmt_stats", entry["lvl"], MAX_LEVEL, entry["rank"],
                    MAX_RANK, atk, dfn, hp, char_power(cid, entry))

# ----------------------------------------------------------------------------
# STAT / LEVEL
# ----------------------------------------------------------------------------
def level_cost(lvl):
    """Material yang dibutuhkan untuk naik dari Lv.lvl ke Lv.lvl+1."""
    return LEVEL_COST_BASE + lvl * LEVEL_COST_STEP


def char_stats(cid, entry):
    """(ATK, DEF, HP) = base rarity + growth level, dikali buff rank."""
    atk, dfn, hp = BASE_STATS[CHAR_BY_ID[cid]["rarity"]]
    growth = (entry["lvl"] - 1) * STAT_PER_LEVEL
    mult = 1.0 + (entry["rank"] - 1) * RANK_BUFF
    return (int((atk + growth) * mult),
            int((dfn + growth) * mult),
            int((hp + growth) * mult))


def char_power(cid, entry):
    """Angka 'Power' gabungan stat, buat lihat rate progres karakter."""
    atk, dfn, hp = char_stats(cid, entry)
    return atk * POWER_W[0] + dfn * POWER_W[1] + hp * POWER_W[2]

# ----------------------------------------------------------------------------
# KOLEKSI & PILIH KARAKTER
# ----------------------------------------------------------------------------

def sorted_owned(st):
    return sorted_by_rarity(st["owned"].keys())


def collection_menu(st):
    while True:
        header(T("coll_title"), st)
        owned = sorted_owned(st)
        if not owned:
            print(T("no_char"))
            print(T("hint_first"))
            pause()
            return
        for i, cid in enumerate(owned, 1):
            act = T("active_flag") if cid == st["active"] else ""
            print(f" [{i:>2}] {fmt_char(cid, st['owned'][cid], st['show_stats'])}{act}")
        print(T("count_owned", len(owned), len(CHARACTERS)))
        print(T("pick_active"))
        n = ask_pick("> ", 0, len(owned))
        if n == 0:
            return
        cid = owned[n - 1]
        name = CHAR_BY_ID[cid]["name"]
        # Dua pilihan terpisah. Dulu sekali ketik nomor langsung mengganti
        # unit dan membuka hub, jadi membuka detail diam-diam ganti unit.
        print()
        print(T("pick_action", name))
        print(" [1]" + T("a_hub"))
        print(" [2]" + T("a_unit"))
        print(T("back"))
        act = ask_key({"0", "1", "2"})
        if act == "1":
            character_menu(st, cid)      # upgrade / gift / character story
            save_state(st)
        elif act == "2":
            st["active"] = cid
            save_state(st)
            print(T("active_now", name))


def upgrade_char(st, cid):
    """
    Naikkan level karakter pakai material miliknya sendiri.
    Rank tidak disentuh di sini; rank tetap datang dari dupe gacha.
    """
    c = CHAR_BY_ID[cid]
    entry = st["owned"][cid]
    if entry["lvl"] >= MAX_LEVEL:
        print(T("max_level_line", c["name"], MAX_LEVEL))
        return
    while entry["lvl"] < MAX_LEVEL:
        need = level_cost(entry["lvl"])
        have = st["mats"].get(cid, 0)
        print(T("mat_equals", mat_name(cid), have))
        print(T("upgrade_need", c["name"], entry["lvl"], entry["lvl"] + 1, need))
        if have < need:
            print(T("mat_short"))
            pause()
            return
        if not is_yes(ask(T("upgrade_q"))):
            return
        st["mats"][cid] = have - need
        entry["lvl"] += 1
        atk, dfn, hp = char_stats(cid, entry)
        print(T("lvup", entry["lvl"], atk, dfn, hp, char_power(cid, entry)))
    print(T("max_level_line", c["name"], MAX_LEVEL))
    pause()

def char_story_menu(st, cid):
    """Daftar cerita milik SATU karakter. Unlock murni dari affection dia."""
    c = CHAR_BY_ID[cid]
    while True:
        header(T("cs_title", c["name"]), st)
        aff = affection_of(st, cid)
        print(T("affection_line", aff))
        print()
        for i, need in enumerate(CHAR_STORY_LEVELS, 1):
            if char_story_open(st, cid, i):
                if char_story_key(cid, i) in st["read_story"]:
                    status, extra = T("ms_status_read"), ""
                else:
                    status, extra = T("ms_status_new"), ""
            else:
                status, extra = T("ms_status_locked"), T("cs_need", need)
            print(T("cs_line", status, i, extra))
        print(T("back"))
        n = ask_pick("> ", 0, len(CHAR_STORY_LEVELS))
        if n == 0:
            return
        need = CHAR_STORY_LEVELS[n - 1]
        if not char_story_open(st, cid, n):
            print(T("cs_locked", aff, need))
            pause()
            continue
        header(f"{T('cs_title', c['name'])} #{n}")
        print(T("story_body"))
        if char_story_key(cid, n) not in st["read_story"]:
            st["read_story"].append(char_story_key(cid, n))
            save_state(st)
        pause()


def give_gift(st, cid):
    """Konsumsi 1 gift -> affection naik. Return True kalau gift terpakai."""
    c = CHAR_BY_ID[cid]
    if st["gifts"] <= 0:
        print(T("no_gift"))
        pause()
        return False
    before = affection_of(st, cid)
    st["gifts"] -= 1
    st["affection"][cid] = before + GIFT_AFFECTION
    aff = st["affection"][cid]
    print(T("gave_gift", c["name"], aff, GIFT_AFFECTION))
    for i, need in enumerate(CHAR_STORY_LEVELS, 1):
        if before < need <= aff:          # baru saja melewati ambang
            print(T("cs_unlocked", c["name"], i))
    save_state(st)
    pause()
    return True


def character_menu(st, cid):
    """
    Hub per karakter setelah dipilih di Koleksi:
    tampil progression dia (level/affection/cerita) + aksinya.
    """
    c = CHAR_BY_ID[cid]
    while True:
        header(T("char_title", c["name"]), st)
        entry = st["owned"][cid]
        print(" " + fmt_char(cid, entry, st["show_stats"]))
        aff = affection_of(st, cid)
        print(T("affection_line", aff))
        print(T("gift_line", st["gifts"]))
        nxt = next((need for need in CHAR_STORY_LEVELS if aff < need), None)
        if nxt is not None:
            print(T("affection_next", CHAR_STORY_LEVELS.index(nxt) + 1, nxt))
        print()
        print(T("a_upgrade"))
        print(T("a_gift", st["gifts"]))
        print(T("a_story"))
        print(T("back"))
        c_in = ask_key({"0", "1", "2", "3"})
        if c_in == "0":
            return
        elif c_in == "1":
            upgrade_char(st, cid)
            save_state(st)
        elif c_in == "2":
            give_gift(st, cid)
        elif c_in == "3":
            char_story_menu(st, cid)
