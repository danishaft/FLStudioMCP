# Merlin Sprint — 88 Remaining Tools

Working tracker. Check off tools as they land. After each tool, write a small
lesson/note under its `**Lesson:**` line (what tripped you, what to reuse next
time). Keep it short — one or two sentences.

## Progress Tally

| Phase | Layer | Total | Done |
|---|---|---|---|
| 1 | Layer 3 — Offline PyFLP | 15 | 0 |
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

- [ ] `flp-info` — read project metadata (tempo, key, time sig, title) from `.flp` — **Lesson:**
- [ ] `flp-channels` — list all channels (name, type, plugin) — **Lesson:**
- [ ] `flp-patterns` — list all patterns (name, id, length) — **Lesson:**
- [ ] `flp-notes` — extract all MIDI notes per pattern — **Lesson:**
- [ ] `flp-plugins` — list plugins used (names, tracks, param counts) — **Lesson:**
- [ ] `flp-samples` — list samples referenced (paths, channel) — **Lesson:**

## 1B. Project Manipulation (5)

- [ ] `flp-rename` — batch rename channels/patterns/tracks in a `.flp` — **Lesson:**
- [ ] `flp-tempo` — get/set BPM in a `.flp` — **Lesson:**
- [ ] `flp-merge` — merge multiple projects into one output file — **Lesson:**
- [ ] `flp-template` — create a template `.flp` from an existing project — **Lesson:**
- [ ] `flp-diff` — structural diff between two projects (channels/patterns/params) — **Lesson:**

## 1C. Generation & Validation (4)

- [ ] `flp-generate` — build a project from a JSON spec (channels, notes, tempo) — **Lesson:**
- [ ] `flp-validate` — integrity check: parseability, index bounds, missing samples — **Lesson:**
- [ ] `flp-analyze` — structure report: arrangement, patterns used, mixer usage — **Lesson:**
- [ ] `flp-batch` — apply an action (info/validate/tempo) across a directory — **Lesson:**

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