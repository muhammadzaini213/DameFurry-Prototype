"""
main. Menu utama + loop dispatch.

Jalankan:  python3 itkopter_cli.py  (shim)  atau  python3 -m itkopter.main
"""

from .account import open_session, save_state
from .character import collection_menu
from .data import T, CHAR_BY_ID
from .debug import debug_menu
from .gacha import gacha_menu
from .menus import profile_menu, settings_menu, story_menu
from .shop import shop_menu, topup_menu
from .stages import stage_menu
from .ui import ask_key, header

# ----------------------------------------------------------------------------
# MAIN MENU
# ----------------------------------------------------------------------------
def main():
    st = open_session()
    if st is None:
        print(T("bye"))
        return
    while True:
        header(T("main_title"), st)
        active = (CHAR_BY_ID[st["active"]]["name"] if st["active"]
                  else T("no_unit"))
        print(T("unit_line", active))
        # Arahan singkat biar pemain baru tidak bingung harus mulai dari mana.
        if not st["owned"]:
            print(T("hint_first"))
        elif st["active"] is None:
            print(T("hint_pick"))
        print(T("m_mission"))
        print(T("m_gacha"))
        print(T("m_collection"))
        print(T("m_profile"))
        print(T("m_shop"))
        print(T("m_topup"))
        print(T("m_settings"))
        print(T("m_story"))
        if not st["hide_debug"]:
            print(T("m_debug"))
        print(T("m_exit"))
        # [9] Debug disembunyikan lewat Settings -> ikut keluar dari daftar
        # pilihan valid, jadi menekannya kini dapat balasan [!] sekali saja
        # alih-alih memutar ulang seluruh layar utama.
        valid = set("012345678") if st["hide_debug"] else set("0123456789")
        c = ask_key(valid)
        if c == "1":
            stage_menu(st)
        elif c == "2":
            gacha_menu(st)
        elif c == "3":
            collection_menu(st)
        elif c == "4":
            profile_menu(st)
        elif c == "5":
            shop_menu(st)
        elif c == "6":
            topup_menu(st)
        elif c == "7":
            settings_menu(st)
        elif c == "8":
            story_menu(st)
        elif c == "9":
            debug_menu(st)
        elif c == "0":
            save_state(st)
            print(T("bye"))
            break
        if st.pop("force_quit", None):
            # logout dibatalkan: sesi sudah dibersihkan logout() dan state
            # sudah di-save di sana -- jangan save_state() lagi, karena bisa
            # menulis ulang session (membatalkan logout) atau menimpa file
            # Tamu dengan data akun lain.
            print(T("bye"))
            break


if __name__ == "__main__":
    main()
