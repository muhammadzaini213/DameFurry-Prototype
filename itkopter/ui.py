"""
ui. Primitif layar: garis, header, ask/pause, dan format angka.

di bawah semua modul domain supaya domain boleh mencetak tanpa
cyclical import ke menus.py.
"""

from .data import T

# ----------------------------------------------------------------------------
# HELPER UI
# ----------------------------------------------------------------------------
def line(ch="=", n=52):
    print(ch * n)


def header(title, st=None):
    print()
    line()
    print(f" {title}")
    if st:
        print(T("gems_coins", st["gems"], st["coins"]))
    line()


def ask(prompt="> "):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return "0"


def pause():
    ask(T("pause"))


def ask_int(prompt, lo, hi):
    """Minta angka lo..hi. Return None kalau input tidak valid."""
    s = ask(prompt)
    if s.isdigit() and lo <= int(s) <= hi:
        return int(s)
    return None


def ask_pick(prompt, lo, hi):
    """ask_int sampai valid, TANPA mengulang layar.

    Input salah cuma mencetak satu baris [!] lalu menanya ulang. Dulu tiap
    salah satu menu mencetak ulang seluruh layar (header + daftar pilihan),
    jadi riwayat di atasnya hilang dan sulit dibaca.

    INVARIAN: `lo` HARUS 0. ask() memakai "0" sebagai penanda EOF, jadi
    dengan lo == 0 stdin yang habis selalu keluar dari loop ini dengan bersih.
    """
    while True:
        n = ask_int(prompt, lo, hi)
        if n is not None:
            return n
        print(T("invalid"))


def ask_key(valid, prompt="> "):
    """ask() sampai masuk `valid` (set of string), TANPA mengulang layar.

    INVARIAN: `valid` HARUS memuat "0". ask() memakai "0" sebagai penanda
    EOF/KeyboardInterrupt, jadi stdin yang habis selalu keluar dari loop ini
    dengan bersih. Kalau "0" tidak diizinkan, layar bisa berputar selamanya.
    """
    while True:
        s = ask(prompt)
        if s in valid:
            return s
        print(T("invalid"))


def onoff(flag):
    return T("on") if flag else T("off")

def fmt_idr(n):
    return "Rp " + f"{n:,}".replace(",", ".")

def is_yes(s):
    """Jawaban ya di Bahasa Indonesia maupun English, tanpa peduli kapital.

    Dulu cuma T("yes_word") dibandingkan persis, jadi mengetik "y" di mode ID
    atau "ya" di mode EN membatalkan aksi diam-diam tanpa pesan apa pun.
    """
    return str(s).strip().lower() in ("ya", "y", "yes")
