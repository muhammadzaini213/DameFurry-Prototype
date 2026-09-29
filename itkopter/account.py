"""
account. Save file, sesi akun, dan layar login.

Multi-save lokal tanpa server: Tamu -> itkopter_save.json,
akun bernama -> itkopter_save_<nama>.json,
itkopter_session.json menunjuk akun yang sedang jalan.
"""

import json
import os

from .config import GUEST, SAVE_FILE, SESSION_FILE
from .data import T, set_lang
from .state import normalize_state
from .ui import ask, ask_key, ask_pick, header, is_yes, line, pause

# ----------------------------------------------------------------------------
# SAVE / LOAD
# ----------------------------------------------------------------------------
def save_path(account):
    """Path file save untuk sebuah akun. Tamu -> SAVE_FILE (kompatibel save lama)."""
    if not account or account == GUEST:
        return SAVE_FILE
    # Jangan di-strip: valid_account_name mengizinkan -/_ di mana saja,
    # jadi membuangnya membuat "___" -> slot Guest dan "_abc" -> "abc"
    # (dua akun beda nama saling menimpa satu file).
    safe = "".join(ch for ch in str(account) if ch.isalnum() or ch in "-_")[:24]
    return f"itkopter_save_{safe}.json" if safe else SAVE_FILE

def backup_file(path, tag="korup"):
    """Salin file save ASLI sebelum ditimpa. Return path salinan atau None.

    tag = "korup" untuk file yang gagal dibaca, "asli" untuk file yang
    terbaca tapi isinya dirombak normalisasi. Dalam kedua kasus ini file
    aslinya akan tertimpa save berikutnya, jadi salinannya satu-satunya
    sisa data lama yang bisa diperbaiki manual.
    """
    try:
        if not os.path.exists(path):
            return None
        base, ext = os.path.splitext(path)
        dst = f"{base}.{tag}{ext}"
        n = 1
        while os.path.exists(dst):
            n += 1
            dst = f"{base}.{tag}{n}{ext}"
        with open(path, "rb") as f:
            blob = f.read()
        with open(dst, "wb") as f:
            f.write(blob)
        return dst
    except OSError:
        return None


def _isi_berubah(data, st):
    """True kalau normalisasi membuang / menambah / mengubah isi save yang tadi terbaca.

    Penambahan harus ikut dihitung: save lama yang belum punya key baru
    (mis. sebelum fitur gift/settings) tidak diubah nilainya, tapi bytes
    file aslinya tetap hilang begitu save berikutnya menulis key tambahan
    itu -- jadi salinannya tetap dibuat.
    """
    if set(data) - set(st) or set(st) - set(data):
        return True
    for k, v in data.items():
        try:
            if json.dumps(v, sort_keys=True) != json.dumps(st.get(k), sort_keys=True):
                return True
        except (TypeError, ValueError):
            return True
    return False


def load_state(path, account=None):
    """Baca save. File tidak ada -> state baru. Rusak -> backup + state baru.

    Dua tahap dipisah supaya kerusakan format (JSON/encoding) tidak
    bercampur dengan kerusakan isi; keduanya sama-sama dibackup dulu
    supaya data asli tidak hilang permanen.
    """
    if not os.path.exists(path):
        return normalize_state({}, account)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)   # ValueError mencakup JSONDecodeError
                                 # dan UnicodeDecodeError (file non-UTF-8)
        if not isinstance(data, dict):
            raise ValueError("bukan object JSON")
    except (OSError, ValueError):
        _report_corrupt(path, "korup")
        return normalize_state({}, account)
    try:
        st = normalize_state(data, account)
    except Exception:
        # Isi save tidak baca (salah tipe di mana pun) -> rusak total.
        _report_corrupt(path, "korup")
        return normalize_state({}, account)
    if _isi_berubah(data, st):
        # Normalisasi membuang/mengubah isi (mis. rank berbentuk string).
        # File asli tetap disimpan dulu sebelum save berikutnya menimpanya.
        bk = backup_file(path, "asli")
        if bk:
            print(T("save_backup", bk))
    return st


def _report_corrupt(path, tag):
    bk = backup_file(path, tag)
    print(T("save_corrupt"))
    if bk:
        print(T("save_backup", bk))


def save_state(st):
    path = save_path(st.get("account"))
    tmp = path + ".tmp"
    try:
        # Tulis ke .tmp lalu os.replace: kalau proses mati di tengah,
        # file save lama tetap utuh, bukan terpotong setengah.
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(st, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except (OSError, TypeError, ValueError) as e:
        print(T("save_fail", e))
        try:
            os.remove(tmp)
        except OSError:
            pass
    write_session(st.get("account"), st.get("lang", "id"))


# --- sesi akun (akun mana yang sedang dipakai) ---
def read_session():
    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def write_session(account, lang):
    tmp = SESSION_FILE + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"account": account or "", "lang": lang or "id"},
                      f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, SESSION_FILE)
    except OSError:
        try:
            os.remove(tmp)
        except OSError:
            pass


def list_accounts():
    """Nama akun tersimpan (file itkopter_save_<nama>.json), tanpa slot Tamu."""
    out = []
    try:
        for fn in sorted(os.listdir(".")):
            if fn.startswith("itkopter_save_") and fn.endswith(".json"):
                nm = fn[len("itkopter_save_"):-len(".json")]
                if nm:
                    out.append(nm)
    except OSError:
        pass
    return out


def valid_account_name(name):
    if not (3 <= len(name) <= 24):
        return False
    return all(ch.isalnum() or ch in "-_" for ch in name)


def login_gate():
    """
    Layar pilih akun. Return nama akun, atau None kalau pemain memilih keluar.
    """
    sess = read_session()
    set_lang(sess.get("lang"))
    last = sess.get("account") or GUEST
    names = list_accounts()
    while True:
        print()
        line()
        print(" " + T("login_title"))
        line()
        print(T("login_last", last))
        print(T("login_pick"))
        print(f" [1] {T('login_guest')}")
        for i, n in enumerate(names, 2):
            print(f" [{i}] {n}")
        print(f" [{len(names) + 2}] {T('login_new')}")
        print(T("m_exit"))
        n = ask_pick("> ", 0, len(names) + 2)
        if n == 0:
            return None
        if n == 1:
            return GUEST
        if n == len(names) + 2:
            name = ask(T("login_name_q"))
            if name == "0":
                continue
            if not valid_account_name(name):
                print(T("login_bad"))
                pause()
                continue
            if name == GUEST:
                # Slot Tamu sudah ada; jangan bilang "akun dibuat".
                return GUEST
            if name not in names:
                print(T("login_new_created", name))
                pause()
            return name
        return names[n - 2]


def open_session():
    """
    Buka sesi: baca akun aktif dari session file; kalau belum ada, layar login.
    Return state, atau None kalau pemain keluar dari layar login.
    """
    acct = read_session().get("account") or None
    if not acct:
        acct = login_gate()
        if acct is None:
            return None
    st = load_state(save_path(acct), acct)
    write_session(st["account"], st["lang"])
    return st

def account_menu(st):
    while True:
        header(T("account_title"), st)
        print(T("acc_active", st["account"] or GUEST))
        print(T("acc_file", save_path(st["account"])))
        print()
        print(T("acc_login"))
        print(T("acc_logout"))
        print(T("acc_reset"))
        print(T("back"))
        c = ask_key({"0", "1", "2", "3"})
        if c == "0":
            return
        elif c == "1":
            login_gate_into(st)
        elif c == "2":
            logout(st)
            return
        elif c == "3":
            acct = st["account"]
            if is_yes(ask(T("acc_save_q", acct or GUEST))):
                p = save_path(acct)
                if os.path.exists(p):
                    os.remove(p)
                st.clear()
                st.update(normalize_state({}, acct))
                print(T("acc_reset_done", acct or GUEST))
                save_state(st)
            pause()
            return


def login_gate_into(st):
    """Ganti akun di tengah sesi: simpan yang lama, muat yang baru ke dict st."""
    name = login_gate()
    if name is None:
        return
    save_state(st)
    st.clear()
    st.update(load_state(save_path(name), name))
    save_state(st)
    print(T("acc_switched", st["account"]))
    pause()


def logout(st):
    """
    Simpan akun sekarang, bersihkan sesi, lalu tampilkan layar login lagi.
    Kalau pemain batal di layar login, sesi tetap dibersihkan dan aplikasi
    keluar -- jangan dipanggil save_state() lagi setelah ini (lihat main()).
    """
    save_state(st)
    prev = st["account"] or GUEST
    write_session(None, st.get("lang", "id"))
    name = login_gate()
    if name is None:
        st["force_quit"] = True
        return
    st.clear()
    st.update(load_state(save_path(name), name))
    save_state(st)
    print(T("acc_logged_out", prev))
    print(T("acc_switched", st["account"]))
    pause()
