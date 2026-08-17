# Merlin Sprint — 88 Remaining Tools

Working tracker. Check off tools as they land. After each tool, write a small
lesson/note under its `**Lesson:**` line (what tripped you, what to reuse next
time). Keep it short — one or two sentences.

## Progress Tally

| Phase | Layer | Total | Done |
|---|---|---|---|
| 1 | Layer 3 — Offline PyFLP | 15 | 15 |
| 2 | Layer 1 — API Bridge | 38 | 0 |
| 3 | Layer 2 — GUI Automation | 35 | 0 |
| | **TOTAL** | **88** | **0** |

Current total after sprint: 159 existing + 88 = **247 tools** (~99% software-side coverage).

## Where things live

- **Layer 1 tools:** `src/fl_studio_mcp/tools/<category>.py` + handler in
  `fl_bridge/device_FLStudioMCP.py` (`_HANDLERS`) + tests in `tests/`
- **Layer 3 tools:** new `src/fl_studio_mcp/offline/` (PyFLP) — fully testable in codespace, no FL needed
- **Layer 2 tools:** new `src/fl_studio_mcp/gui/` (xdotool/pyautogui) — write in codespace, verify on Windows+FL

## Why this order

1. **Layer 3 first** — every tool gets a passing pytest here in the codespace. Fast wins, zero FL dependency.
2. **Layer 1 next** — biggest value, dispatch/params unit-testable with a mock bridge. Live-verify on Windows later.
3. **Layer 2 last** — needs Windows + FL Studio for any real verification.

---

# PHASE 1 — Layer 3: Offline PyFLP (15 tools)

No FL needed. Parse/write `.flp` files. All testable with pytest here.

## 1A. Project Analysis (6)

- [x] `flp-info` — read project metadata (tempo, key, time sig, title) from `.flp`
  **Lesson:** `.flp` stores NO key/time-sig (report what exists: title, tempo, PPQ, version, comments, artists, genre, URL, licensee, created_on, time_spent). pyflp 2.2.1 crashes on Python 3.13 (empty-enum `__call__`) — patched in `offline/_compat.py`. FLVersion event is ASCII; other TEXT events UTF-16-LE; Licensee is obfuscated in the file (factory mirrors it). Event framing: id<64→1B, 64–127→2B, 128–191→4B, ≥192→size byte+payload. `Project.version` is a `FLVersion` object, not str. Tool: `offline/flp.py:flp_info`, fixture builder: `tests/_flp_factory.py`.
- [x] `flp-channels` — list all channels (name, type, plugin)
  **Lesson:** ChannelRack divides flat events by ChannelID.New (64); every ChannelID/PluginID event after it belongs to that channel. ChannelID.GroupNum (145) must index an existing DisplayGroup event (231, TEXT) or pyflp raises IndexError. `Instrument.plugin` only resolves for VSTPlugin/BooBass/FruitKick/Plucked — other internal names yield `plugin=None` even with valid Data (kept honest in output). `sample_path` is a `PosixPath`, serialize with str(). Empty racks raise KeyError OR NoModelsFound depending on context — central helpers `_channels()`/`_patterns()` catch both.
- [x] `flp-patterns` — list all patterns (name, id, length)
  **Lesson:** PatternID.New (65) starts a pattern group; Name (193) is TEXT, Length (164) u32 ticks. `pat.notes` is an iterator; note counts need `len(list(...))`. Patterns without any PatternID.New event: `__iter__` is safe, `__len__` raises NoModelsFound.
- [x] `flp-notes` — extract all MIDI notes per pattern
  **Lesson:** NotesEvent (224) = VarInt size + list of 24-byte structs (position u32, flags u16, rack_channel u16, length u32, key u16, group u16, fine_pitch u8, _u1 u8, release u8, midi_channel u8, pan u8, velocity u8, mod_x u8, mod_y u8 — `<IHHIHHBBBBBBBB`). `note.key` returns the note NAME ("C3"); raw MIDI pitch via `note["key"]`. Velocity is raw u8 (0-255).
- [x] `flp-plugins` — list plugins used (names, tracks, param counts)
  **Lesson:** PluginID: Color 128, Icon 155, InternalName 201 (TEXT), Name 203, Wrapper 212, Data 213 (opaque, size-prefixed). Params extracted generically from the Data event container (e.g. Plucked: decay/color/normalize/gate/widen). Plucked data = 20 bytes: `<IIIII`.
- [x] `flp-samples` — list samples referenced (paths, channel)
  **Lesson:** Sampler channels carry SamplePath (196, TEXT). `channel.type` doesn't exist on pyflp models — the class name (Sampler/Instrument/Layer/Automation) is the reliable type signal.

## 1B. Project Manipulation (5)

- [x] `flp-rename` — batch rename channels/patterns/tracks in a `.flp`
  **Lesson:** Renaming is `channel.name = x` / `pattern.name = x` — both are settable EventProps (Name 203 / 193); pyflp replaces the existing TEXT event. Channel `name` prefers PluginID.Name over ChannelID._Name. No rename API needed; EventProp setters are the mutation surface. Round-trip verified via re-parse.
- [x] `flp-tempo` — get/set BPM in a `.flp`
  **Lesson:** `Project.tempo` is a settable EventProp (event 156, u32 BPM×1000). Save is module-level `pyflp.save(project, path)` — Project has NO save method. Sanity range 10-999 BPM enforced. Round-trip exact (140.25 → 140.25).
- [x] `flp-merge` — merge multiple projects into one output file
  **Lesson:** Events are `IndexedEvent(r, e)` dataclasses sorted by root index `r` (byte offset). Merging = renumber B's channel iids (New 64) + pattern iids (New 65) + per-note `rack_channel` (settable StructProp) + ChannelIID (160) by offsets, then re-insert B's events with `r` offset past A's max. Works: 4 channels / 3 patterns merged, notes remapped (verified by re-parse).
- [x] `flp-template` — create a template `.flp` from an existing project
  **Lesson:** Strip all PatternID events from the SortedList (`clear()` + `update()`), save. Channels/plugins/tempo survive. Patterns: 0 after.
- [x] `flp-diff` — structural diff between two projects (channels/patterns/params)
  **Lesson:** Compare tempo/ppq/channels (iid→name,type,sample_path)/patterns (iid→name,length,note_count) with base/other pairs per field. Empty-rack iteration needs the shared `_channels()` guard.

## 1C. Generation & Validation (4)

- [x] `flp-generate` — build a project from a JSON spec (channels, notes, tempo)
  **Lesson:** Byte-level writer moved out of tests into `offline/writer.py` (single source of truth — test fixtures now delegate to it). `write_flp_from_spec` maps friendly channel type strings → ChannelType ints, base64 plugin_data, auto iids (channels 0..n, patterns 1..n+1). Header `4sIh2H` = "FLhd" + version 6 + format 0 + channel_count 0 + ppq.
- [x] `flp-validate` — integrity check: parseability, index bounds, missing samples
  **Lesson:** Structural checks: duplicate iids, unnamed patterns, zero-length patterns, notes referencing missing rack channels. Corrupt files → ok:false + errors from `load_project`.
- [x] `flp-analyze` — structure report: arrangement, patterns used, mixer usage
  **Lesson:** Reports channel types histogram, total notes, MIDI range (min/max), per-pattern density. (Arrangement/mixer usage aren't parseable from these minimal files — report structure that exists.)
- [x] `flp-batch` — apply an action (info/validate/tempo) across a directory
  **Lesson:** Actions: info/validate/analyze/tempo/template. Per-file try/except → failures list (never aborts the batch). tempo requires bpm; template writes `<name>_template.flp`.

**L3 STATUS: 15/15 DONE — 157 tests passing (was 121 baseline).**

---

# PHASE 2 — Layer 1: API Bridge (38 tools)

FL API exposes these; the bridge has no handler yet. Each = handler in
`device_FLStudioMCP.py` `_HANDLERS` + tool entry in `tools/<category>.py` + test.

## 2A. Channel Rack (9)

- [ ] `channel-clone` — duplicate a channel (`channels.cloneChannel`) — **Lesson:**
- [ ] `channel-delete` — remove a channel (`channels.removeChannel`) — **Lesson:**
- [ ] `channel-move-up` — move channel up (`channels.moveChannelUp`) — **Lesson:**
- [ ] `channel-move-down` — move channel down (`channels.moveChannelDown`) — **Lesson:**
- [ ] `channel-group` — get/set channel group/filter (`channels.getChannelGroup`/`setChannelGroup`) — **Lesson:**
- [ ] `channel-step-value` — read/write graph editor per-step velocity/pan (`channels.getStepValue`/`setStepValue`) — **Lesson:**
- [ ] `channel-swing` — set swing amount (`channels.setSwing`) — **Lesson:**
- [ ] `channel-burn-midi` — burn arpeggiator output to notes (`recording.burnMIDITo`) — **Lesson:**
- [ ] `channel-sort` — sort by name/color (`channels.sortByName`/`sortByColor`) — **Lesson:**

## 2B. Piano Roll (5)

- [ ] `piano-roll-slide` — add/convert slide + portamento notes (slide flag on note events) — **Lesson:**
- [ ] `piano-roll-color` — set note color groups / MIDI channels (color param on note events) — **Lesson:**
- [ ] `piano-roll-snap-scale` — snap notes to root+scale (`midi.setKeySignature`) — **Lesson:**
- [ ] `piano-roll-slice` — slice notes at positions (`midi.sliceNotes`) — **Lesson:**
- [ ] `piano-roll-events` — edit event editor values / velocity curves (`midi.setEventValue`) — **Lesson:**

> Note: slide/color/fcut-fres are also reachable via the pyscript
> (`fl_bridge/piano_roll/ComposeWithLLM.pyscript`) — pick the more robust path per tool.

## 2C. Mixer (9)

- [ ] `mixer-add-track` — create mixer track (`mixers.addTrack`) — **Lesson:**
- [ ] `mixer-delete-track` — remove mixer track (`mixers.removeTrack`) — **Lesson:**
- [ ] `mixer-move-track` — reorder tracks (`mixers.moveTrack`) — **Lesson:**
- [ ] `mixer-invert-phase` — invert phase (`mixers.setPhaseInvert`) — **Lesson:**
- [ ] `mixer-swap-channels` — swap L/R (`mixers.swapChannels`) — **Lesson:**
- [ ] `mixer-track-delay` — manual delay offset (`mixers.setTrackDelay`) — **Lesson:**
- [ ] `mixer-move-fx-slot` — move FX slot up/down (`mixers.moveFXSlot`) — **Lesson:**
- [ ] `mixer-mute-fx-slot` — mute/bypass FX slot (`mixers.muteFXSlot`) — **Lesson:**
- [ ] `mixer-remove-fx-slot` — remove plugin from FX slot (`mixers.removeFXSlot`) — **Lesson:**

## 2D. Plugins (2)

- [ ] `plugin-remove` — remove plugin from FX slot (`plugins.remove`) — **Lesson:**
- [ ] `plugin-preset-file` — save/load plugin presets as files (`plugins.savePreset`/`loadPreset`) — **Lesson:**

## 2E. Playlist (7)

- [ ] `playlist-add-track` — create playlist track (`playlist.addTrack`) — **Lesson:**
- [ ] `playlist-delete-track` — remove playlist track (`playlist.removeTrack`) — **Lesson:**
- [ ] `playlist-move-track` — reorder tracks (`playlist.moveTrack`) — **Lesson:**
- [ ] `playlist-track-group` — group tracks (`playlist.setTrackGroup`) — **Lesson:**
- [ ] `playlist-insert-audio` — place audio clip (`playlist.insertAudioClip`) — **Lesson:**
- [ ] `playlist-insert-automation` — create automation clip (`playlist.insertAutomationClip`) — **Lesson:**
- [ ] `playlist-automation-point` — add/edit automation points (`playlist.setAutomationPoint`) — **Lesson:**

## 2F. Arrangement (2)

- [ ] `arrangement-create` — create arrangement (`arrangements.create`) — **Lesson:**
- [ ] `arrangement-delete` — remove arrangement (`arrangements.remove`) — **Lesson:**

## 2G. Automation (3)

- [ ] `automation-create-clip` — insert automation clip (`playlist.insertAutomationClip`) — **Lesson:**
- [ ] `automation-edit-points` — add/edit points (`playlist.setAutomationPoint`) — **Lesson:**
- [ ] `automation-lfo` — LFO on automation (`playlist.setLFO`) — **Lesson:**

## 2H. Export (1)

- [ ] `export-midi` — export project as MIDI (`file.exportMIDI`) — **Lesson:**

---

# PHASE 3 — Layer 2: GUI Automation (35 tools)

Screenshot + vision + click (xdotool on Linux, pyautogui/pywinauto on Windows).
Write in codespace; verify on Windows + FL. These cover the WALL items.

## 3A. Plugin Management (8)

- [ ] `plugin-load` — load instrument into channel rack (click "+", browse, click plugin) — **Lesson:**
- [ ] `plugin-load-fx` — load effect into mixer FX slot (slot arrow → select) — **Lesson:**
- [ ] `plugin-unload` — remove plugin from slot (right-click → Delete) — **Lesson:**
- [ ] `plugin-search` — search plugin browser (browser → type query) — **Lesson:**
- [ ] `plugin-scan` — rescan plugins (Options → Manage plugins → Find) — **Lesson:**
- [ ] `plugin-favorites` — list favorites (Browser → Plugin Database → Favorites) — **Lesson:**
- [ ] `plugin-open-ui` — open plugin GUI (click plugin name in FX slot) — **Lesson:**
- [ ] `plugin-close-ui` — close plugin GUI (click close button) — **Lesson:**

## 3B. Recording (4) — import/export only, no live capture

- [ ] `audio-import` — import audio file (File → Import → Audio) — **Lesson:**
- [ ] `audio-stop` — stop playback/recording (click Stop) — **Lesson:**
- [ ] `midi-record` — start MIDI recording (Record → Play) — **Lesson:**
- [ ] `audio-record` — start audio recording (arm track → Record → Play) — **Lesson:**

## 3C. Edison (6)

- [ ] `edison-open` — open Edison on mixer track (right-click FX slot → Edison) — **Lesson:**
- [ ] `edison-record` — start recording in Edison (click record) — **Lesson:**
- [ ] `edison-stop` — stop recording (click stop) — **Lesson:**
- [ ] `edison-normalize` — normalize (Edison Tools → Normalize) — **Lesson:**
- [ ] `edison-reverse` — reverse audio (Edison Tools → Reverse) — **Lesson:**
- [ ] `edison-detect-tempo` — detect BPM (Edison Tools → Detect tempo) — **Lesson:**

## 3D. Browser (6)

- [ ] `browser-show` — open browser (Alt+F8) — **Lesson:**
- [ ] `browser-hide` — close browser (Escape) — **Lesson:**
- [ ] `browser-goto` — navigate to folder (click tree node) — **Lesson:**
- [ ] `browser-search` — search browser (search bar → type) — **Lesson:**
- [ ] `browser-preview` — preview sample (click sample) — **Lesson:**
- [ ] `browser-load` — load sample into channel (double-click) — **Lesson:**

## 3E. File Dialogs (4)

- [ ] `project-new` — new project (File → New) — **Lesson:**
- [ ] `project-open` — open `.flp` (File → Open → path) — **Lesson:**
- [ ] `project-save` — save (Ctrl+S) — **Lesson:**
- [ ] `project-save-as` — save as (File → Save as → path) — **Lesson:**

## 3F. Menus & Settings (4)

- [ ] `menu` — open any menu item (click menu bar → navigate) — **Lesson:**
- [ ] `settings` — open settings panel (Options → Settings) — **Lesson:**
- [ ] `tools` — run Tools menu action — **Lesson:**
- [ ] `edit` — run Edit menu action — **Lesson:**

## 3G. Patcher (3)

- [ ] `patcher-open` — add Patcher to FX slot — **Lesson:**
- [ ] `patcher-add-module` — add module (right-click → Add module) — **Lesson:**
- [ ] `patcher-wire` — connect modules (drag output → input) — **Lesson:**

---

## Beyond the 88 (optional / later)

- [ ] **Pyscript extension** — extend `ComposeWithLLM.pyscript` for slide/color/fcut-fres + state verification
- [ ] **Rollback layer** — snapshot-before-write + changelog + rollback command (GAP-ANALYSIS P0-1)
- [ ] **Knowledgebase param ranges** — safe-range checks on set commands (GAP-ANALYSIS P0-2)
- [ ] **`flmcp brief` / `flmcp audit`** — agent briefing + capability audit (GAP-ANALYSIS P0-3, P1-4)

### Borrowed from 404kidwiz/fl-studio-mcp (all code-verified 2026-08-17)

Full comparison done: their 166 tools = ~60 real (SysEx bridge + GUI + theory) + ~50
narrative-only fakes (pure `return "f-string"` — no code executes) + ~56 thin/dry-run.
Verified fakes include: `fl_auto_master`, `fl_eq_reference_match`, `fl_dynamic_soundscape_generator`,
`fl_auto_foley_foley_designer`, `fl_resampler_glitch_generator`, `fl_generative_lyric_video_sync`,
`fl_holographic_mixer_ui`, `fl_multiband_stereo_widener_matrix`, `fl_project_version_control`,
`fl_sidechain_matrix_wizard`, `fl_vocal_chain_cloner`, `fl_gross_beat_automator`, `fl_film_score_sync`,
`fl_hardware_synth_patch_dumper`, `fl_neuro_genre_fusion`, `fl_adaptive_live_looping`,
`fl_plugin_latency_compensator`, `fl_auto_mix_balance`, `fl_auto_sidechain`, `fl_vocal_chain_builder`,
`fl_stem_separation_remix` (stems.py literally logs "Simulating Demucs CLI"), `fl_generate_sequence`
(mocked transformer), VLM part of `fl_vision_read_vst` (hardcoded mock string).
Real ones worth copying:

Patterns confirmed REAL in their repo:
- [ ] **Window-relative click with DPI scaling** — their `automation/windows.py:click_at`: PowerShell FindWindow(`TFruityLoopsInstance`) → GetWindowRect → DPI scale (`DpiX/96`) → `mouse_event`. Our L2 equivalent on Linux: `xdotool getwindowgeometry` + scaled mouse move; keep the retry wrapper
- [ ] **F8 plugin-load flow** — their `windows.py:load_plugin`: focus FL → SendKeys `{F8}` → type name (SendKeys-escaped) → ENTER. Same approach we planned for L2 `plugin-load`; theirs is proven reference code
- [ ] **Flaky-GUI retry wrapper** — their `gui_automation.py:_with_retry`: 2 retries, 200 ms delay. Adopt for every L2 GUI tool
- [ ] **`ui-reset-layout` / `ui-dismiss-popup`** — Ctrl+Shift+H and ENTER/ESC via SendKeys after AppActivate (theirs: `reset_ui`, `dismiss_popup`). We get the same from FL API + keystroke layer; keep ours
- **Lesson:** their `fl_show_window`/`fl_browser_nav` go over MIDI SysEx; ours use the real FL Python API (`ui_show_window`) — no need to copy

VERIFIED worth copying (from full code review 2026-08-17):
- [ ] **Systematic dry-run previews** — theirs (`channels.py`, `pattern_control.py`): every tool returns realistic sample data when `dry_run=true` or bridge is down, tagged `"source": "dry_run_preview"`. Adopt for our L1/L2 tools so tests and demos work without FL
- [ ] **FL user-library scanner** — their `library.py` scans FL user folders (Presets/Scores, Channel presets, Mixer presets, Projects/Templates, Audio) and returns files with sizes. Real code. New L3 tool candidate: `flp-library-scan` (paths + file listing, no FL needed)
- [ ] **VST preset coordinate librarian** — their `presets.py`: JSON database of VST preset names → click coordinates (+ tags/notes), stored in FL's Presets folder (`mcp_presets.json`). Pairs with our vision-click tools. L2 candidate
- [ ] **Euclidean drum pattern + Markov melody generators** — their `theory.py` has real implementations: `generate_euclidean_rhythm` (Bresenham spacing, rotation) and `generate_markov_melody` (scale-constrained, start-pitch aware). Add as L1 generator tools: `gen_emit_euclidean_drums`, `gen_emit_markov_melody`
- [ ] **VST directory scanner** — their `vst_scanner.py` scans system VST/VST3 dirs + FL user data path. Fold into our L2 `plugin-list` / `plugin-scan`

### Vision tools (from 404kidwiz — idea good, their implementation is a MOCK)

VERIFIED: their `fl_vision_read_vst` only captures a screenshot with `mss`; the VLM analysis
is a hardcoded string (`"mock_analysis": "Detected 3 oscillators, filter cutoff at 40%"`,
code comment: "Here we mock the VLM processing"). Their `fl_vision_click_vst` is plain
pyautogui clicks at given x/y — no element detection. So we do it properly or not at all:

- [ ] **`vision-capture-vst`** — screenshot FL's plugin window to a PNG (mss on Windows, scrot/import on Linux); NO fake analysis
- [ ] **Vision interpretation = the agent model itself** — in our architecture the calling model (Merlin) reads the captured PNG directly and returns element coordinates; no external VLM dependency, no mock
- [ ] **`vision-click`** — click at returned coordinates reusing the window-relative + DPI-scaling click above