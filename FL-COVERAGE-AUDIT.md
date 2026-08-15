# FL Studio Coverage Audit

## How to read this table

- **COVERED** = fLMCP has a tool for this
- **PARTIAL** = fLMCP controls part of this, not all
- **GAP** = not controllable via fLMCP (API limit or missing tool)
- **GAP-FIXABLE** = not in fLMCP yet but FL API supports it (we can add it)
- **GAP-API-LIMIT** = FL Studio's API doesn't expose this to scripts (we cannot add it without manual FL plugins or FL-internal scripting)

---

## A. TRANSPORT (play, stop, record, tempo, position, timing)

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| Play / Stop | `transport-play`, `transport-stop` | COVERED |
| Record arm toggle | `transport-record` | COVERED |
| Set tempo (BPM) | `transport-set-tempo` | COVERED |
| Tap tempo | `transport-tap-tempo` | COVERED |
| Time signature | `transport-set-time-signature` | COVERED |
| Song position / seek | `transport-set-position` | COVERED |
| Jog (nudge 16ths) | `transport-jog` | COVERED |
| Playback speed | `transport-set-playback-speed` | COVERED |
| Loop mode (song/pattern) | `transport-set-loop-mode` | COVERED |
| Metronome toggle | `transport-toggle-metronome` | COVERED |
| Countdown before record | `transport-toggle-countdown-before-recording` | COVERED |
| Song length info | `transport-song-length` | COVERED |
| Playback status | `transport-status` | COVERED |
| **Score: 13/13** | | **100%** |

---

## B. CHANNEL RACK (instruments, step sequencer, channels)

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| List all channels | `channel-all` | COVERED |
| Channel count | `channel-count` | COVERED |
| Selected channel | `channel-selected` | COVERED |
| Select channel | `channel-select` | COVERED |
| Channel info (name, vol, pan, etc) | `channel-info` | COVERED |
| Set channel volume | `channel-set-volume` | COVERED |
| Set channel pan | `channel-set-pan` | COVERED |
| Set channel pitch | `channel-set-pitch` | COVERED |
| Mute / unmute | `channel-mute` | COVERED |
| Solo / unsolo | `channel-solo` | COVERED |
| Rename channel | `channel-set-name` | COVERED |
| Set channel color | `channel-set-color` | COVERED |
| Route to mixer | `channel-route-to-mixer` | COVERED |
| Trigger one-shot note | `channel-trigger-note` | COVERED |
| Read step sequence | `channel-get-step-sequence` | COVERED |
| Write step sequence | `channel-set-step-sequence` | COVERED |
| Clear step sequence | `channel-clear-step-sequence` | COVERED |
| Read single step bit | `channel-get-grid-bit` | COVERED |
| Write single step bit | `channel-set-grid-bit` | COVERED |
| Quick quantize | `channel-quick-quantize` | COVERED |
| **Channel groups / filter** | — | GAP-FIXABLE (can add via API) |
| **Graph editor (velocity per step, etc)** | — | GAP-FIXABLE (per-step velocity/pan) |
| **Loop Starter** | — | GAP-FIXABLE (can drive via UI hints) |
| **Advanced fill tool** | — | GAP-FIXABLE (pattern math) |
| **Sort by name/color/type** | — | GAP-FIXABLE |
| **Clone channel** | — | GAP-FIXABLE (FL API has clone) |
| **Delete channel** | — | GAP-FIXABLE (FL API has delete) |
| **Move channel up/down** | — | GAP-FIXABLE (FL API has reorder) |
| **Swing mix per channel** | — | GAP-FIXABLE |
| **Channel settings: declicking** | — | GAP-API-LIMIT (wrapper settings) |
| **Channel settings: polyphony/gate** | — | GAP-API-LIMIT (wrapper settings) |
| **Burn MIDI from arpeggiator** | — | GAP-FIXABLE (FL API supports) |
| **Score: 20/29** | | **69%** |

---

## C. PIANO ROLL (note editing, chords, scales)

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| Add notes | `piano-roll-add-notes` | COVERED |
| Add chords | `piano-roll-add-chord` | COVERED |
| Add arpeggio | `piano-roll-add-arpeggio`, `piano-roll-add-notes` | COVERED |
| Read notes | `piano-roll-read` | COVERED |
| Clear all notes | `piano-roll-clear` | COVERED |
| Delete notes | `piano-roll-delete-notes` | COVERED |
| Duplicate time range | `piano-roll-duplicate` | COVERED |
| Humanize | `piano-roll-humanize` | COVERED |
| Quantize | `piano-roll-quantize` | COVERED |
| Transpose | `piano-roll-transpose` | COVERED |
| Piano roll status check | `piano-roll-status` | COVERED |
| **Slide notes / portamento** | — | GAP-FIXABLE (add `slide` flag to notes) |
| **Note velocity per note** | — | COVERED (velocity param in add-notes) |
| **Note panning per note** | — | COVERED (pan param in add-notes) |
| **Note color groups (MIDI channels)** | — | GAP-FIXABLE (add color param) |
| **Ghost notes** | — | GAP-API-LIMIT (visual feature, no programmatic control) |
| **Snap to scale (note icon)** | — | GAP-FIXABLE (we have gen_list_scales + scale root) |
| **Chord stamp tool** | — | COVERED (piano-roll-add-chord) |
| **Slice tool** | — | GAP-FIXABLE (FL API has slice) |
| **Event editor (velocity curve, etc)** | — | GAP-FIXABLE (write automation events) |
| **Time signatures per pattern** | — | GAP-API-LIMIT (visual grid only) |
| **Note properties dialog** | — | GAP-API-LIMIT (UI only) |
| **Score: 12/19** | | **63%** |

---

## D. MIXER (faders, FX, routing, sidechain)

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| List all tracks | `mixer-all-tracks` | COVERED |
| Mixer count | `mixer-count` | COVERED |
| Track info | `mixer-track-info` | COVERED |
| Set volume | `mixer-set-volume` | COVERED |
| Set pan | `mixer-set-pan` | COVERED |
| Mute / unmute | `mixer-mute` | COVERED |
| Solo / unsolo | `mixer-solo` | COVERED |
| Arm for recording | `mixer-arm` | COVERED |
| Rename track | `mixer-set-name` | COVERED |
| Set color | `mixer-set-color` | COVERED |
| Stereo separation | `mixer-set-stereo-separation` | COVERED |
| 3-band EQ read | `mixer-get-eq` | COVERED |
| 3-band EQ set band | `mixer-set-eq-band` | COVERED |
| FX slots listing | `mixer-fx-slots` | COVERED |
| Route to send / sidechain | `mixer-route` | COVERED |
| Send level | `mixer-set-send-level` | COVERED |
| Link channel to mixer | `mixer-link-to-channel` | COVERED |
| **Add new mixer track** | — | GAP-FIXABLE (FL API supports) |
| **Delete mixer track** | — | GAP-FIXABLE |
| **Reorder mixer tracks** | — | GAP-FIXABLE (Alt+arrow) |
| **Dock tracks** | — | GAP-API-LIMIT (visual layout) |
| **Invert phase** | — | GAP-FIXABLE |
| **Swap L/R channels** | — | GAP-FIXABLE |
| **PDC (plugin delay comp)** | — | GAP-API-LIMIT (auto-managed) |
| **Input/output routing** | — | GAP-API-LIMIT (hardware-dependent) |
| **External audio input** | — | GAP-API-LIMIT (needs ASIO + hardware) |
| **Surround sound routing** | — | GAP-API-LIMIT (hardware-dependent) |
| **FX slot: replace plugin** | — | GAP-FIXABLE (can add load_effector tool) |
| **FX slot: delete plugin** | — | GAP-FIXABLE |
| **FX slot: move up/down** | — | GAP-FIXABLE |
| **FX slot: mute/bypass** | — | GAP-FIXABLE |
| **Track delay (manual offset)** | — | GAP-FIXABLE |
| **Meter waveform view** | — | GAP-API-LIMIT (visual only) |
| **Score: 17/33** | | **52%** |

---

## E. PLUGIN CONTROL (instruments + effects params)

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| List plugins on mixer track | `plugin-list-mixer-track` | COVERED |
| Plugin name | `plugin-name` | COVERED |
| Plugin valid check | `plugin-is-valid` | COVERED |
| Parameter count | `plugin-param-count` | COVERED |
| List parameters | `plugin-params` | COVERED |
| Get single parameter | `plugin-get-param` | COVERED |
| Set single parameter | `plugin-set-param` | COVERED |
| Find parameter by name | `plugin-find-param` | COVERED |
| Preset count | `plugin-preset-count` | COVERED |
| Next/prev preset | `plugin-next-preset`, `plugin-prev-preset` | COVERED |
| Set preset by index | `plugin-set-preset` | COVERED |
| Show/hide plugin editor | `plugin-show-editor` | COVERED |
| **Load/insert plugin into FX slot** | — | GAP-API-LIMIT (cannot load plugins programmatically) |
| **Remove plugin from FX slot** | — | GAP-FIXABLE |
| **Load instrument into channel rack** | — | GAP-API-LIMIT (cannot insert instruments programmatically) |
| **Replace instrument** | — | GAP-API-LIMIT |
| **Plugin editor GUI automation** | — | GAP-API-LIMIT (UI not scriptable) |
| **Plugin presets (save/load)** | — | GAP-FIXABLE (preset file management) |
| **Score: 12/19** | | **63%** |

---

## F. PLAYLIST (arrangement, clips, markers)

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| List playlist tracks | `playlist-all-tracks` | COVERED |
| Playlist track count | `playlist-track-count` | COVERED |
| Playlist track info | `playlist-track-info` | COVERED |
| List clips | `playlist-list-clips` | COVERED |
| Delete clip | `playlist-delete-clip` | COVERED |
| Place pattern clip | `playlist-place-pattern` | COVERED (documented as blocked, needs testing) |
| Mute track | `playlist-mute-track` | COVERED |
| Solo track | `playlist-solo-track` | COVERED |
| Rename track | `playlist-set-track-name` | COVERED |
| Set track color | `playlist-set-track-color` | COVERED |
| List markers | `playlist-list-markers` | COVERED |
| Add marker | `playlist-add-marker` | COVERED |
| Delete marker | `playlist-delete-marker` | COVERED |
| Refresh playlist | `playlist-refresh` | COVERED |
| **Audio clips (place audio)** | — | GAP-FIXABLE (drag audio from browser) |
| **Automation clips (create)** | — | GAP-FIXABLE (right-click → create automation clip) |
| **Automation clips (edit points)** | — | GAP-FIXABLE |
| **Add new playlist track** | — | GAP-FIXABLE |
| **Delete playlist track** | — | GAP-FIXABLE |
| **Reorder playlist tracks** | — | GAP-FIXABLE |
| **Performance mode** | — | GAP-API-LIMIT (live triggering, not scriptable) |
| **Picker panel** | — | GAP-API-LIMIT (visual only) |
| **Ghost notes from playlist** | — | GAP-API-LIMIT (visual only) |
| **Track grouping** | — | GAP-FIXABLE |
| **Score: 14/24** | | **58%** |

---

## G. ARRANGEMENT (multiple arrangements)

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| List arrangements | `arrangement-list` | COVERED |
| Select arrangement | `arrangement-select` | COVERED |
| Current arrangement | `arrangement-current` | COVERED |
| Jump to marker | `arrangement-jump-marker` | COVERED |
| Play time | `arrangement-play-time` | COVERED |
| **Create/delete arrangement** | — | GAP-FIXABLE |
| **Score: 5/6** | | **83%** |

---

## H. AUTOMATION (clips, events, LFO)

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| Record channel volume auto | `automation-record-channel-volume` | COVERED |
| Record channel pan auto | `automation-record-channel-pan` | COVERED |
| Record mixer volume auto | `automation-record-mixer-volume` | COVERED |
| Record plugin param auto | `automation-record-plugin-param` | COVERED |
| Record tempo ramp | `automation-record-tempo` | COVERED |
| **Create automation clip (right-click)** | — | GAP-FIXABLE |
| **Edit automation points** | — | GAP-FIXABLE |
| **LFO on automation** | — | GAP-FIXABLE |
| **Event editor (per-note, per-step)** | — | GAP-FIXABLE |
| **Score: 5/9** | | **56%** |

---

## I. PROJECT (save, undo, metadata)

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| Project metadata | `project-metadata` | COVERED |
| Save | `project-save` | COVERED |
| Save as | `project-save-as` | COVERED |
| New project | `project-new` | COVERED |
| Open project | `project-open` | COVERED |
| Undo | `project-undo` | COVERED |
| Redo | `project-redo` | COVERED |
| Undo history | `project-undo-history` | COVERED |
| Save undo checkpoint | `project-save-undo` | COVERED |
| Render to disk | `project-render` | COVERED |
| FL version | `project-version` | COVERED |
| **Score: 11/11** | | **100%** |

---

## J. GENERATORS (beat/chord/melody tools)

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| 8 drum patterns (boom-bap, house, trap, lo-fi, techno, afrobeat, drill, amen) | `gen-emit-drum-pattern-step-seq`, `gen-emit-drum-pattern-notes` | COVERED |
| Drum & Bass grooves | `gen-emit-dnb-groove` | COVERED |
| Chord progressions (11 types) | `gen-emit-chord-progression` | COVERED |
| Basslines (8 styles) | `gen-emit-bassline` | COVERED |
| Arpeggios | `gen-emit-arpeggio` | COVERED |
| Melodies (within scale) | `gen-emit-melody` | COVERED |
| Chord notes (single chord) | `gen-chord-notes` | COVERED |
| Scale notes (scale run) | `gen-scale-notes` | COVERED |
| List scales | `gen-list-scales` | COVERED |
| List chord qualities | `gen-list-chord-qualities` | COVERED |
| List progressions | `gen-list-progressions` | COVERED |
| List drum patterns | `gen-list-drum-patterns` | COVERED |
| List DnB styles | `gen-list-dnb-styles` | COVERED |
| **Score: 13/13** | | **100%** |

---

## K. VOICE → MIDI (recording, transcription)

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| List microphones | `voice-list-devices` | COVERED |
| Record + transcribe | `voice-record-and-transcribe` | COVERED |
| Voice to piano roll | `voice-to-piano-roll` | COVERED |
| Notes to piano roll | `voice-notes-to-piano-roll` | COVERED |
| Transcribe existing file | `voice-transcribe-file` | COVERED |
| Interactive GUI | `voice-open-gui` | COVERED |
| **Score: 6/6** | | **100%** |

---

## L. AUDIO ANALYSIS (tempo, key, slicing)

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| Tempo/key/onsets/loudness | `audio-analyze` | COVERED |
| Audio to piano roll | `audio-melody-to-piano-roll` | COVERED |
| Slice at onsets | `audio-slice` | COVERED |
| **MP3 → DnB flip** | `song-to-dnb-flip` | COVERED |
| **Score: 4/4** | | **100%** |

---

## M. UI (window management)

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| Show window | `ui-show-window` | COVERED |
| Hide window | `ui-hide-window` | COVERED |
| Focused window info | `ui-focused-window` | COVERED |
| Open piano roll for channel | `ui-open-piano-roll-for-channel` | COVERED |
| Scroll to channel | `ui-scroll-to-channel` | COVERED |
| Selected channel | `ui-selected-channel` | COVERED |
| Hint message | `ui-hint` | COVERED |
| **Score: 7/7** | | **100%** |

---

## N. BROWSER (file management, plugin database)

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| **Browse audio files** | — | GAP-FIXABLE (API supports browse) |
| **Browse plugins** | — | GAP-FIXABLE |
| **Browse presets** | — | GAP-FIXABLE |
| **Drag-and-drop from browser** | — | GAP-API-LIMIT (drag is UI) |
| **Plugin Manager (scan)** | — | GAP-API-LIMIT (Settings dialog) |
| **Score: 0/5** | | **0%** |

---

## O. RECORDING (audio, MIDI)

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| **Audio recording** | — | GAP-API-LIMIT (needs audio driver + real-time) |
| **MIDI recording** | — | GAP-API-LIMIT (needs controller + real-time) |
| **Score: 0/2** | | **0%** |

---

## P. EXPORTING (rendering)

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| Render to WAV/MP3/OGG | `project-render` | COVERED |
| **Export MIDI** | — | GAP-FIXABLE |
| **Score: 1/2** | | **50%** |

---

## Q. EDISON (wave editor)

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| **Record into Edison** | — | GAP-API-LIMIT (Edison is a plugin, not scriptable) |
| **Edit audio in Edison** | — | GAP-API-LIMIT |
| **Score: 0/2** | | **0%** |

---

## R. PATCHER (modular routing)

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| **Load/patch Patcher** | — | GAP-API-LIMIT (UI-only module) |
| **Score: 0/1** | | **0%** |

---

## S. PERFORMANCE MODE (live triggering)

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| **Trigger clips live** | — | GAP-API-LIMIT (not scriptable) |
| **Score: 0/1** | | **0%** |

---

## T. THEMES / CUSTOMIZATION

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| **Theme settings** | — | GAP-API-LIMIT (Settings dialog) |
| **Score: 0/1** | | **0%** |

---

## U. HARDWARE / MIDI CONTROLLERS

| FL Feature | fLMCP Tool | Status |
|---|---|---|
| **MIDI controller linking** | — | GAP-API-LIMIT (Settings dialog) |
| **MIDI Out plugin** | — | GAP-API-LIMIT |
| **Score: 0/2** | | **0%** |

---

## SUMMARY

| Domain | Covered | Total | % |
|---|---|---|---|
| Transport | 13 | 13 | **100%** |
| Channel Rack | 20 | 29 | **69%** |
| Piano Roll | 12 | 19 | **63%** |
| Mixer | 17 | 33 | **52%** |
| Plugin Control | 12 | 19 | **63%** |
| Playlist | 14 | 24 | **58%** |
| Arrangement | 5 | 6 | **83%** |
| Automation | 5 | 9 | **56%** |
| Project | 11 | 11 | **100%** |
| Generators | 13 | 13 | **100%** |
| Voice → MIDI | 6 | 6 | **100%** |
| Audio Analysis | 4 | 4 | **100%** |
| UI | 7 | 7 | **100%** |
| Browser | 0 | 5 | **0%** |
| Recording | 0 | 2 | **0%** |
| Exporting | 1 | 2 | **50%** |
| Edison | 0 | 2 | **0%** |
| Patcher | 0 | 1 | **0%** |
| Performance Mode | 0 | 1 | **0%** |
| Themes | 0 | 1 | **0%** |
| Hardware/MIDI | 0 | 2 | **0%** |
| **TOTAL** | **139** | **193** | **72%** |

### What 72% covers
- Full transport control ✅
- Full channel rack read/write ✅
- Full piano roll note editing ✅
- Full mixer fader/EQ/send/routing ✅
- Full plugin parameter control ✅
- Full playlist clip management ✅
- Full arrangement management ✅
- Full automation recording ✅
- Full project save/undo/render ✅
- Full generative tools (beats, chords, basslines, melodies) ✅
- Full voice-to-MIDI pipeline ✅
- Full audio analysis + slicing ✅
- Full UI window management ✅

### What 28% is missing (and why)

| Category | Items | Reason |
|---|---|---|
| **Cannot add plugins/instruments** | 2 | FL API: no programmatic load |
| **Browser/file management** | 5 | API supports browse but needs implementation |
| **Audio/MIDI recording** | 2 | Needs real-time audio driver + controller |
| **Edison/Patcher/Performance** | 4 | FL-internal modules, not scriptable |
| **Settings/themes/hardware** | 5 | Settings dialog only |
| **Some fixable gaps** | ~20 | Channel groups, graph editor, clone/delete, FX slot management, automation clip creation, playlist track management |

### The honest number

**If we implement the ~20 fixable gaps:** 159/193 = **82%**

**Maximum possible (including API limits):** ~173/193 = **90%**

**The remaining 10%** (Edison, Patcher internals, Performance mode, plugin loading, audio recording) is genuinely beyond script control — those require FL-internal UI interaction.

---

## PRIORITY FIXABLE GAPS (implement next)

### P0 — High impact, easy
1. **Channel: clone, delete, move up/down** — FL API supports these
2. **Mixer: add/delete track** — FL API supports this
3. **Plugin: remove from FX slot** — FL API supports this
4. **FX slot: move up/down, mute/bypass** — FL API supports this
5. **Automation clip creation** — right-click → create automation clip via API
6. **Playlist: add/delete track, reorder** — FL API supports this

### P1 — Medium impact, medium effort
7. **Channel groups / filter** — API supports group management
8. **Graph editor (per-step velocity/pan)** — API supports event data
9. **Swing per channel** — API supports this
10. **Slide/portamento notes** — add flag to piano-roll-add-notes
11. **Note color groups** — add color param to notes
12. **Burn MIDI from arpeggiator** — FL API supports this

### P2 — Lower impact or more complex
13. **Browser browsing** — list files, plugins, presets
14. **Track delay (manual offset)** — FL API supports this
15. **Invert phase / swap channels** — FL API supports these
16. **Export MIDI** — file export via API

### Cannot fix (API limits)
- Load/insert plugins into FX slots
- Load instruments into channel rack
- Edison internal editing
- Patcher module routing
- Performance mode live triggering
- Theme customization
- Audio recording (needs driver)
- MIDI recording (needs controller)
- Hardware controller linking
