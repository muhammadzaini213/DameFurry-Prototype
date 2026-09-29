# AGENTS.md

ITKOPTER — CLI flow prototype for a top-down danmaku gacha. The program is a stdlib-only package `itkopter/` (13 modules, ~1800 lines) plus an 86-line compatibility shim `itkopter_cli.py`: no deps, no build, no package manager, no tests, no lint, no typecheck. Player-facing text is **bilingual** (Indonesian + English, see *i18n* below); comments and docstrings are Indonesian. See *Package layout* below for which module owns what — it was split out of one file by verbatim line-slice, and behaviour is identical, so every invariant below still names functions without saying where they live.

## Running

- `python3 itkopter_cli.py` from this directory (the shim). `python3 -m itkopter.main` also works. **`python3 itkopter/main.py` does NOT** — the package uses relative imports (`from .config import ...`), so running a module inside the package by path fails; use one of the two forms above.
- **No test / lint / typecheck / build command exists.** Verification is manual play-through, or drive the pure functions from a REPL (see below).
- Smoke test without a TTY: `printf '0\n' | python3 itkopter_cli.py` — prints the main menu and exits 0. This is the only scripted check that works as-is. **It only goes straight to the menu if `itkopter_session.json` already exists**; with no session file the run stops at the login gate instead (also exit 0, different output). Both are correct.
- Importing creates `__pycache__/` next to the sources. It is disposable build output — delete it freely, it is not a source file.

## The `run_gameplay()` seam is the point of the game

`run_gameplay(stage, char_id)` in **`itkopter/gameplay.py`** is a deliberate placeholder: it prints the stage and offers a manual WIN / LOSE / abort prompt. **Return contract — `True` = win, `False` = loss, `None` = cancel/abort.** `stage_menu` (in `itkopter/stages.py`) treats `None` as "back to the stage list with no reward" and both bools as a real run through `show_result()`. Swap this function (and only this function) when the real gameplay lands; nothing else in the package knows it is a stub. Keep the 3-value return, not just win/lose, or cancelling will pay out a loss reward (`LOSE_COINS`).

## Package layout — one module per domain

The package used to be one file; it was split by **verbatim line-slice**, so the code in each module is unchanged text with an import header added. Import rule — a module may only import from a level *above* it (never sideways, never down):

```text
L0   config
L1   data
L2   ui            state
L3   account
L4   gameplay      character
L5   gacha         stages      shop      debug      menus
L6   main
```

(Every arrow points up: `main` sits on `gacha/stages/shop/debug/menus/character/account`; `character` sits on `account/ui/data/config`; `data` sits on `config`; nothing sits on `main`.)

| Module | Owns |
|---|---|
| `config` | every balance/tuning constant: `GEM_PER_PULL`, `RATES`, `HARD_PITY_SSR`, `MAX_*`, `LEVEL_COST_*`, `SHOP_MAT_PRICE`, `TOPUP_PACKS`, plus `SAVE_FILE`/`SESSION_FILE`/`GUEST`, `LOSE_COINS`, `CHAR_STORY_LEVELS`/`GIFT_AFFECTION`/`START_GIFTS`, `RARITY_ORDER`/`RARITY_STAR` |
| `data` | `CHARACTERS`, `STAGES`, `MAIN_STORY`, `SPECIES_EN`/`DIFF_EN`, the whole i18n layer (`STR`, `T`, `set_lang`, `_LANG`), the name helpers (`mat_name`/`species_of`/`stage_name`/`diff_of`/`chapter_title`), `sorted_by_rarity`, and the story predicates (`affection_of`, `main_story_open`, `char_story_open`, `main_key`, `char_story_key`) |
| `state` | `new_state()` (the one definition of the save schema) and `normalize_state()` |
| `account` | `save_path`, load/save, session file, `login_gate`, `open_session`, `account_menu`, `login_gate_into`, `logout` |
| `ui` | screen primitives only: `line`, `header`, `ask`, `pause`, `ask_int`, `onoff`, `fmt_idr` — deliberately **below** the domain modules so a domain menu can print without importing `menus` and creating a cycle |
| `character` | `fmt_char`, `level_cost`, `char_stats`, `char_power`, `sorted_owned`, `collection_menu`, `character_menu`, `upgrade_char`, `give_gift`, `char_story_menu` |
| `gacha` | `roll_rarity`, `do_pull`, `run_pulls`, `print_results`, `pay_and_pull`, `gacha_menu` |
| `gameplay` | `run_gameplay()` — the seam, nothing else |
| `stages` | `stage_menu`, `show_result`, `grant_drops` |
| `shop` | `shop_menu`, `buy_tickets`, `shop_material_menu`, `topup_menu` |
| `menus` | `profile_menu`, `settings_menu`, `story_menu`, `main_story_menu`, `char_story_pick_menu` |
| `debug` | `debug_menu` and its actions |
| `main` | `main()` + the dispatch loop |

Two placements that look odd but are load-bearing:

- **`sorted_by_rarity` lives in `data`, not `character`** — `normalize_state()` needs it, and `state` is below `character`. `sorted_owned(st)` (the one that reads a save) stays in `character`.
- **`char_story_menu` lives in `character`, not `menus`** — `character_menu` calls it, and `menus` imports `character` for `fmt_char`. The reverse direction would be a cycle. `char_story_pick_menu` (the character *picker*) stays in `menus`.

`itkopter_cli.py` is now an 86-line shim. It exists only so `python3 itkopter_cli.py` and `import itkopter_cli` keep working: a `__getattr__` forwards reads to the owning module, and a `_Shim` module class (installed via `sys.modules[__name__].__class__`) forwards **writes** too, so `itkopter_cli.roll_rarity = f` still changes what `do_pull()` calls. Adding a name to the shim is never needed — `__getattr__` searches all thirteen modules.

## Flow map — the loop the file is built around

```text
Login/Guest → Main Menu → Gacha/Prep → Stage → run_gameplay() → Reward
            → Upgrade/Progression → Next Stage / Replay / Gacha / Story
```

Main menu: `1` Mission, `2` Gacha, `3` Collection, `4` Profile, `5` Shop, `6` Topup, `7` Settings, **`8` Story**, `9` Debug (hidden by `hide_debug`), `0` Exit.

Flow glue that exists so the player is never stranded (do not remove without replacing):

- **`hint_first` / `hint_pick`** are printed in `main()` when `owned` is empty / `active` is None — the only onboarding there is. No tutorial system exists and none is planned. `hint_pick` is easy to assume unreachable, because `normalize_state()` repairs a `None`/stale `active` to the first owned character whenever `owned` is non-empty, and both `do_pull()` and debug `[8]` set `active` when it is `None`. The one live path is debug **`[B]`**, which fills `owned` *without* touching `active` (scenario `50_debug_misc`). Don't "tidy up" the branch without finding another path.
- **`pay_and_pull()`** diffs `st["owned"]` before/after and, if a *new* character appeared, offers `gacha_open_coll` to jump straight into `collection_menu()`. Pulls no longer dead-end in the gacha menu.
- **`collection_menu()`** does *not* act on a pick directly: choosing a number opens a two-item sub-menu — `[1]` Buka hub karakter (→ `character_menu()`, unit untouched) and `[2]` Jadikan unit (sets `st["active"]`, saves, prints `active_now`). Picking alone never changes the unit; `[0]` backs out of the sub-menu with nothing done.
- **`show_result()`** after a win prints `ms_unlocked` (Main Story) and `hint_after_reward` — reward is never the last screen.
- **`normalize_state()`** repairs `active`: if `owned` is non-empty but `active` isn't a member, it picks the first owned character; if `owned` is empty it forces `None`. Without this, a broken save makes `stage_menu` refuse with "no active unit" while the collection is non-empty — a hard dead end.


## Gacha invariants that are easy to break

- `RATES` is walked cumulatively in the order SSR, SR, R with `result` defaulting to `"R"`. **If the rates don't sum to 1.0 the leftover is silently folded into R** — lowering SSR's rate without renormalizing hands the difference to R rather than rescaling SR. Current values sum to exactly 1.0.
- Hard pity is `if st["pity"] + 1 >= HARD_PITY_SSR` inside `roll_rarity`, where `pity` counts pulls since the last SSR. At `pity == HARD_PITY_SSR - 1` the next pull is forced SSR. `do_pull` resets `pity` to 0 on SSR, otherwise `+= 1`.
- The 10-pull guarantee is **not a re-roll**: `run_pulls()` only passes `min_rarity` on the 10th slot, and only when slots 1–9 contain no SSR/SR. It floors that one pull's rarity (`RARITY_ORDER[result] > RARITY_ORDER[min_rarity]` → upgrade) and never re-rolls or redistributes. Verified: 9 forced R's then SR. If `TENPULL_GUARANTEE` is changed, `RARITY_ORDER` must gain the matching key or you get a `KeyError`. Note `run_pulls(st, 1)` passes `min_rarity=None` — the guarantee is `n == 10 and i == 9`, so a single pull never gets floored.
- **Pulls have two payment paths but one code path.** `pay_and_pull(st, n)` asks gems-or-ticket and then calls `run_pulls()`; tickets cost `n` tickets for an `n`-pull (no gems). `run_pulls()` is what mutates pity/rank/coins, so a ticket pull still counts toward `total_pulls` and `pity`. Anything that changes gacha behaviour belongs in `run_pulls`/`do_pull`, not in the payment branch.
- `DUPE_COIN_REFUND` is indexed by rarity, so it must contain a key for **every** rarity present in `CHARACTERS` or a max-rank duplicate raises `KeyError`. A new rarity means editing `RATES`, `CHAR_BY_ID`-consuming maps, `RARITY_ORDER`, `RARITY_STAR`, and `DUPE_COIN_REFUND` together.
- Debug `force_next` is a field of `new_state()`, so it is **persisted to the save file and survives restarts** — a leftover forced rarity silently fires on your next session. Also note a debug-forced SR still does `pity += 1` in `do_pull`, so force-pull while testing pity and you burn pity slots.

## Stage list invariants

- `STAGES[n - 1]` selects by **list position**, but the menu prints `s["id"]` and `show_result` / unlock logic key off `id`. Today the two coincide (ids are exactly `1..len(STAGES)` in order). Inserting a stage in the middle, or using a non-contiguous `id`, silently selects/plays the wrong stage and breaks sequential unlock.
- Unlock is purely sequential: `s["id"] == 1 or (s["id"] - 1) in st["cleared"]`. No branching or star-gating exists.
- First-clear bonus keys off `stage["id"] not in st["cleared"]`; replays pay base rewards only.
- **Each stage line is followed by an indented `Drop:` preview** built from `s["drops"]`, with `(belum dimiliki)` / `(not owned yet)` (`drop_unowned`) appended per material you don't own. It is display-only — nothing there touches `st["mats"]`. It renders even for locked stages (deliberate: it's the farming preview).

## Story — TWO TRACKS, NEVER CROSS-WIRED

There are two independent story systems with different unlock sources. **This is the single most important thing not to break.**

| | Unlock source | Data | Key in `read_story` |
|---|---|---|---|
| **Main Story** | `stage["id"] in st["cleared"]` | `MAIN_STORY` (`unlock_stage`) | `"m:<id>"` |
| **Character Story** | `st["affection"][cid] >= threshold` | `CHAR_STORY_LEVELS` (`[1,2,3]`) | `"c:<cid>:<idx>"` |

```text
ACCOUNT / STAGE PROGRESSION        CHARACTER PROGRESSION
  Stage  ──► Main Story               Gift ──► Affection ──► Character Story
```

- `main_story_open(st, ch)` reads **only** `st["cleared"]`. `char_story_open(st, cid, idx)` reads **only** `st["affection"][cid]`. Neither ever consults the other's field — a stage clear must never bump affection, and a gift must never open a Main Story chapter.
- Affection is **per character** (`st["affection"] = {cid: int}`), never global. Thresholds ascend, so story N is open iff affection ≥ `CHAR_STORY_LEVELS[N-1]`. Unlock is *derived*, not stored — there is no separate "unlocked" flag to get stale.
- `MAIN_STORY` is deliberately sparse: only stages 1, 3 and 6 open a chapter. Do not add a chapter per stage.
- `st["read_story"]` is only for the `BARU`/`baca` marker; it is **not** part of any unlock condition.
- Story bodies are the `story_body` placeholder string. Writing real prose is a future feature.

## Affection & Gift

Flow: `character_menu()` → `[2] Beri Gift` → `give_gift()` → affection `+= GIFT_AFFECTION` (1) → prints `cs_unlocked` for any threshold just crossed → `char_story_menu()`.

- `st["gifts"]` is a plain inventory counter, consumed one per gift.
- **Gift source = TBD / feature gap.** The only way to get a gift today is debug `[D]` (+10), which exists purely so the flow is testable. Do **not** quietly add gifts to the Shop or to stage drops — that is an economy decision that hasn't been made. See *Feature gaps* in the hand-off report.
- The yes/no answer for gift/upgrade prompts goes through **`is_yes()` in `ui.py`**, which accepts `ya`, `y` or `yes` in either language, case-insensitive. `T("yes_word")` is only the *hint printed in the prompt*. Before this, the code compared `.lower() == T("yes_word")` exactly, so typing `y` in Indonesian mode silently cancelled. Anything that is not `is_yes()` still counts as "no" — there is no re-prompt, so piped tests must still send an explicit yes or the flow drifts.


## Save file

- `SAVE_FILE = "itkopter_save.json"` is a **relative path resolved against the current working directory, not the script directory**. Running the script from anywhere else creates a second, independent save with fresh gems. Always run it from this directory.
- The save is disposable — delete the file to reset (or use debug menu `[9]`, which requires typing `ya`).
- `load_state()` normalizes through `normalize_state()`, so schema evolution is backward-compatible. It never raises: a file that fails to read (bad JSON, **non-UTF-8**, not an object) is reported as "[!] Save korup" and copied to `*.korup.json` first; a file that reads fine but gets reshaped by `normalize_state()` — wrong types, out-of-range values, **or simply missing fields that `normalize_state()` fills in** — is copied to `*.asli.json` with no error message. In both cases the original bytes survive, because the next `save_state()` would otherwise overwrite them permanently. The missing-field case is checked by `_isi_berubah()` comparing the two key *sets*, not just values: a pre-settings save's values are all intact, so a value-only diff returns `False` and the original bytes would be gone forever. (This gap is how the real `itkopter_save_niga_niga.json` lost its original 429 bytes — values all survived, five defaulted fields were added.)
- `save_state()` / `write_session()` are **atomic**: they write `*.tmp`, `fsync`, then `os.replace()` onto the real path. A crash mid-write truncates the temp file, never the live save. Also catches `TypeError`/`ValueError`, so a non-serialisable state reports `[!] Gagal simpan` instead of dying.
- Reads and writes are explicit `encoding="utf-8"` with `ensure_ascii=False` — the UI emits `★` and `✓`, so a non-UTF-8 terminal will mangle them.
- **Never run a scripted test that mutates state against this directory's save.** `save_state()` is called after each mutating menu action and on exit — **and also from inside `show_result()`, `give_gift()` and `pay_and_pull()`**, so even a "pure function" scenario test that calls them will overwrite `itkopter_save.json` if its CWD is this directory. That has already bitten twice. The plain exit smoke test above is safe for values — and, with the `_isi_berubah()` key-set check above, an old save it loads now leaves an `*.asli.json` copy too. **Never run the P0 regression script (`check.py`) from this directory**: its own docstring says "jalankan dari temp dir", but it writes scratch saves (`s1..s4`, `k1`, `a1`), an `itkopter_save_a.json`, and `write_session("a")` — i.e. it points `itkopter_session.json` at a fake account. It has done so twice. For anything else, `cd` into a fresh temp dir holding a copy of `itkopter_cli.py` **and the whole `itkopter/` package** and let it build its own save. (`cp itkopter_cli.py "$d" && cp -r itkopter "$d"` — a bare copy of the shim is now an immediate ImportError.) If it does happen, recovery means a copy you took beforehand: `load_state()` only writes `*.korup.json` / `*.asli.json` when it detects a damaged, reshaped or key-incomplete file — never for a healthy *current* save that got overwritten without first being loaded.

## i18n — every UI string lives in `STR`

`_LANG` is a module global (default `"id"`), set by `set_lang()`; `T(key, *args)` looks up `STR[key][_LANG]` and `.format(*args)`s it. `STR` has 203 keys.

- `STR` values are `(indonesian, english)` tuples indexed by `LANGS.index(lang)`. **A new UI string must add a key with both languages.** A missing key does **not** raise: `T()` falls back to `STR.get(key)` and returns the raw key string, so the typo shows up on screen as literally `some_key` instead of crashing. Check for stray keys with `T() terpakai == len(STR)` (both are 203 today).
- **Never print a raw literal in player-facing code.** Every `print()` of user-visible text, every `header()`, every `ask()` prompt goes through `T()`. Comments and docstrings stay Indonesian-only and get no `STR` key.
- Interpolated strings take positional args (`T("acc_switched", name)`); both halves must carry the same `{}` placeholders — a mismatch only explodes in one language.
- `_LANG` is re-read on every `T()` call, so switching language takes effect immediately with no restart; the choice is stored in `st["lang"]` (persisted in the save) and mirrored into `itkopter_session.json`.
- English-only extras not present in the ID strings: `SPECIES_EN`, `DIFF_EN`, `STAGES[].name_en` (looked up by `species_of()`, `diff_of()`, `stage_name()`); `mat_name(cid)` maps to `"<MAT_NAME[cid]> Shard"` in EN.

## Settings, language and local accounts

Main menu `[7]` opens `settings_menu()`:

| # | Item | Notes |
|---|------|-------|
| 1 | Language | toggles `id` ↔ `en`, saves immediately |
| 2 | Volume | `st["volume"]`, **placeholder only — nothing consumes it, no audio exists**. `0` is a legal value and is saved; it used to be swallowed as "cancel" |
| 3 | Info stats | `st["show_stats"]`, gates the `Lv/R/ATK/DEF/HP/Pow` tail in the collection list |
| 4 | Menu Debug | `st["hide_debug"]`, removes `[9] Debug` from the main menu. While hidden, `9` is *not* in the main menu's valid key set, so typing it prints one `[!]` line instead of silently redrawing |
| 5 | Akun & Save | `account_menu()` |

Accounts are **local multi-save, no server**:

- `GUEST = "Tamu"` → `itkopter_save.json` (the legacy `SAVE_FILE`). Named accounts → `itkopter_save_<name>.json`, built by `save_path(name)`. **`save_path` must be the identity on every name `valid_account_name()` accepts** — it filters to alnum/`-`/`_` (already guaranteed) and truncates to 24 (already guaranteed), and used to `strip("-_")`, which made `___` fall into the Guest file and `_abc` collide with `abc`. Two different accounts silently sharing one file is the failure mode to guard against; add a name to the round-trip assertion if you touch either function.
- `itkopter_session.json` = `{"account", "lang"}` points at the running account. Missing/empty file → login gate; present → **the gate is skipped and the session resumes**, so an ordinary restart never shows it. Clearing `account` (leaving the file) is what forces the gate back next launch.
- `login_gate()` returns an account name, or `None` on `[0]`. Names are 3–24 chars of alnum plus `-`/`_` (`valid_account_name()`). Typing `Tamu` at the "new account" prompt returns the Guest slot **without** printing the "account created" line — it is not a new account.
- **`logout()` must not be followed by `save_state()`.** It saves the current account first, then clears the session, then shows the gate. Cancelling the gate sets `st["force_quit"] = True`, and `main()` prints bye **without** saving. Saving there would rewrite the session (cancelling the logout) and, with `st["account"]` no longer matching a live file, spill one account's data into another's save. Keep the flag path save-free.
- Switching accounts does `st.clear()` + `st.update(load_state(...))`, so nothing from the previous account leaks forward. Verified: hero99 at 4800 gems → Tamu still 3200.

## Testing / automation notes

- **Importing the module has no side effects** (`main()` is under `__main__`), so `import itkopter_cli` then calling `new_state()`, `roll_rarity()`, `do_pull()`, `run_pulls()`, `show_result()` directly is the only sane way to test anything. `run_pulls(st, n)` is the one that exercises pity/dupe/guarantee without touching payment. Menu functions are `while True` + `input()` and cannot be driven directly.
- `ask()` swallows `EOFError`/`KeyboardInterrupt` and **returns `"0"`**, which means "back / exit" in every menu. A piped or non-tty stdin will therefore always land on exit rather than erroring — don't mistake that for a passing test.
- **Piped-input tests are a line-counting exercise**: every menu prompt, every `pause()` ("[Enter untuk lanjut]"), and every nested `ask()` consumes exactly one line, and reaching a nested menu means the outer menu's line was consumed by `return` instead of the prompt you expected. When a scripted run seems to "skip" a menu, the input drifted — write the expected line sequence out explicitly rather than debugging the code. Testing one menu at a time in a fresh temp dir (with a copy of `itkopter_cli.py` **plus the `itkopter/` package**, and its own save) is far less confusing than driving the whole session.
- `random` is used as the global module, so there is no seed hook. For deterministic pulls in a test, call `random.seed(...)` yourself or monkeypatch `itkopter_cli.random.random`.
- `import itkopter_cli` still exposes every function (the shim's `__getattr__` searches all thirteen modules), so the old test style keeps working unchanged. To replace a function, assign through the shim (`itkopter_cli.roll_rarity = f`) — `_Shim.__setattr__` forwards the write to the owning module, which is what makes `do_pull()` actually call it. Patching `itkopter.gacha.roll_rarity` directly is equally valid.
- **No menu reprints on invalid input.** Every menu prompt goes through `ask_pick(prompt, lo, hi)` or `ask_key(valid)` in `ui.py`: bad input prints **one** `[!] Input tidak valid.` line and re-asks at the same screen, instead of redrawing header + options and erasing the history above. The old pattern was `if n is None: print(T("invalid")); continue`. Both helpers carry an invariant you must preserve: **`ask_pick` needs `lo == 0` and `ask_key` needs `"0" in valid`**, because `ask()` returns `"0"` on EOF — without that the loop spins forever on an exhausted stdin. Keep `T("invalid")` *only* inside those two helpers (grep proves it: the only occurrences left are `ui.py:57` and `ui.py:71`).
- **Four regression passes exist, all against a copy of the code in a fresh temp dir** (never this directory), driven by `drive.sh <label> <codedir> <outdir>` with one `scenarios/*.stdin` per case: (1) *the package split* — 47 stdin scenarios, pre-split file vs package, byte-identical stdout/stderr/exit/save/session in all 47; (2) *the bug-fix batch* — the same 50 scenarios (47 plus volume-0, debug-keeps-level, login-as-Guest), pre-fix vs post-fix; (3) *the P3 batch* — **53 scenarios**, pre-P3 vs post-P3. Passes 2 and 3 are **expected** to differ; each was reviewed opcode by opcode. Pass 2: the only removals are the three symptoms being fixed (`[!] Input tidak valid.` for volume 0, `Akun baru dibuat: Tamu`, and the old reset of `lvl`), and the only save changes are those two scenarios. Pass 3: the removals are only the old `pick_active` wording, the `Aktif:` line a pick used to emit, and menu redraws after invalid input; the additions are only the new pick-action sub-menu, the `Drop:` previews and the `(belum dimiliki)` markers, plus one new `[!]` in `30_debug_dup_refund` (the gacha menu used to swallow bad keys in silence). The only save changes are `09_upgrade_levels`, `16_story_char_affection` and `17_story_char_locked`, all because picking a character no longer overwrites `st["active"]`. Seven older scenarios gained one input line (the new sub-menu); `52_collection_hub_vs_unit` is new and proves hub-does-not-change-unit vs `[2]`-does. In every pass all exit codes stay 0. 201 of the 203 `T()` keys appear somewhere in pass 3's combined output; the two missing are `mat_drop_none` (unreachable — see *drops*) and `save_fail` (only on a write error). Reproduce with `random.seed(20260928)` + `PYTHONHASHSEED=0`. Pass 4 is the *pilot→unit* terminology rename plus the `_isi_berubah()` key-set fix: **53 scenarios, byte-identical to pass 3 once the word is normalised** — every differing line in every `out.txt` contains `pilot`/`unit`, no `save`/`session`/`exit`/`files.txt` changed, all exits 0. (Two lines looked suspicious, `19_shop_material` and `46_shop_mat_qty0`; they only carry the pre-existing phrase `Harga per unit beda per rarity`, so a naive `unit`→`gold` normaliser false-positives on them.)
- **`show_result` grants drops for every id in `stage["drops"]`, whether or not you own that character** (`grant_drops` only checks `CHAR_BY_ID`). Consequently the `mat_drop_none` branch is unreachable with the current data — every stage has 3–4 drops. Don't write a test expecting `mat_drop_none`, and don't assume drops imply ownership. The `(belum dimiliki)` marker on the result screen is a **display hint only**; ownership is never an input to `grant_drops`.

## Conventions

- Comments and docstrings are **Indonesian**; player-facing strings are Indonesian (default) with an English twin — see *i18n* above.
- The tuning surface for balance testing now lives in `itkopter/config.py` (economy, pity, level costs, shop, topup) and `itkopter/data.py` (`CHARACTERS`, `STAGES`, `MAIN_STORY`) — `GEM_PER_PULL`, `START_GEMS`, `RATES`, `HARD_PITY_SSR`, `TENPULL_GUARANTEE`, `MAX_RANK`, `DUPE_COIN_REFUND`, `MAX_LEVEL`, `LEVEL_COST_*`, `CHARACTERS`, `STAGES`, `TICKET_PRICE`, `SHOP_MAT_PRICE`, `TOPUP_PACKS`. `CHAR_BY_ID` and `MAT_NAME` are derived; don't hand-edit them.
- `CHARACTERS[].role` is a placeholder string for the future bullet pattern / ship type, not implemented behaviour. Debug menu also has `[A]` +999 material, `[B]` level everything to `MAX_LEVEL`, `[C]` +20 tickets, and **`[D]` +10 gift** (the only gift source while the economy source is TBD), for exercising the shop/upgrade/affection UI without grinding. Every action prints a `[+]`/`[!]` confirmation line — it used to return to the menu in silence, which made it look like the key had been ignored. **`[8]` sets rank only**; it used to overwrite the whole entry with `{"rank": MAX, "lvl": 1}` and silently wipe upgrades.
- `save_state(st)` is called after each mutating menu action, and again on exit. Writes are atomic (`*.tmp` + `os.replace`).

## Level / rank are two separate axes — don't merge them

`owned[cid]` is `{"rank": 1..MAX_RANK, "lvl": 1..MAX_LEVEL}`, and they come from different sources:

- **rank** only rises from gacha dupes (`do_pull`). Grants `RANK_BUFF` (a flat +10% to *all* stats per rank above 1). Max-rank dupes pay `DUPE_COIN_REFUND` coins instead.
- **lvl** only rises from materials (from stage drops *or* bought in the Shop). Adds flat `STAT_PER_LEVEL` to all three stats. Never touched by gacha.

Both are display-only right now: `char_stats()` / `char_power()` exist so the collection list and profile have something to show, but nothing consumes the numbers yet because `run_gameplay()` is still a stub. When the real gameplay lands, these are the hooks.

- **Material is character-specific**: `mats` is keyed by *character* id, and a material only ever levels its own character. `STAGES[].drops` is `{char_id: amount}`, so adding a character means giving it a stage that drops its material, or it can never be leveled. All 16 current characters are covered by `STAGES[0..5].drops` — if you add a character, keep that invariant true or it is unlevelable.
- Drops happen on **win only** (`grant_drops` is called from the `win` branch of `show_result`). Losing pays `LOSE_COINS` and dropping the stage grants nothing — same as cancelling. Drops are **not** first-clear gated, only `first_bonus` is.
- Upgrading lives in `character_menu()` (reached *from* `collection_menu` by picking a character and answering `[1] Buka hub karakter`), via `upgrade_char()`. **Opening the hub does not touch `st["active"]`** — only the separate `[2] Jadikan unit` choice does, so you can upgrade / gift / read story for any owned character without swapping units first (this used to be automatic and was the most surprising thing in the old collection flow). The loop keeps going while `is_yes()` holds, and stops at `MAX_LEVEL` or insufficient material.

## Save schema migration

`owned` changed from `id -> int` (rank) to `id -> {"rank", "lvl"}`, so **`load_state()` no longer just merges over `new_state()`** — it goes through `normalize_state(data)`, which:
- converts a legacy `int` rank to `{"rank": n, "lvl": 1}`,
- fills in missing `rank`/`lvl` keys,
- **drops ids no longer present in `CHARACTERS`** from both `owned` and `mats`, so deleting a character from the roster doesn't make a stale save raise `KeyError` everywhere,
- coerces **every numeric field** (`gems`, `coins`, `pity`, `total_pulls`, `wins`, `losses`, `tickets`, `topups`, `gifts`, `volume`) to a non-negative int, falling back to `0` for earned values and to the `new_state()` default for settings — so `"gems": null` becomes `0`, never `None` and never a windfall;
- **clamps `rank` to `1..MAX_RANK` and `lvl` to `1..MAX_LEVEL`**, and skips non-dict `owned` entries, so a hand-edited `rank: 0` / `lvl: 999` / `owned: {"monas": "x"}` cannot reach the UI;
- **rejects an unknown `force_next`** (anything outside `None`/`R`/`SR`/`SSR`) — a stray `"XX"` in the save would otherwise survive normalisation and make `random.choice([])` raise `IndexError` on the next pull;
- tolerates non-dict `owned`/`mats`/`affection`, non-list `read_story` and a non-string `active`, and accepts a non-dict root (`data` that is a list, etc.);
- **fills in the settings fields** (`account`, `lang`, `volume`, `show_stats`, `hide_debug`) when absent — a save written before the settings feature loads with `Tamu`/`id`/70/`True`/`False` and no data loss,
- **fills in the story fields** (`gifts`, `affection`, `read_story`) the same way, dropping affection entries whose character id no longer exists and non-string entries from `read_story`.

Verified: the pre-existing `itkopter_save.json` (v1, `owned` as ints) loads with ranks and gems/pity intact. Any new code that reads `st["owned"][cid]` must go through `normalize_state` first — if you add a field to `new_state()` and want it normalized, add it to `normalize_state()` too; merging in `load_state` alone will not sanitize it.

## Shop & topup

- **The shop sells only two things: tickets and materials. Never characters.** Main menu `[5]` Shop, `[6]` Topup. Do not add a "buy/gacha-adjacent character" path — selling characters is explicitly out of scope.
- Everything in the shop costs **coins** (earned from stages), not gems. Gems are the premium currency bought only through topup. Keep those lanes separate: shop → coins, topup → gems.
- `TICKET_PRICE = 1500` coins per ticket; `SHOP_MAT_PRICE` is a `{"R": 10, "SR": 25, "SSR": 60}` per-unit price keyed by rarity, so **a new rarity must be added to `SHOP_MAT_PRICE`** or `shop_material_menu` raises `KeyError` (same family of mistake as `DUPE_COIN_REFUND`).
- Tickets are consumed by `pay_and_pull()` at **1 ticket per pull** — a 10-pull costs 10 tickets. Tickets are *not* a discount: they are an alternate wallet for the same `run_pulls()` call, so pity/rank behave identically.
- `TOPUP_PACKS` entries are `{name, idr, gems, bonus}` where the player receives `gems + bonus`. It is a **dummy purchase** — no payment backend, just `if input == "ya"`. The `idr` field is display-only string input for `fmt_idr()`; don't compute anything from it.
- Shop and topup both take coins/gems directly and call `save_state()` after each successful transaction; the cancel paths don't, so a cancel leaves state untouched.

## Balance constraints

Cost to take one character from Lv.1 to Lv.20 is 247 of its own material (`sum(level_cost(l) for l in 1..19)`), and per-stage drop amounts were set to land at **5–13 clears per character**. The grind is gated on *which* stage drops the material, not on quantity, so drop amounts stay flat across stages. If you retune `LEVEL_COST_BASE`/`LEVEL_COST_STEP`/`MAX_LEVEL` or the `drops` amounts, re-check that ratio — an earlier draft cost 912 material against ~6/clear, which is ~150 runs per character and unplayable even for a flow prototype.

## Repo layout

- This directory is **not a git repo of its own** — `git rev-parse` walks up to the user's home directory, whose only commit is a stray `README.md` containing `# .github`. Don't run git commands expecting real project history here.
- `../ecoboo/` is a separate project with its own git repo and its own `AGENTS.md`; don't apply its Node/Docker instructions here.
- `itkopter/` is the game itself (13 modules — see *Package layout*); `itkopter_cli.py` is only the compatibility shim.
- The other files are `itkopter_save.json` (guest play state, disposable), `itkopter_session.json` (login pointer), and `itkopter_save_<name>.json` for named accounts. Ignore any `*.crdownload` that shows up — those are unrelated partial Chrome downloads.
- `itkopter.zip` is the distributable snapshot and must contain **sources only**. Regenerate with `zip -X itkopter.zip AGENTS.md itkopter_cli.py itkopter/*.py` — never `zip -r` over the directory, which sweeps up `__pycache__/*.pyc` and every real save. An earlier copy shipped 14 `.pyc` files plus `itkopter_save_niga_niga.json` and `itkopter_session.json`; don't reintroduce them.
