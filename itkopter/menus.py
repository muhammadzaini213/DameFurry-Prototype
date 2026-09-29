"""
menus. Menu utilitas: cerita, profil, pengaturan.

Main Story (stage) dan Character Story (affection) sengaja dipisah;
lihat blok komentar di data.py.
"""

from .account import account_menu, save_state
from .character import char_story_menu, fmt_char, sorted_owned
from .config import GUEST, HARD_PITY_SSR
from .data import (T, CHARACTERS, CHAR_BY_ID, CHAR_STORY_LEVELS, LANG_LABEL,
                   MAIN_STORY, STAGES, affection_of, chapter_title,
                   char_story_open, main_key, main_story_open, mat_name, set_lang,
                   sorted_by_rarity)
from .ui import ask_key, ask_pick, header, onoff, pause

def main_story_menu(st):
    while True:
        header(T("ms_title"), st)
        for ch in MAIN_STORY:
            if not main_story_open(st, ch):
                status, extra = T("ms_status_locked"), T("ms_need", ch["unlock_stage"])
            elif main_key(ch) in st["read_story"]:
                status, extra = T("ms_status_read"), ""
            else:
                status, extra = T("ms_status_new"), ""
            print(T("ms_line", status, ch["id"], chapter_title(ch)) + " " + extra)
        print(T("back"))
        n = ask_pick("> ", 0, len(MAIN_STORY))
        if n == 0:
            return
        ch = MAIN_STORY[n - 1]
        if not main_story_open(st, ch):
            print(T("ms_locked", ch["unlock_stage"]))
            pause()
            continue
        header(f"{T('ms_title')} {ch['id']} - {chapter_title(ch)}")
        print(T("story_body"))
        if main_key(ch) not in st["read_story"]:
            st["read_story"].append(main_key(ch))
            save_state(st)
        pause()

def char_story_pick_menu(st):
    """Pilih karakter (dari koleksi) untuk melihat Character Story miliknya."""
    while True:
        header(T("cs_pick"), st)
        owned = sorted_owned(st)
        if not owned:
            print(T("no_char"))
            pause()
            return
        for i, cid in enumerate(owned, 1):
            aff = affection_of(st, cid)
            n_open = sum(1 for x in range(1, len(CHAR_STORY_LEVELS) + 1)
                         if char_story_open(st, cid, x))
            print(f" [{i:>2}] {fmt_char(cid, st['owned'][cid], st['show_stats'])}"
                  + T("cs_count", aff, n_open, len(CHAR_STORY_LEVELS)))
        print(T("back"))
        n = ask_pick("> ", 0, len(owned))
        if n == 0:
            return
        char_story_menu(st, owned[n - 1])


def story_menu(st):
    """Titik akses cerita. [1] Main Story = stage, [2] Character Story = affection."""
    while True:
        header(T("story_title"), st)
        n_new = sum(1 for ch in MAIN_STORY
                    if main_story_open(st, ch) and main_key(ch) not in st["read_story"])
        print(T("story_main") + (T("story_new_badge", n_new) if n_new else ""))
        print(T("story_char"))
        print(T("back"))
        c = ask_key({"0", "1", "2"})
        if c == "0":
            return
        elif c == "1":
            main_story_menu(st)
        elif c == "2":
            char_story_pick_menu(st)

# ----------------------------------------------------------------------------
# PROFIL
# ----------------------------------------------------------------------------
def profile_menu(st):
    header(T("profile_title"), st)
    active = CHAR_BY_ID[st["active"]]["name"] if st["active"] else "-"
    print(T("prof_active", active))
    print(T("prof_coll", len(st["owned"]), len(CHARACTERS)))
    print(T("prof_pull", st["total_pulls"], st["pity"], HARD_PITY_SSR))
    print(T("prof_clear", len(st["cleared"]), len(STAGES)))
    print(T("prof_wl", st["wins"], st["losses"]))
    print(T("prof_tickets", st["tickets"]))
    print(T("prof_gift", st["gifts"]))
    print(T("prof_topup", st["topups"]))
    print(T("prof_account", st["account"] or GUEST))
    if st["active"]:
        print("\n " + fmt_char(st["active"], st["owned"][st["active"]],
                               st["show_stats"]))
    mats = {c: n for c, n in st["mats"].items() if n > 0}
    if mats:
        print(T("prof_mat"))
        for c in sorted_by_rarity(mats):
            e = st["owned"].get(c)
            lv = f"Lv.{e['lvl']}" if e else T("not_owned")
            print(f"   {mat_name(c)} x{mats[c]}   ({lv})")
    else:
        print(T("prof_mat_none"))
    pause()


# ----------------------------------------------------------------------------
# PENGATURAN
# ----------------------------------------------------------------------------
def settings_menu(st):
    while True:
        header(T("set_title"), st)
        print(T("set_lang", LANG_LABEL[st["lang"]]))
        print(T("set_volume", st["volume"]))
        print(T("set_stats", onoff(st["show_stats"])))
        print(T("set_debug", onoff(not st["hide_debug"])))
        print(T("set_account"))
        print()
        print(T("back"))
        c = ask_key({"0", "1", "2", "3", "4", "5"})
        if c == "0":
            return
        elif c == "1":
            st["lang"] = "en" if st["lang"] == "id" else "id"
            set_lang(st["lang"])
            print(T("lang_switched", LANG_LABEL[st["lang"]]))
            save_state(st)
            pause()
        elif c == "2":
            v = ask_pick(T("vol_q"), 0, 100)
            # 0 adalah volume valid, bukan sinyal batal.
            st["volume"] = v
            save_state(st)
            print(T("vol_saved", v))
            pause()
        elif c == "3":
            st["show_stats"] = not st["show_stats"]
            save_state(st)
        elif c == "4":
            st["hide_debug"] = not st["hide_debug"]
            save_state(st)
        elif c == "5":
            account_menu(st)
