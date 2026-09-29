"""
config. Konfigurasi & tombol balance. Semua angka yang enak diubah ada di sini.
"""

# Save file default (= slot "Tamu"). Path relatif terhadap CWD, bukan lokasi skrip.
SAVE_FILE = "itkopter_save.json"
SESSION_FILE = "itkopter_session.json"   # akun mana yang sedang dipakai + bahasa
GUEST = "Tamu"

# ----------------------------------------------------------------------------
# KONFIGURASI (ubah sesuka hati untuk ngetes balance / alur)
# ----------------------------------------------------------------------------
GEM_PER_PULL = 160
START_GEMS = 3200
RATES = {"SSR": 0.02, "SR": 0.13, "R": 0.85}
HARD_PITY_SSR = 50          # pull ke-50 tanpa SSR = pasti SSR
TENPULL_GUARANTEE = "SR"    # 10x pull minimal 1 SR ke atas
MAX_RANK = 5                # duplikat menaikkan rank sampai batas ini
DUPE_COIN_REFUND = {"R": 50, "SR": 200, "SSR": 800}   # kalau sudah rank max

# Level upgrade. Rank (dari dupe) sama level (dari material) itu DUA sumbu
# terpisah: rank kasih buff persen, level tambah stat.
MAX_LEVEL = 20
LEVEL_COST_BASE = 3         # material untuk naik dari Lv.N -> Lv.N+1
LEVEL_COST_STEP = 1         # tiap level naik, cost naik sebesar ini
RANK_BUFF = 0.10            # +10% semua stat per rank di atas rank 1
STAT_PER_LEVEL = 6          # tambahan ATK/DEF/HP per level
BASE_STATS = {              # (ATK, DEF, HP) dasar per rarity
    "SSR": (120, 80, 100),
    "SR": (90, 60, 80),
    "R": (60, 40, 60),
}
POWER_W = (2, 1, 1)         # bobot ATK/DEF/HP jadi angka "Power"

# --- SHOP (semua pakai coins; tanpa jual karakter) ---
TICKET_PRICE = 1500            # coins per tiket gacha, 1 tiket = 1 pull
SHOP_MAT_PRICE = {             # coins per unit material, beda per rarity
    "R": 10,
    "SR": 25,
    "SSR": 60,
}

# --- TOPUP (dummy, tidak ada pembayaran beneran) ---
TOPUP_PACKS = [
    {"name": "Koin Perdana",   "idr": 15000,   "gems": 1000,  "bonus": 0},
    {"name": "Kantong Reguler","idr": 75000,   "gems": 5500,  "bonus": 500},
    {"name": "Peti Sultan",    "idr": 250000,  "gems": 20000, "bonus": 2500},
    {"name": "Peti Sultan++",  "idr": 990000,  "gems": 88000, "bonus": 12000},
]

# --- PENGATURAN (nilai default sebelum save punya field-nya) ---
START_VOLUME = 70           # 0..100. Belum ada konsumen audio: cuma disimpan & ditampilkan.
START_SHOW_STATS = True     # tampil/sembunyi ATK/DEF/HP/Power di list koleksi
START_HIDE_DEBUG = False    # sembunyikan menu [9] Debug di menu utama

LOSE_COINS = 50     # hadiah hiburan kalau kalah

# --- CHARACTER STORY (dibuka oleh AFFECTION per karakter) ---
# Dua sumbu cerita ini sengaja dipisah total: MAIN_STORY pakai stage,
# CHAR_STORY_LEVELS pakai affection. Jangan dicampur.
CHAR_STORY_LEVELS = [1, 2, 3]   # ambang affection per cerita (urut)
GIFT_AFFECTION = 1              # affection yang didapat per gift
START_GIFTS = 0                 # jumlah gift awal. SUMBER GIFT = TBD (fitur gap).

RARITY_ORDER = {"SSR": 0, "SR": 1, "R": 2}
RARITY_STAR = {"SSR": "★★★", "SR": "★★ ", "R": "★  "}
