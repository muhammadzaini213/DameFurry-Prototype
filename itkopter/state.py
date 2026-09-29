"""
state. Schema save + normalisasi.

new_state() adalah definisi satu-satunya field save;
normalize_state() mem-repair save lama / save rusak sebelum dipakai.
"""

from .config import (MAX_LEVEL, MAX_RANK, START_GEMS, START_GIFTS,
                     START_HIDE_DEBUG, START_SHOW_STATS, START_VOLUME)
from .data import CHAR_BY_ID, LANGS, set_lang, sorted_by_rarity

# force_next yang diizinkan debug; nilai lain dari save liar dibuang.
FORCE_VALUES = (None, "R", "SR", "SSR")

def new_state():
    return {
        "account": None,        # nama akun, None = belum login / Tamu
        "lang": "id",           # bahasa UI: "id" | "en"
        "volume": START_VOLUME, # 0..100 (belum ada konsumen audio)
        "show_stats": START_SHOW_STATS,
        "hide_debug": START_HIDE_DEBUG,
        "gems": START_GEMS,
        "coins": 0,
        "tickets": 0,           # tiket gacha dari shop, 1 tiket = 1 pull
        "pity": 0,              # pull sejak SSR terakhir
        "total_pulls": 0,
        "topups": 0,            # berapa kali menu topup dipakai (statistik)
        "owned": {},            # id -> {"rank": 1..MAX_RANK, "lvl": 1..MAX_LEVEL}
        "mats": {},             # id karakter -> jumlah material (untuk upgrade level)
        "gifts": START_GIFTS,   # gift yang belum dipakai (sumber: TBD, lihat AGENTS.md)
        "affection": {},        # id karakter -> affection (per karakter, bukan global)
        "read_story": [],       # key cerita yang sudah dibaca: "m:1" / "c:monas:2"
        "active": None,         # id karakter yang dipakai bertarung
        "cleared": [],          # list id stage yang sudah clear
        "wins": 0,
        "losses": 0,
        "force_next": None,     # dipakai debug: paksa rarity pull berikutnya
    }


def normalize_state(data, account=None):
    """
    Rapikan data save mentah jadi state yang valid.

    Tujuan: save apa pun (rusak sebagian, salah tipe, nilai liar) harus
    selalu menghasilkan state yang bisa dipakai, bukan exception.
    Save lama punya owned[id] = rank (int) -> diubah jadi {"rank","lvl"}.
    Id karakter yang sudah dihapus dari CHARACTERS dibuang biar tidak
    bikin KeyError.
    """
    if not isinstance(data, dict):
        data = {}
    st = new_state()
    st.update(data)
    raw_owned = st.get("owned")
    owned = {}
    for cid, v in (raw_owned.items() if isinstance(raw_owned, dict) else ()):
        if cid not in CHAR_BY_ID:
            continue
        if isinstance(v, int):          # migrasi save versi lama
            v = {"rank": v}
        if not isinstance(v, dict):
            v = {}
        # rank/lvl di-clamp: save berisi 0 / 999 tidak boleh bocor ke UI.
        owned[cid] = {"rank": _num(v.get("rank"), 1, 1, MAX_RANK),
                      "lvl": _num(v.get("lvl"), 1, 1, MAX_LEVEL)}
    st["owned"] = owned
    # Anti-buntu: kalau punya karakter tapi active tidak valid, stage menolak
    # masuk dengan pesan "belum ada unit" padahal koleksi tidak kosong.
    if owned:
        act = st.get("active")
        if not isinstance(act, str) or act not in owned:
            st["active"] = sorted_by_rarity(owned.keys())[0]
    else:
        st["active"] = None
    raw_mats = st.get("mats")
    st["mats"] = {cid: _num(n, 0)
                  for cid, n in (raw_mats.items() if isinstance(raw_mats, dict) else ())
                  if cid in CHAR_BY_ID}
    # affection per karakter: buang id yang sudah tidak ada di roster
    aff = {}
    raw_aff = st.get("affection")
    for cid, v in (raw_aff.items() if isinstance(raw_aff, dict) else ()):
        if cid not in CHAR_BY_ID:
            continue
        n = _num(v, None)
        if n is not None:
            aff[cid] = n
    st["affection"] = aff
    raw_read = st.get("read_story")
    if not isinstance(raw_read, list):
        raw_read = []
    st["read_story"] = [k for k in raw_read if isinstance(k, str)]
    # Angka: dipaksa jadi int >= 0. Nilai hilang/rusak -> 0 (bukan default
    # new_state), supaya save yang korup tidak mendapat gems gratis.
    for key in ("gems", "coins", "pity", "total_pulls", "wins", "losses",
                "tickets", "topups"):
        st[key] = _num(st.get(key), 0)
    st["volume"] = _num(st.get("volume"), START_VOLUME, 0, 100)
    st["gifts"] = _num(st.get("gifts"), START_GIFTS)
    for key in ("show_stats", "hide_debug"):
        if not isinstance(st.get(key), bool):
            st[key] = new_state()[key]
    # force_next disimpan di save; nilai asing bikin random.choice([]) crash.
    if st.get("force_next") not in FORCE_VALUES:
        st["force_next"] = None
    if account is not None:
        st["account"] = account
    if st.get("lang") not in LANGS:
        st["lang"] = "id"
    set_lang(st["lang"])
    return st


def _num(v, default, lo=0, hi=None):
    """Coerce jadi int; gagal -> default. lo/hi = batas opsional."""
    try:
        n = int(v)
    except (TypeError, ValueError):
        return default
    n = max(lo, n)
    return min(hi, n) if hi is not None else n
