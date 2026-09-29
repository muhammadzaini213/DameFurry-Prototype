#!/usr/bin/env python3
"""
ITKOPTER - CLI Flow Tester (shim masuk)
Top-down danmaku + gacha waifu furry (gedung / bangunan / benda mati)

Kode aslinya satu file itkopter_cli.py; sekarang sudah dipecah jadi paket
`itkopter/` per domain (config, data, state, account, ui, character, gacha,
gameplay, stages, shop, menus, debug, main). File ini cuma penjaga pintu supaya

    python3 itkopter_cli.py

dan pola lama

    import itkopter_clix ; itkopter_cli.run_pulls(...)

tetap jalan persis seperti dulu.

Dua hal yang supaya pola lama TIDAK jadi diam-diam berubah:

  * baca  -> __getattr__ meneruskan ke modul asalnya, jadi `_LANG` / `STR`
             yang berubah lewat set_lang() langsung kelihatan dari sini;
  * tulis -> __setattr__ diteruskan juga, jadi monkeypatch lama
             `itkopter_cli.roll_rarity = f` tetap mengubah perilaku do_pull().
             Module biasa mengabaikan __setattr__ level-module, makanya kelas
             `_Shim` dipasang lewat `sys.modules[__name__].__class__`.

Ini HANYA layer menu untuk ngetes alur. Gameplay diganti opsi debug WIN / LOSE.
Kalau gameplay asli sudah jadi, cukup ganti isi fungsi run_gameplay()
di itkopter/gameplay.py.
"""
import sys
import types

import itkopter.config as _config
import itkopter.data as _data
import itkopter.state as _state
import itkopter.account as _account
import itkopter.ui as _ui
import itkopter.character as _character
import itkopter.gacha as _gacha
import itkopter.gameplay as _gameplay
import itkopter.stages as _stages
import itkopter.shop as _shop
import itkopter.menus as _menus
import itkopter.debug as _debug
import itkopter.main as _main

# Urutan ini menentukan jawaban kalau ada nama sama di dua modul.
# Semua duplikat di sini adalah objek yang sama, jadi urutannya aman.
_MODULES = (_config, _data, _state, _account, _ui, _character, _gacha,
            _gameplay, _stages, _shop, _menus, _debug, _main)


class _Shim(types.ModuleType):
    def __setattr__(self, name, value):
        if name.startswith("__") and name.endswith("__"):
            super().__setattr__(name, value)
            return
        sent = False
        for _m in _MODULES:
            if name in vars(_m):
                setattr(_m, name, value)
                sent = True
        if not sent:
            super().__setattr__(name, value)


sys.modules[__name__].__class__ = _Shim


def __getattr__(name):
    """Baca dari modul asal, biar `itkopter_cli.X` selalu segar."""
    if name.startswith("__") and name.endswith("__"):
        raise AttributeError(name)
    for _m in _MODULES:
        if hasattr(_m, name):
            return getattr(_m, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted({n for _m in _MODULES for n in dir(_m)})


if __name__ == "__main__":
    _main.main()
