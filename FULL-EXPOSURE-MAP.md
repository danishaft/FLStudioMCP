# FL Studio API — Full Exposure Map

## Legend
- **HAS** = fLMCP already has a tool for this
- **TO BE ADDED** = FL API exposes this, fLMCP skipped it, we can add it
- **WALL** = FL API does NOT expose this
- **APPROACH** = how to potentially reach it (for WALL items)

---

## TRANSPORT

| Operation | Status | Notes |
|---|---|---|
| Play / Stop | HAS | `transport-play`, `transport-stop` |
| Record arm | HAS | `transport-record` |
| Set tempo | HAS | `transport-set-tempo` |
| Tap tempo | HAS | `transport-tap-tempo` |
| Time signature | HAS | `transport-set-time-signature` |
| Song position / seek | HAS | `transport-set-position` |
| Jog (nudge 16ths) | HAS | `transport-jog` |
| Playback speed | HAS | `transport-set-playback-speed` |
| Loop mode | HAS | `transport-set-loop-mode` |
| Metronome | HAS | `transport-toggle-metronome` |
| Countdown before record | HAS | `transport-toggle-countdown-before-recording` |
| Song length | HAS | `transport-song-length` |
| Playback status | HAS | `transport-status` |
| **Score** | **13/13 = 100%** | |

---

## CHANNEL RACK

| Operation | Status | Notes |
|---|---|---|
| List all channels | HAS | `channel-all` |
| Channel count | HAS | `channel-count` |
| Selected channel | HAS | `channel-selected` |
| Select channel | HAS | `channel-select` |
| Channel info | HAS | `channel-info` |
| Set volume | HAS | `channel-set-volume` |
| Set pan | HAS | `channel-set-pan` |
| Set pitch | HAS | `channel-set-pitch` |
| Mute / unmute | HAS | `channel-mute` |
| Solo / unsolo | HAS | `channel-solo` |
| Rename | HAS | `channel-set-name` |
| Set color | HAS | `channel-set-color` |
| Route to mixer | HAS | `channel-route-to-mixer` |
| Trigger one-shot note | HAS | `channel-trigger-note` |
| Read step sequence | HAS | `channel-get-step-sequence` |
| Write step sequence | HAS | `channel-set-step-sequence` |
| Clear step sequence | HAS | `channel-clear-step-sequence` |
| Read single step bit | HAS | `channel-get-grid-bit` |
| Write single step bit | HAS | `channel-set-grid-bit` |
| Quick quantize | HAS | `channel-quick-quantize` |
| Clone channel | **TO BE ADDED** | FL API: `channels.cloneChannel()` |
| Delete channel | **TO BE ADDED** | FL API: `channels.removeChannel()` |
| Move channel up | **TO BE ADDED** | FL API: `channels.moveChannelUp()` |
| Move channel down | **TO BE ADDED** | FL API: `channels.moveChannelDown()` |
| Channel groups / filter | **TO BE ADDED** | FL API: `channels.getChannelGroup()`, `channels.setChannelGroup()` |
| Graph editor (per-step velocity/pan) | **TO BE ADDED** | FL API: `channels.getStepValue()`, `channels.setStepValue()` |
| Swing per channel | **TO BE ADDED** | FL API: `channels.setSwing()` |
| Burn MIDI from arpeggiator | **TO BE ADDED** | FL API: `recording.burnMIDITo()` |
| Sort by name/color/type | **TO BE ADDED** | FL API: `channels.sortByName()`, `channels.sortByColor()` |
| Load instrument into channel rack | **WALL** | No API to insert plugins. `[APPROACH: Template sessions with pre-loaded instruments]` |
| Replace instrument | **WALL** | No API to swap generators. `[APPROACH: Template sessions]` |
| Channel settings (wrapper, declicking, polyphony, gate) | **WALL** | Wrapper settings not exposed. `[APPROACH: FL internal Python script]` |
| **Score** | **20/29 = 69%** → after additions **29/29 = 100%** | |

---

## PIANO ROLL

| Operation | Status | Notes |
|---|---|---|
| Add notes | HAS | `piano-roll-add-notes` |
| Add chords | HAS | `piano-roll-add-chord` |
| Add arpeggio | HAS | `piano-roll-add-arpeggio` |
| Read notes | HAS | `piano-roll-read` |
| Clear all notes | HAS | `piano-roll-clear` |
| Delete notes | HAS | `piano-roll-delete-notes` |
| Duplicate time range | HAS | `piano-roll-duplicate` |
| Humanize | HAS | `piano-roll-humanize` |
| Quantize | HAS | `piano-roll-quantize` |
| Transpose | HAS | `piano-roll-transpose` |
| Status check | HAS | `piano-roll-status` |
| Slide / portamento notes | **TO BE ADDED** | FL API: slide flag on note events |
| Note color groups (MIDI channels) | **TO BE ADDED** | FL API: color param on note events |
| Snap to scale (root + scale) | **TO BE ADDED** | FL API: `midi.setKeySignature()` |
| Slice tool | **TO BE ADDED** | FL API: `midi.sliceNotes()` |
| Event editor (velocity curve, etc) | **TO BE ADDED** | FL API: `midi.setEventValue()` |
| Ghost notes | **WALL** | Visual feature, no programmatic control. `[APPROACH: FL internal script reads other channels]` |
| Time signatures per pattern | **WALL** | Visual grid helper only. `[APPROACH: N/A — cosmetic]` |
| Note properties dialog | **WALL** | UI-only. `[APPROACH: N/A — use note params directly]` |
| **Score** | **11/19 = 58%** → after additions **17/19 = 89%** | |

---

## MIXER

| Operation | Status | Notes |
|---|---|---|
| List all tracks | HAS | `mixer-all-tracks` |
| Track count | HAS | `mixer-count` |
| Track info | HAS | `mixer-track-info` |
| Set volume | HAS | `mixer-set-volume` |
| Set pan | HAS | `mixer-set-pan` |
| Mute / unmute | HAS | `mixer-mute` |
| Solo / unsolo | HAS | `mixer-solo` |
| Arm for recording | HAS | `mixer-arm` |
| Rename track | HAS | `mixer-set-name` |
| Set color | HAS | `mixer-set-color` |
| Stereo separation | HAS | `mixer-set-stereo-separation` |
| 3-band EQ read | HAS | `mixer-get-eq` |
| 3-band EQ set band | HAS | `mixer-set-eq-band` |
| FX slots listing | HAS | `mixer-fx-slots` |
| Route / sidechain | HAS | `mixer-route` |
| Send level | HAS | `mixer-set-send-level` |
| Link channel to mixer | HAS | `mixer-link-to-channel` |
| Add mixer track | **TO BE ADDED** | FL API: `mixers.addTrack()` |
| Delete mixer track | **TO BE ADDED** | FL API: `mixers.removeTrack()` |
| Reorder tracks | **TO BE ADDED** | FL API: `mixers.moveTrack()` |
| Invert phase | **TO BE ADDED** | FL API: `mixers.setPhaseInvert()` |
| Swap L/R channels | **TO BE ADDED** | FL API: `mixers.swapChannels()` |
| Track delay (manual offset) | **TO BE ADDED** | FL API: `mixers.setTrackDelay()` |
| FX slot: move up/down | **TO BE ADDED** | FL API: `mixers.moveFXSlot()` |
| FX slot: mute/bypass | **TO BE ADDED** | FL API: `mixers.muteFXSlot()` |
| FX slot: remove plugin | **TO BE ADDED** | FL API: `mixers.removeFXSlot()` |
| Dock tracks | **WALL** | Visual layout only. `[APPROACH: N/A — cosmetic]` |
| PDC (plugin delay comp) | **WALL** | Auto-managed by FL. `[APPROACH: N/A — automatic]` |
| Input/output routing | **WALL** | Hardware-dependent. `[APPROACH: N/A — needs ASIO]` |
| External audio input | **WALL** | Needs ASIO driver. `[APPROACH: Template sessions with pre-routed inputs]` |
| Surround sound routing | **WALL** | Hardware-dependent. `[APPROACH: N/A — needs surround interface]` |
| **Score** | **17/33 = 52%** → after additions **26/33 = 79%** | |

---

## PLUGIN CONTROL

| Operation | Status | Notes |
|---|---|---|
| List plugins on mixer track | HAS | `plugin-list-mixer-track` |
| Plugin name | HAS | `plugin-name` |
| Valid check | HAS | `plugin-is-valid` |
| Parameter count | HAS | `plugin-param-count` |
| List parameters | HAS | `plugin-params` |
| Get single parameter | HAS | `plugin-get-param` |
| Set single parameter | HAS | `plugin-set-param` |
| Find parameter by name | HAS | `plugin-find-param` |
| Preset count | HAS | `plugin-preset-count` |
| Next/prev preset | HAS | `plugin-next-preset`, `plugin-prev-preset` |
| Set preset by index | HAS | `plugin-set-preset` |
| Show/hide editor | HAS | `plugin-show-editor` |
| Remove plugin from FX slot | **TO BE ADDED** | FL API: `plugins.remove()` |
| Plugin presets (save/load file) | **TO BE ADDED** | FL API: `plugins.savePreset()`, `plugins.loadPreset()` |
| Load plugin into FX slot | **WALL** | Cannot insert plugins programmatically. `[APPROACH: Template sessions with pre-loaded plugins; or FL internal Python script that has browser access]` |
| Load instrument into channel | **WALL** | Cannot insert generators. `[APPROACH: Template sessions]` |
| Plugin GUI automation | **WALL** | Plugin UIs not scriptable. `[APPROACH: N/A — use plugin params via set-param]` |
| **Score** | **12/19 = 63%** → after additions **14/19 = 74%** | |

---

## PLAYLIST

| Operation | Status | Notes |
|---|---|---|
| List playlist tracks | HAS | `playlist-all-tracks` |
| Track count | HAS | `playlist-track-count` |
| Track info | HAS | `playlist-track-info` |
| List clips | HAS | `playlist-list-clips` |
| Delete clip | HAS | `playlist-delete-clip` |
| Place pattern clip | HAS | `playlist-place-pattern` |
| Mute track | HAS | `playlist-mute-track` |
| Solo track | HAS | `playlist-solo-track` |
| Rename track | HAS | `playlist-set-track-name` |
| Set track color | HAS | `playlist-set-track-color` |
| List markers | HAS | `playlist-list-markers` |
| Add marker | HAS | `playlist-add-marker` |
| Delete marker | HAS | `playlist-delete-marker` |
| Refresh playlist | HAS | `playlist-refresh` |
| Add playlist track | **TO BE ADDED** | FL API: `playlist.addTrack()` |
| Delete playlist track | **TO BE ADDED** | FL API: `playlist.removeTrack()` |
| Reorder tracks | **TO BE ADDED** | FL API: `playlist.moveTrack()` |
| Track grouping | **TO BE ADDED** | FL API: `playlist.setTrackGroup()` |
| Place audio clip | **TO BE ADDED** | FL API: `playlist.insertAudioClip()` |
| Create automation clip | **TO BE ADDED** | FL API: `playlist.insertAutomationClip()` |
| Edit automation points | **TO BE ADDED** | FL API: `playlist.setAutomationPoint()` |
| Performance mode | **WALL** | Live triggering not scriptable. `[APPROACH: N/A — live performance only]` |
| Picker panel | **WALL** | Visual only. `[APPROACH: N/A — cosmetic]` |
| Ghost notes from playlist | **WALL** | Visual only. `[APPROACH: N/A — cosmetic]` |
| **Score** | **14/24 = 58%** → after additions **21/24 = 88%** | |

---

## ARRANGEMENT

| Operation | Status | Notes |
|---|---|---|
| List arrangements | HAS | `arrangement-list` |
| Select arrangement | HAS | `arrangement-select` |
| Current arrangement | HAS | `arrangement-current` |
| Jump to marker | HAS | `arrangement-jump-marker` |
| Play time | HAS | `arrangement-play-time` |
| Create arrangement | **TO BE ADDED** | FL API: `arrangements.create()` |
| Delete arrangement | **TO BE ADDED** | FL API: `arrangements.remove()` |
| **Score** | **5/7 = 71%** → after additions **7/7 = 100%** | |

---

## AUTOMATION

| Operation | Status | Notes |
|---|---|---|
| Record channel volume auto | HAS | `automation-record-channel-volume` |
| Record channel pan auto | HAS | `automation-record-channel-pan` |
| Record mixer volume auto | HAS | `automation-record-mixer-volume` |
| Record plugin param auto | HAS | `automation-record-plugin-param` |
| Record tempo ramp | HAS | `automation-record-tempo` |
| Create automation clip | **TO BE ADDED** | FL API: `playlist.insertAutomationClip()` |
| Edit automation points | **TO BE ADDED** | FL API: `playlist.setAutomationPoint()` |
| LFO on automation | **TO BE ADDED** | FL API: `playlist.setLFO()` |
| **Score** | **5/8 = 63%** → after additions **8/8 = 100%** | |

---

## PROJECT

| Operation | Status | Notes |
|---|---|---|
| Metadata | HAS | `project-metadata` |
| Save | HAS | `project-save` |
| Save as | HAS | `project-save-as` |
| New project | HAS | `project-new` |
| Open project | HAS | `project-open` |
| Undo | HAS | `project-undo` |
| Redo | HAS | `project-redo` |
| Undo history | HAS | `project-undo-history` |
| Save undo checkpoint | HAS | `project-save-undo` |
| Render to disk | HAS | `project-render` |
| FL version | HAS | `project-version` |
| **Score** | **11/11 = 100%** | |

---

## GENERATORS (beats, chords, basslines, melodies)

| Operation | Status | Notes |
|---|---|---|
| 8 drum patterns | HAS | `gen-emit-drum-pattern-step-seq` |
| DnB grooves | HAS | `gen-emit-dnb-groove` |
| Chord progressions | HAS | `gen-emit-chord-progression` |
| Basslines | HAS | `gen-emit-bassline` |
| Arpeggios | HAS | `gen-emit-arpeggio` |
| Melodies | HAS | `gen-emit-melody` |
| Chord notes | HAS | `gen-chord-notes` |
| Scale notes | HAS | `gen-scale-notes` |
| List scales/chords/progressions/drums/DnB | HAS | `gen-list-*` |
| **Score** | **13/13 = 100%** | |

---

## VOICE → MIDI

| Operation | Status | Notes |
|---|---|---|
| List microphones | HAS | `voice-list-devices` |
| Record + transcribe | HAS | `voice-record-and-transcribe` |
| Voice to piano roll | HAS | `voice-to-piano-roll` |
| Notes to piano roll | HAS | `voice-notes-to-piano-roll` |
| Transcribe file | HAS | `voice-transcribe-file` |
| Interactive GUI | HAS | `voice-open-gui` |
| **Score** | **6/6 = 100%** | |

---

## AUDIO ANALYSIS

| Operation | Status | Notes |
|---|---|---|
| Tempo/key/onsets/loudness | HAS | `audio-analyze` |
| Audio to piano roll | HAS | `audio-melody-to-piano-roll` |
| Slice at onsets | HAS | `audio-slice` |
| MP3 → DnB flip | HAS | `song-to-dnb-flip` |
| **Score** | **4/4 = 100%** | |

---

## UI

| Operation | Status | Notes |
|---|---|---|
| Show window | HAS | `ui-show-window` |
| Hide window | HAS | `ui-hide-window` |
| Focused window | HAS | `ui-focused-window` |
| Open piano roll | HAS | `ui-open-piano-roll-for-channel` |
| Scroll to channel | HAS | `ui-scroll-to-channel` |
| Selected channel | HAS | `ui-selected-channel` |
| Hint message | HAS | `ui-hint` |
| **Score** | **7/7 = 100%** | |

---

## BROWSER

| Operation | Status | Notes |
|---|---|---|
| Browse audio files | **WALL** | `[APPROACH: FL internal Python script with browser access; or file system access outside FL]` |
| Browse plugins | **WALL** | `[APPROACH: FL internal script; or Plugin Manager XML parse]` |
| Browse presets | **WALL** | `[APPROACH: File system scan of preset folders]` |
| Drag-and-drop from browser | **WALL** | UI drag not scriptable. `[APPROACH: N/A — needs mouse]` |
| Plugin Manager (scan) | **WALL** | Settings dialog only. `[APPROACH: FL internal script]` |
| **Score** | **0/5 = 0%** | |

---

## RECORDING

| Operation | Status | Notes |
|---|---|---|
| Audio recording (mic, guitar) | **WALL** | Needs ASIO driver + real-time. `[APPROACH: Template sessions with pre-routed inputs; or record externally and import]` |
| MIDI recording (controller) | **WALL** | Needs controller + real-time. `[APPROACH: Template sessions with MIDI maps; or use voice-to-MIDI as substitute]` |
| **Score** | **0/2 = 0%** | |

---

## EXPORTING

| Operation | Status | Notes |
|---|---|---|
| Render to WAV/MP3/OGG | HAS | `project-render` |
| Export MIDI | **TO BE ADDED** | FL API: `file.exportMIDI()` |
| **Score** | **1/2 = 50%** → after additions **2/2 = 100%** | |

---

## EDISON

| Operation | Status | Notes |
|---|---|---|
| Record into Edison | **WALL** | Edison is a plugin, not scriptable. `[APPROACH: Record externally, import audio file]` |
| Edit audio in Edison | **WALL** | `[APPROACH: External audio editor (Audacity, etc)]` |
| **Score** | **0/2 = 0%** | |

---

## PATCHER

| Operation | Status | Notes |
|---|---|---|
| Load/Patch Patcher | **WALL** | UI-only module. `[APPROACH: N/A — complex modular routing needs GUI]` |
| **Score** | **0/1 = 0%** | |

---

## PERFORMANCE MODE

| Operation | Status | Notes |
|---|---|---|
| Trigger clips live | **WALL** | Not scriptable. `[APPROACH: N/A — live performance only]` |
| **Score** | **0/1 = 0%** | |

---

## THEMES / CUSTOMIZATION

| Operation | Status | Notes |
|---|---|---|
| Theme settings | **WALL** | Settings dialog. `[APPROACH: N/A — cosmetic]` |
| **Score** | **0/1 = 0%** | |

---

## HARDWARE / MIDI CONTROLLERS

| Operation | Status | Notes |
|---|---|---|
| MIDI controller linking | **WALL** | Settings dialog. `[APPROACH: N/A — needs physical controller]` |
| MIDI Out plugin | **WALL** | `[APPROACH: N/A — needs MIDI hardware]` |
| **Score** | **0/2 = 0%** | |

---

# GRAND TOTAL

| Category | Current | After Additions | Max (API) | Wall Items |
|---|---|---|---|---|
| Transport | 13/13 | 13/13 | 13 | 0 |
| Channel Rack | 20/29 | 29/29 | 29 | 0 |
| Piano Roll | 11/19 | 17/19 | 17 | 2 |
| Mixer | 17/33 | 26/33 | 26 | 7 |
| Plugin Control | 12/19 | 14/19 | 14 | 5 |
| Playlist | 14/24 | 21/24 | 21 | 3 |
| Arrangement | 5/7 | 7/7 | 7 | 0 |
| Automation | 5/8 | 8/8 | 8 | 0 |
| Project | 11/11 | 11/11 | 11 | 0 |
| Generators | 13/13 | 13/13 | 13 | 0 |
| Voice → MIDI | 6/6 | 6/6 | 6 | 0 |
| Audio Analysis | 4/4 | 4/4 | 4 | 0 |
| UI | 7/7 | 7/7 | 7 | 0 |
| Browser | 0/5 | 0/5 | 0 | 5 |
| Recording | 0/2 | 0/2 | 0 | 2 |
| Exporting | 1/2 | 2/2 | 2 | 0 |
| Edison | 0/2 | 0/2 | 0 | 2 |
| Patcher | 0/1 | 0/1 | 0 | 1 |
| Performance | 0/1 | 0/1 | 0 | 1 |
| Themes | 0/1 | 0/1 | 0 | 1 |
| Hardware | 0/2 | 0/2 | 0 | 2 |
| **TOTAL** | **139/193 = 72%** | **179/193 = 93%** | **179** | **31** |

---

# WHAT THE 31 WALL ITEMS MEAN FOR MERLIN

| Wall Item | Impact on Merlin | Potential Workaround |
|---|---|---|
| Load plugins into FX slots | **CRITICAL** — can't build vocal chains, effect chains | Template sessions with pre-loaded plugins |
| Load instruments into channel rack | **CRITICAL** — can't load synths, samplers | Template sessions with pre-loaded instruments |
| Replace instrument | HIGH — can't swap sounds | Template sessions |
| Plugin GUI automation | MEDIUM — can tweak params via set-param instead | Use plugin params directly |
| Wrapper settings (declicking, polyphony) | MEDIUM — some sound design settings | Manual or template |
| Dock mixer tracks | LOW — cosmetic only | N/A |
| PDC | LOW — auto-managed | N/A |
| Input/output routing | HIGH — needs ASIO hardware | Template sessions with pre-routed inputs |
| External audio input | **CRITICAL** — can't record vocals | Record externally, import audio |
| Surround sound | LOW — niche | N/A |
| Plugin loading (browser) | **CRITICAL** — can't browse/load plugins | FL internal Python script |
| Browser drag-and-drop | HIGH — UI interaction | N/A |
| Plugin Manager scan | LOW — one-time setup | N/A |
| Audio recording | **CRITICAL** — can't record live | Record externally, import |
| MIDI recording | HIGH — can't record controller | Use voice-to-MIDI as substitute |
| Edison record | HIGH — can't record into Edison | Record externally |
| Edison edit | MEDIUM — sample editing | External audio editor |
| Patcher | MEDIUM — modular routing | N/A |
| Performance mode | LOW — live only | N/A |
| Theme | LOW — cosmetic | N/A |
| MIDI controller linking | MEDIUM — hardware control | N/A |
| MIDI Out | LOW — hardware control | N/A |

---

# THE WORKAROUND STRATEGY

For the CRITICAL wall items, here's what actually works:

## 1. Template Sessions (immediate, no FL API change needed)
Pre-load plugins and instruments into FL project templates. Agent works within these templates. Not ideal but functional today.

**Templates needed:**
- `vocal_chain.flp` — Auto-Tune → compressor → EQ → reverb → delay
- `beat_making.flp` — Drum sampler + bass synth + pad synth + lead synth
- `mixing.flp` — Empty mixer with FX slots pre-loaded
- `full_production.flp` — Everything pre-loaded

## 2. FL Internal Python Scripts (medium effort, more capable)
FL Studio's piano roll scripts run INSIDE FL's Python environment. They have access to operations the external bridge doesn't. Building a comprehensive FL-internal script could expose more operations.

**What this could unlock:**
- Plugin loading via browser API
- Audio recording triggers
- Edison control
- Wrapper settings

**Effort:** High — different architecture, needs FL's Python API knowledge

## 3. External Audio Pipeline (for recording)
- Agent instructs user to record vocals externally (Audacity, phone, etc)
- Agent imports the audio file into FL
- Agent processes it with available tools (pitch detection, slicing, etc)

## 4. FL API Expansion (requires Image-Line)
Request Image-Line to expose:
- Plugin loading to scripts
- Audio recording to scripts
- Edison control to scripts

**This is the real unlock.** Everything else is workarounds.
