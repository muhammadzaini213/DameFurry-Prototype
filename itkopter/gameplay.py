"""
gameplay. PLACEHOLDER -- ganti fungsi run_gameplay() dengan gameplay asli.

Kontrak return: True = menang, False = kalah, None = batal/keluar.
stage_menu memperlakukan None sebagai "kembali tanpa hadiah".
"""

from .data import T, CHAR_BY_ID, diff_of, stage_name
from .ui import ask, header

# ----------------------------------------------------------------------------
# GAMEPLAY (PLACEHOLDER) & STAGE
# ----------------------------------------------------------------------------
def run_gameplay(stage, char_id):
    """
    GANTI FUNGSI INI dengan gameplay asli nanti.
    Return True = menang, False = kalah, None = batal/keluar.
    Sekarang: opsi debug manual.
    """
    c = CHAR_BY_ID[char_id]
    header(T("gp_title", stage["id"], stage_name(stage)))
    print(T("gp_unit", c["name"], c["object"], c["role"]))
    print(T("gp_level", diff_of(stage)))
    print(T("gp_debug"))
    print(T("gp_win"))
    print(T("gp_lose"))
    print(T("gp_abort"))
    c_in = ask()
    if c_in == "1":
        return True
    if c_in == "2":
        return False
    return None
