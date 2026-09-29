"""
data. Data statis + i18n.

Isi CHARACTERS / STAGES / MAIN_STORY, terjemahan bahasa
(STR / T / set_lang), dan helper turunan murni (mat_name, species_of,
sorted_by_rarity, predikat buka cerita).
"""

from .config import CHAR_STORY_LEVELS, RARITY_ORDER

# Daftar karakter. Tambah/ubah bebas.
# role = placeholder untuk tipe pesawat/pola peluru nanti.
CHARACTERS = [
    # ---- SSR : bangunan/landmark ikonik
    {"id": "monas",    "name": "Monasu",    "object": "Tugu Monas",       "species": "Kucing Emas",   "rarity": "SSR", "role": "Sniper Laser"},
    {"id": "borobdr",  "name": "Boroko",    "object": "Candi Borobudur",  "species": "Serigala Batu", "rarity": "SSR", "role": "Tank Spread"},
    {"id": "suramadu", "name": "Suramadi",  "object": "Jembatan Suramadu","species": "Rubah Merah",   "rarity": "SSR", "role": "Wave Sweeper"},
    # ---- SR : bangunan umum / fasilitas
    {"id": "gdsate",   "name": "Satria",    "object": "Gedung Sate",      "species": "Kelinci",       "rarity": "SR", "role": "Homing"},
    {"id": "haltebus", "name": "Halta",     "object": "Halte Bus",        "species": "Anjing Husky",  "rarity": "SR", "role": "Spread"},
    {"id": "menara",   "name": "Tora",      "object": "Menara Air",       "species": "Panda Merah",   "rarity": "SR", "role": "Rain Bullet"},
    {"id": "gerbang",  "name": "Gerbi",     "object": "Gerbang Tol",      "species": "Kucing Hitam",  "rarity": "SR", "role": "Barrier"},
    {"id": "mercusuar","name": "Suara",     "object": "Mercusuar",        "species": "Burung Hantu",  "rarity": "SR", "role": "Rotating Beam"},
    # ---- R : benda mati sehari-hari
    {"id": "kulkas",   "name": "Kulka",     "object": "Kulkas",           "species": "Beruang Kutub", "rarity": "R", "role": "Freeze Shot"},
    {"id": "cone",     "name": "Koni",      "object": "Kerucut Jalan",    "species": "Rubah Oranye",  "rarity": "R", "role": "Straight"},
    {"id": "tiang",    "name": "Listra",    "object": "Tiang Listrik",    "species": "Tupai",         "rarity": "R", "role": "Chain Lightning"},
    {"id": "vending",  "name": "Vendi",     "object": "Vending Machine",  "species": "Rakun",         "rarity": "R", "role": "Random Shot"},
    {"id": "kursi",    "name": "Kurisu",    "object": "Kursi Plastik",    "species": "Kucing Belang", "rarity": "R", "role": "Straight"},
    {"id": "ember",    "name": "Embra",     "object": "Ember Cat",        "species": "Kambing",       "rarity": "R", "role": "Splash"},
    {"id": "warung",   "name": "Warna",     "object": "Warung Kopi",      "species": "Kucing Oren",   "rarity": "R", "role": "Heal Aura"},
    {"id": "payung",   "name": "Payuni",    "object": "Payung",           "species": "Musang",        "rarity": "R", "role": "Shield"},
]
CHAR_BY_ID = {c["id"]: c for c in CHARACTERS}

# Material level tiap karakter itu milik dia sendiri: material "X" hanya menaikkan
# level karakter X, tidak bisa untuk karakter lain. Stage drop material lewat
# STAGES[].drops (kunci = id karakter).
MAT_NAME = {c["id"]: f"Serbuk {c['name']}" for c in CHARACTERS}

# Terjemahan species (dipakai hanya saat bahasa = en; kalau kunci hilang, jatuh
# balik ke species Indonesia sehingga menambah karakter baru tidak bikin error).
SPECIES_EN = {
    "Kucing Emas": "Golden Cat", "Serigala Batu": "Stone Wolf",
    "Rubah Merah": "Red Fox", "Kelinci": "Rabbit", "Anjing Husky": "Husky Dog",
    "Panda Merah": "Red Panda", "Kucing Hitam": "Black Cat",
    "Burung Hantu": "Owl", "Beruang Kutub": "Polar Bear",
    "Rubah Oranye": "Orange Fox", "Tupai": "Squirrel", "Rakun": "Raccoon",
    "Kucing Belang": "Calico Cat", "Kambing": "Goat",
    "Kucing Oren": "Ginger Cat", "Musang": "Civet",
}
DIFF_EN = {"Mudah": "Easy", "Normal": "Normal", "Sulit": "Hard", "Boss": "Boss"}

# Stage. Urut, harus clear yang sebelumnya untuk buka berikutnya.
# "drops" = material yang didapat tiap clear (rewards lain cuma first-clear).
# Jumlah material sengaja datar: yang mahal bukan quantity tapi stage mana yang
# drop material itu. Butuh ~5 clear stage 1 buat Lv.MAX karakter R.
STAGES = [
    {"id": 1, "name": "Landasan Kampus", "name_en": "Campus Runway",  "diff": "Mudah",
     "gems": 60, "coins": 300, "first_bonus": 160,
     "drops": {"warung": 50, "kursi": 50, "kulkas": 45, "cone": 45}},
    {"id": 2, "name": "Atap Gedung Rektorat", "name_en": "Rectorate Rooftop", "diff": "Mudah",
     "gems": 60, "coins": 400, "first_bonus": 160,
     "drops": {"tiang": 45, "vending": 45, "payung": 40, "gdsate": 30}},
    {"id": 3, "name": "Kolong Jembatan", "name_en": "Under the Bridge", "diff": "Normal",
     "gems": 80, "coins": 600, "first_bonus": 240,
     "drops": {"ember": 45, "haltebus": 30, "menara": 30}},
    {"id": 4, "name": "Kompleks Industri", "name_en": "Industrial Complex", "diff": "Normal",
     "gems": 80, "coins": 800, "first_bonus": 240,
     "drops": {"gerbang": 30, "mercusuar": 30, "monas": 25}},
    {"id": 5, "name": "Menara Pemancar", "name_en": "Transmitter Tower", "diff": "Sulit",
     "gems": 100, "coins": 1200, "first_bonus": 320,
     "drops": {"monas": 25, "borobdr": 25}},
    {"id": 6, "name": "Puncak Kota (BOSS)", "name_en": "City Peak (BOSS)", "diff": "Boss",
     "gems": 150, "coins": 2000, "first_bonus": 480,
     "drops": {"borobdr": 20, "suramadu": 20}},
]

# --- MAIN STORY (dibuka oleh STAGE, bukan oleh affection) ---
# unlock_stage = id stage yang harus sudah clear. Sengaja tidak dibuka tiap
# stage: cuma momen tertentu (awal, tengah, akhir) yang punya bab.
MAIN_STORY = [
    {"id": 1, "title": "Pembuka",     "title_en": "Opening",     "unlock_stage": 1},
    {"id": 2, "title": "Pertengahan", "title_en": "Midpoint",    "unlock_stage": 3},
    {"id": 3, "title": "Klimaks",     "title_en": "Climax",      "unlock_stage": 6},
]

# ----------------------------------------------------------------------------
# BAHASA (i18n)
# ----------------------------------------------------------------------------
# Semua string yang keluar ke pemain lewat T(key, *args). Kunci yang tidak ada
# di STR akan tampil mentah sebagai key-nya sendiri, jadi typo ketahuan langsung
# di layar, bukan diam-diam.
LANGS = ("id", "en")
LANG_LABEL = {"id": "Indonesia", "en": "English"}
_LANG = "id"


def set_lang(v):
    global _LANG
    _LANG = v if v in LANGS else "id"


def T(key, *args):
    """Ambil string UI sesuai bahasa aktif. Args diisi ke placeholder {}."""
    pair = STR.get(key)
    if pair is None:
        return key
    s = pair[0] if _LANG == "id" else pair[1]
    return s.format(*args) if args else s


STR = {
    # --- umum / bersama ---
    "save_corrupt": ("[!] Save korup, mulai baru.", "[!] Save corrupted, starting fresh."),
    "save_backup": ("[!] Salinan file asli disimpan ke {}.", "[!] Copy of the original file kept at {}."),
    "save_fail": ("[!] Gagal simpan: {}", "[!] Save failed: {}"),
    "pause": ("\n[Enter untuk lanjut]", "\n[Enter to continue]"),
    "invalid": ("[!] Input tidak valid.", "[!] Invalid input."),
    "back": (" [0] Kembali", " [0] Back"),
    "cancel": (" [0] Batal", " [0] Cancel"),
    "gems_coins": (" Gems: {}   Coins: {}", " Gems: {}   Coins: {}"),
    "yes_word": ("ya", "y"),

    # --- menu utama ---
    "main_title": ("ITKOPTER  -  Main Menu", "ITKOPTER  -  Main Menu"),
    "unit_line": (" Unit aktif: {}\n", " Active unit: {}\n"),
    "no_unit": ("(belum ada)", "(none yet)"),
    "m_mission": (" [1] Mulai Misi (Stage)", " [1] Start Mission (Stage)"),
    "m_gacha": (" [2] Gacha", " [2] Gacha"),
    "m_collection": (" [3] Koleksi / Ganti Unit", " [3] Collection / Change Unit"),
    "m_profile": (" [4] Profil", " [4] Profile"),
    "m_shop": (" [5] Shop", " [5] Shop"),
    "m_topup": (" [6] Topup", " [6] Topup"),
    "m_settings": (" [7] Pengaturan", " [7] Settings"),
    "m_debug": (" [9] Debug", " [9] Debug"),
    "m_exit": (" [0] Keluar", " [0] Exit"),
    "bye": ("Sampai jumpa!", "Goodbye!"),

    # --- gacha ---
    "gacha_title": ("GACHA - Panggil Waifu Bangunan",
                    "GACHA - Summon Building Waifus"),
    "gacha_pity": (" Pity SSR: {}/{}   Total pull: {}",
                   " Pity SSR: {}/{}   Total pulls: {}"),
    "gacha_rate": (" Rate: SSR {}% | SR {}% | R {}%",
                   " Rate: SSR {}% | SR {}% | R {}%"),
    "gacha_tickets": (" Tiket: {}", " Tickets: {}"),
    "pull_x1": (" [1] Pull x1   ({} gems atau 1 tiket)",
                " [1] Pull x1   ({} gems or 1 ticket)"),
    "pull_x10": (" [2] Pull x10  ({} gems atau 10 tiket, min 1 {}+)",
                 " [2] Pull x10  ({} gems or 10 tickets, min 1 {}+)"),
    "see_rates": (" [3] Lihat daftar karakter & rate",
                  " [3] View character list & rates"),
    "pull_results": ("\n--- HASIL PULL ---", "\n--- PULL RESULTS ---"),
    "new": ("NEW!", "NEW!"),
    "dupe_rank": ("Duplikat -> Rank {}", "Duplicate -> Rank {}"),
    "refund_max": ("Rank MAX -> +{} coins", "Rank MAX -> +{} coins"),
    "pay_what": ("\n Bayar {} pull pakai apa?", "\n Pay {} pull with what?"),
    "pay_gems": (" [1] Gems   (butuh {}, sisa {})",
                 " [1] Gems   (need {}, left {})"),
    "pay_tiket": (" [2] Tiket  (butuh {}, sisa {})",
                  " [2] Ticket (need {}, left {})"),
    "gems_short": ("\n[!] Gems kurang. Butuh {}, punya {}.",
                   "\n[!] Not enough gems. Need {}, you have {}."),
    "tiket_short": ("\n[!] Tiket kurang. Butuh {}, punya {}.\n Beli di menu Shop.",
                    "\n[!] Not enough tickets. Need {}, you have {}.\n Buy them in Shop."),
    "list_title": ("DAFTAR KARAKTER", "CHARACTER LIST"),

    # --- koleksi / karakter ---
    "coll_title": ("KOLEKSI / PILIH KARAKTER", "COLLECTION / CHOOSE CHARACTER"),
    "no_char": (" Belum punya karakter. Gacha dulu!",
                " No characters yet. Pull the gacha first!"),
    "count_owned": ("\n Terkumpul: {}/{}", "\n Collected: {}/{}"),
    "pick_active": (" Ketik nomor untuk pilih karakter, [0] kembali",
                    " Type a number to pick a character, [0] back"),
    # Pilih karakter bukan lagi aksi tunggal: pemain memilih dulu mau buka hub
    # atau mau ganti unit, supaya memilih tidak diam-diam mengganti unit.
    "pick_action": (" Aksi untuk {}:", " Action for {}:"),
    "a_hub": (" Buka hub karakter (upgrade / gift / cerita)",
              " Open character hub (upgrade / gift / story)"),
    "a_unit": (" Jadikan unit", " Set as unit"),
    "active_now": (" Aktif: {}", " Active: {}"),
    "active_flag": (" <- AKTIF", " <- ACTIVE"),
    "max_level_line": (" {} sudah Lv.{} (MAX).", " {} is already Lv.{} (MAX)."),
    "mat_equals": ("\n {} = {}", "\n {} = {}"),
    "upgrade_need": (" {}  Lv.{} -> Lv.{}  butuh {} material",
                     " {}  Lv.{} -> Lv.{}  needs {} material"),
    "mat_short": (" Material kurang. Clear stage yang drop material ini.",
                  " Not enough material. Clear the stage that drops it."),
    "upgrade_q": (" Upgrade sekarang? (y/n) > ", " Upgrade now? (y/n) > "),
    "lvup": (" Lv.{}!  ATK {}  DEF {}  HP {}  Power {}",
             " Lv.{}!  ATK {}  DEF {}  HP {}  Power {}"),
    "fmt_stats": (" Lv.{}/{} R{}/{} | ATK {} DEF {} HP {} Pow {}",
                  " Lv.{}/{} R{}/{} | ATK {} DEF {} HP {} Pow {}"),
    "fmt_char": ("{} [{:<3}] {:<9} ({} | {} | {})",
                 "{} [{:<3}] {:<9} ({} | {} | {})"),

    # --- gameplay placeholder ---
    "gp_title": ("[GAMEPLAY PLACEHOLDER] Stage {}: {}",
                 "[GAMEPLAY PLACEHOLDER] Stage {}: {}"),
    "gp_unit": (" Unit : {} ({}) - {}", " Unit : {} ({}) - {}"),
    "gp_level": (" Level : {}", " Level : {}"),
    "gp_debug": ("\n --- DEBUG ---", "\n --- DEBUG ---"),
    "gp_win": (" [1] Menang (WIN)", " [1] Win"),
    "gp_lose": (" [2] Kalah  (LOSE)", " [2] Lose"),
    "gp_abort": (" [0] Kabur / batal", " [0] Abort / cancel"),

    # --- stage ---
    "stage_title": ("PILIH STAGE", "SELECT STAGE"),
    "no_active": (" [!] Belum ada karakter aktif. Gacha dulu di menu utama.",
                  " [!] No active character. Pull the gacha first."),
    "locked": ("(TERKUNCI)", "(LOCKED)"),
    "stage_locked": ("[!] Stage masih terkunci.", "[!] Stage still locked."),
    # Drop sengaja ditampilkan di daftar stage biar pemain bisa merencanakan
    # farming sebelum masuk; penanda "(belum dimiliki)" juga muncul di hasil.
    "stage_drops": ("        Drop: {}", "        Drops: {}"),
    "drop_unowned": (" (belum dimiliki)", " (not owned yet)"),
    "result_title": ("HASIL STAGE", "STAGE RESULT"),
    "mission_ok": (" *** MISSION COMPLETE ***", " *** MISSION COMPLETE ***"),
    "mission_fail": (" *** MISSION FAILED ***", " *** MISSION FAILED ***"),
    "reward": (" Reward: +{} gems, +{} coins", " Reward: +{} gems, +{} coins"),
    "first_bonus": (" (First clear bonus +{} gems)",
                    " (First clear bonus +{} gems)"),
    "next_open": (" Stage {} terbuka!", " Stage {} unlocked!"),
    "all_done": (" Semua stage tamat!", " All stages finished!"),
    "mat_drop": (" Material drop:", " Material drops:"),
    "mat_drop_none": (" Tidak ada material drop di stage ini.",
                      " No material drops in this stage."),
    "lose_cons": (" Hadiah hiburan: +{} coins", " Consolation prize: +{} coins"),

    # --- arahan flow (biar pemain baru tidak buntu di menu utama) ---
    "hint_first": ("\n [?] Belum ada karakter. Mulai dari [2] Gacha untuk dapat unit.",
                   "\n [?] No character yet. Start at [2] Gacha to get a unit."),
    "hint_pick": ("\n [?] Unit belum dipilih. Buka [3] Koleksi lalu ketik nomor karakter.",
                  "\n [?] No unit selected. Open [3] Collection and type a character number."),
    "hint_after_reward": (" Material sudah masuk. Buka [3] Koleksi untuk upgrade karakter,",
                          " Material received. Open [3] Collection to upgrade characters,"),
    "hint_after_reward2": (" atau lanjut ke stage berikutnya / [8] Cerita.",
                           " or continue to the next stage / [8] Story."),

    # --- gacha -> koleksi (lanjutan setelah dapat karakter baru) ---
    "gacha_open_coll": (" Buka Koleksi & atur unit sekarang? ({}) : ",
                        " Open Collection & set unit now? ({}) : "),

    # --- cerita (menu utama [8]) ---
    "m_story": (" [8] Cerita", " [8] Story"),
    "story_title": ("CERITA", "STORY"),
    "story_main": (" [1] Main Story        (buka lewat Stage)",
                   " [1] Main Story        (unlocked by Stage)"),
    "story_char": (" [2] Character Story   (buka lewat Affection)",
                   " [2] Character Story   (unlocked by Affection)"),
    "story_body": ("--- [Konten cerita placeholder - menyusul] ---",
                   "--- [Placeholder story content - TBD] ---"),
    "story_new_badge": ("   ({} baru)", "   ({} new)"),

    # --- main story (stage-based) ---
    "ms_title": ("MAIN STORY", "MAIN STORY"),
    "ms_line": (" [{:>5}] Bab {} - {}", " [{:>5}] Chapter {} - {}"),
    "ms_status_locked": ("KUNCI", "LOCK"),
    "ms_status_read": ("baca", "read"),
    "ms_status_new": ("BARU", "NEW"),
    "ms_locked": ("[!] Terkunci. Selesaikan Stage {} dulu.",
                  "[!] Locked. Clear Stage {} first."),
    "ms_need": ("(butuh Stage {})", "(needs Stage {})"),

    # --- character story (affection-based) ---
    "cs_title": ("CHARACTER STORY - {}", "CHARACTER STORY - {}"),
    "cs_pick": ("CHARACTER STORY - PILIH KARAKTER",
                "CHARACTER STORY - PICK A CHARACTER"),
    "cs_count": ("   Affection {}  ({}/{} cerita)",
                 "   Affection {}  ({}/{} stories)"),
    "cs_line": (" [{:>5}] Cerita ke-{}   {}", " [{:>5}] Story {}   {}"),
    "cs_need": ("(Affection {})", "(Affection {})"),
    "cs_locked": ("[!] Terkunci. Affection {} / {} belum cukup.",
                  "[!] Locked. Affection {}/{} is not enough."),
    "cs_unlocked": (" >>> CERITA KARAKTER TERBUKA: {} cerita ke-{}",
                    " >>> CHARACTER STORY UNLOCKED: {} story {}"),
    "ms_unlocked": (" >>> MAIN STORY terbuka: Bab {} - {}",
                    " >>> MAIN STORY unlocked: Chapter {} - {}"),

    # --- gift / affection ---
    "affection_line": (" Affection : {}", " Affection : {}"),
    "affection_next": (" Berikutnya : cerita ke-{} butuh Affection {}",
                       " Next       : story {} needs Affection {}"),
    "char_title": ("KARAKTER - {}", "CHARACTER - {}"),
    "a_upgrade": (" [1] Upgrade Level (pakai material)", " [1] Level Up (use material)"),
    "a_gift": (" [2] Beri Gift            (punya {})", " [2] Give Gift            (have {})"),
    "a_story": (" [3] Character Story", " [3] Character Story"),
    "gave_gift": (" Gift diberikan ke {} -> Affection {} (+{})",
                  " Gift given to {} -> Affection {} (+{})"),
    "no_gift": (" [!] Gift tidak cukup. Sumber gift masih TBD (fitur gap).",
                " [!] Not enough gifts. Gift source is still TBD (feature gap)."),
    "gift_line": (" Gift            : {}", " Gift            : {}"),

    # --- shop ---
    "shop_title": ("SHOP", "SHOP"),
    "tickets_owned": (" Tiket dimiliki: {}", " Tickets owned: {}"),
    "shop_tickets": (" [1] Tiket Gacha   {} coins  (1 tiket = 1 pull)",
                     " [1] Gacha Ticket  {} coins  (1 ticket = 1 pull)"),
    "shop_material": (" [2] Material Level", " [2] Level Material"),
    "mat_shop_title": ("SHOP - MATERIAL LEVEL", "SHOP - LEVEL MATERIAL"),
    "mat_shop_note1": (" Material cuma untuk naik level karakter sendiri.",
                       " Material only levels up its own character."),
    "mat_shop_note2": (" Harga per unit beda per rarity.\n",
                       " Price per unit differs by rarity.\n"),
    "buy_qty_q": (" Berapa {} @ {} coins? (0..{}, 0 batal) > ",
                  " How many {} @ {} coins? (0..{}, 0 = back) > "),
    "mat_line": (" [{:>2}] {:<20} {:<3} {:>4} coins  punya {:>4}  [{}]",
                 " [{:>2}] {:<20} {:<3} {:>4} coins  owned {:>4}  [{}]"),
    "pick_mat": ("\n Ketik nomor material, [0] kembali",
                 "\n Type a material number, [0] back"),
    "how_many_tiket": (" Berapa tiket? (0..{}, 0 batal) > ",
                       " How many tickets? (0..{}, 0 = back) > "),
    "coins_short": ("\n[!] Coins kurang. Butuh {}, punya {}.",
                    "\n[!] Not enough coins. Need {}, you have {}."),
    "got_tickets": ("\n Dapat {} tiket gacha. Tiket sekarang: {}.",
                    "\n Got {} gacha tickets. Tickets now: {}."),
    "bought_mat": ("\n Beli {} {} -> -{} coins.",
                   "\n Bought {} {} -> -{} coins."),

    # --- topup ---
    "topup_title": ("TOPUP (simulasi, tidak ada pembayaran asli)",
                    "TOPUP (simulation, no real payment)"),
    "topup_bonus": (" + bonus {}", " + bonus {}"),
    "topup_confirm": (" Konfirmasi beli {} ({})? ketik '{}': ",
                      " Confirm buy {} ({})? type '{}': "),
    "topup_ok": ("\n Sukses! +{} gems{}. Sisa: {} gems.",
                 "\n Success! +{} gems{}. You have {} gems."),
    "topup_cancel": ("\n Topup dibatalkan.", "\n Topup cancelled."),

    # --- profil ---
    "profile_title": ("PROFIL", "PROFILE"),
    "prof_active": (" Karakter aktif : {}", " Active character : {}"),
    "prof_coll": (" Koleksi        : {}/{}", " Collection      : {}/{}"),
    "prof_pull": (" Total pull     : {}  (pity {}/{})",
                  " Total pulls    : {}  (pity {}/{})"),
    "prof_clear": (" Stage clear    : {}/{}", " Stages cleared : {}/{}"),
    "prof_wl": (" Menang / Kalah : {} / {}", " Wins / Losses  : {} / {}"),
    "prof_tickets": (" Tiket gacha    : {}", " Gacha tickets  : {}"),
    "prof_gift": (" Gift           : {}", " Gifts          : {}"),
    "prof_topup": (" Topup          : {}x (simulasi)", " Topups         : {}x (simulated)"),
    "prof_mat": ("\n Material dimiliki:", "\n Materials owned:"),
    "prof_mat_none": ("\n Belum ada material. Clear stage dulu.",
                      "\n No materials yet. Clear a stage first."),
    "not_owned": ("belum dimiliki", "not owned"),
    "prof_account": (" Akun           : {}", " Account        : {}"),

    # --- pengaturan ---
    "set_title": ("PENGATURAN", "SETTINGS"),
    "set_lang": (" [1] Bahasa        : {}", " [1] Language     : {}"),
    "set_volume": (" [2] Volume        : {}", " [2] Volume       : {}"),
    "set_stats": (" [3] Info stats    : {}", " [3] Stats info   : {}"),
    "set_debug": (" [4] Menu Debug    : {}", " [4] Debug menu   : {}"),
    "set_account": (" [5] Akun & Save", " [5] Account & Save"),
    "on": ("AKTIF", "ON"),
    "off": ("MATI", "OFF"),
    "vol_q": (" Volume (0-100, 0 batal) > ", " Volume (0-100, 0 = back) > "),
    "vol_saved": (" Volume disimpan: {}", " Volume saved: {}"),
    "lang_switched": (" Bahasa diubah ke {}", " Language switched to {}"),
    "account_title": ("AKUN & SAVE", "ACCOUNT & SAVE"),
    "acc_active": (" Akun aktif : {}", " Active account : {}"),
    "acc_file": (" File save  : {}", " Save file    : {}"),
    "acc_login": (" [1] Login / ganti akun", " [1] Login / switch account"),
    "acc_logout": (" [2] Logout", " [2] Logout"),
    "acc_reset": (" [3] Reset save akun ini", " [3] Reset this account's save"),
    "acc_logged_out": (" Logout sukses. Sesi kembali ke {}.",
                       " Logged out. Session back to {}."),
    "acc_switched": (" Sekarang login sebagai {}.", " Now logged in as {}."),
    "acc_reset_done": (" Save {} direset.", " Save for {} has been reset."),
    "acc_save_q": (" Hapus save {}? ketik 'ya': ", " Delete save {}? type 'y': "),

    # --- layar login ---
    "login_title": ("ITKOPTER - MASUK", "ITKOPTER - LOG IN"),
    "login_last": (" Akun terakhir : {}", " Last account : {}"),
    "login_guest": (" Tamu (tanpa login)", " Guest (no account)"),
    "login_new": (" Ketik nama akun baru...", " Type a new account name..."),
    "login_pick": (" Pilih akun:", " Choose account:"),
    "login_name_q": (" Nama akun (3-24 huruf/angka, 0 batal) > ",
                     " Account name (3-24 letters/digits, 0 = back) > "),
    "login_bad": (" [!] Nama tidak valid. Hanya huruf, angka, - dan _.",
                  " [!] Invalid name. Only letters, digits, - and _."),
    "login_new_created": (" Akun baru dibuat: {}", " New account created: {}"),

    # --- debug ---
    "debug_title": ("DEBUG MENU", "DEBUG MENU"),
    "d_force": (" force_next pull: {}", " force_next pull: {}"),
    "d1": (" [1] +1600 gems", " [1] +1600 gems"),
    "d2": (" [2] +5000 coins", " [2] +5000 coins"),
    "d3": (" [3] Paksa pull berikutnya jadi SSR", " [3] Force next pull to SSR"),
    "d4": (" [4] Paksa pull berikutnya jadi SR", " [4] Force next pull to SR"),
    "d5": (" [5] Set pity ke (HARD_PITY-1)", " [5] Set pity to (HARD_PITY-1)"),
    "d6": (" [6] Buka semua stage", " [6] Unlock all stages"),
    "d7": (" [7] Reset stage clear", " [7] Reset stage clears"),
    "d8": (" [8] Beri semua karakter (Rank MAX)", " [8] Give all characters (Rank MAX)"),
    "d9": (" [9] RESET SAVE (hapus semuanya)", " [9] RESET SAVE (delete everything)"),
    "dA": (" [A] +999 material semua karakter", " [A] +999 material for all characters"),
    "dB": (" [B] Naikkan semua karakter ke Lv.MAX", " [B] Level all characters to Lv.MAX"),
    "dC": (" [C] +20 tiket gacha", " [C] +20 gacha tickets"),
    "dD": (" [D] +10 gift  (sumber sementara, ekonomi TBD)", " [D] +10 gift  (temp source, economy TBD)"),
    "d_ok_gems": (" [+] Gems +1600  (sekarang {})", " [+] Gems +1600  (now {})"),
    "d_ok_coins": (" [+] Coins +5000  (sekarang {})", " [+] Coins +5000  (now {})"),
    "d_ok_force": (" [!] Pull berikutnya dipaksa jadi {}.",
                   " [!] Next pull forced to {}."),
    "d_ok_pity": (" [!] Pity diatur ke {}.", " [!] Pity set to {}."),
    "d_ok_clear": (" [+] Stage 1-{} dianggap clear.", " [+] Stages 1-{} marked clear."),
    "d_ok_reset": (" [-] Semua stage di-reset.", " [-] All stages reset."),
    "d_ok_rank": (" [+] Semua karakter Rank MAX (level tidak diubah).",
                  " [+] All characters Rank MAX (level unchanged)."),
    "d_ok_mats": (" [+] Semua material +999.", " [+] All materials +999."),
    "d_ok_level": (" [+] Semua karakter Lv.MAX (rank tidak diubah).",
                   " [+] All characters Lv.MAX (rank unchanged)."),
    "d_ok_tiket": (" [+] Tiket +20  (sekarang {})", " [+] Tickets +20  (now {})"),
    "d_ok_gift": (" [+] Gift +10  (sekarang {})", " [+] Gifts +10  (now {})"),
    "reset_q": (" Yakin? ketik '{}': ", " Sure? type '{}': "),
    "reset_done": (" Save direset.", " Save has been reset."),
}

def mat_name(cid):
    """Nama material per karakter. Indonesian: 'Serbuk X', English: 'X Shard'."""
    if _LANG == "en":
        return f"{CHAR_BY_ID[cid]['name']} Shard"
    return MAT_NAME[cid]


def species_of(c):
    return SPECIES_EN.get(c["species"], c["species"]) if _LANG == "en" else c["species"]


def stage_name(s):
    return s["name_en"] if _LANG == "en" else s["name"]


def diff_of(s):
    return DIFF_EN.get(s["diff"], s["diff"]) if _LANG == "en" else s["diff"]

def sorted_by_rarity(ids):
    """Urut id karakter: SSR dulu, lalu SR, lalu R; dalam raritas itu by name."""
    return sorted(ids, key=lambda i: (RARITY_ORDER[CHAR_BY_ID[i]["rarity"]],
                                      CHAR_BY_ID[i]["name"]))

# ----------------------------------------------------------------------------
# CERITA: MAIN STORY (stage) & CHARACTER STORY (affection)
# ----------------------------------------------------------------------------
# DUA SUMBU CERITA INI SENGAJA TIDAK DICAMPUR:
#   MAIN STORY        -> dibuka oleh stage yang sudah clear  (progression akun)
#   CHARACTER STORY   -> dibuka oleh affection per karakter  (progression karakter)
# Jangan pernah membuka salah satunya lewat jalur yang satunya lagi.

def chapter_title(ch):
    return ch["title_en"] if _LANG == "en" else ch["title"]


def main_key(ch):
    return f"m:{ch['id']}"


def char_story_key(cid, idx):
    return f"c:{cid}:{idx}"


def affection_of(st, cid):
    return st["affection"].get(cid, 0)


def main_story_open(st, ch):
    """Main Story bab ini terbuka kalau stage unlock_stage-nya sudah clear."""
    return ch["unlock_stage"] in st["cleared"]


def char_story_open(st, cid, idx):
    """Cerita karakter idx (mulai 1) terbuka kalau affection >= ambang idx."""
    if idx < 1 or idx > len(CHAR_STORY_LEVELS):
        return False
    return affection_of(st, cid) >= CHAR_STORY_LEVELS[idx - 1]
