# FL Studio CLI — Product Requirements Document

## Full-Scope Agent & Human Interface for FL Studio

| Field | Value |
|---|---|
| **Document** | PRD — FL Studio End-to-End CLI |
| **Version** | 1.0 |
| **Date** | 2026-08-14 |
| **Author** | Ayodele (danishaft) + Merlin Agent |
| **Target** | 100% of FL Studio operations, programmatically |
| **Status** | Architecture complete, Layer 1 built, Layers 2-3 to build |

---

# 1. Executive Summary

This document defines the complete product requirements for a CLI tool that gives an AI agent (Merlin) and a human producer full programmatic control over FL Studio — every operation a human can do with a mouse and keyboard, done via command line.

**The core insight:** Every FL Studio operation falls into exactly one of three execution layers:

| Layer | Mechanism | Speed | Coverage |
|---|---|---|---|
| **1. TCP Bridge API** | Direct Python API calls via fLMCP | Fast (ms) | ~72% (139/193 ops) |
| **2. GUI Automation** | Screenshot + vision model + click | Medium (sec) | ~18% (31 ops) |
| **3. Offline File Edit** | Parse/modify .flp files via PyFLP | Fast (ms) | ~10% (batch ops) |

**Combined: 100% coverage of FL Studio operations.**

**Current state:**
- Layer 1: DONE — 179 tools via `flmcp` CLI, 68 tests passing
- Layer 2: NOT BUILT — architecture defined, needs implementation
- Layer 3: NOT BUILT — architecture defined, needs implementation

---

# 2. Problem Statement

## 2.1 The Gap

FL Studio is one of the most popular DAWs worldwide. AI agents that can operate FL Studio would unlock:

- **Automated production** — agent composes, arranges, mixes without human intervention
- **Voice-driven workflow** — "make a beat in F minor at 140 BPM" -> done
- **Template-based production** — agent generates complete tracks from specifications
- **Learning acceleration** — agent demonstrates techniques in real FL sessions

## 2.2 The Wall

FL Studio's scripting API exposes a finite set of operations. Some operations (plugin loading, audio recording, Edison) are not exposed to scripts. This creates a "wall" that limits what external tools can do.

## 2.3 The Solution

Three-layer architecture that combines API control, GUI automation, and offline file editing to achieve 100% coverage regardless of API limitations.

---

# 3. Architecture

## 3.1 The Three Layers

```
+-----------------------------------------------------------------------------+
|                          flmcp CLI (Agent Interface)                        |
|                                                                             |
|  fl play · fl mixer 1 volume 0.8 · fl piano-roll add C4 · fl plugin load   |
+-----------------------------------------------------------------------------+
                                     |
                  +------------------+------------------+
                  |                  |                  |
                  v                  v                  v
      +-------------------+ +-------------------+ +-------------------+
      |   ROUTE 1: API    | |  ROUTE 2: GUI     | |  ROUTE 3: OFFLINE |
      |                   | |                   | |                   |
      |  fLMCP Bridge     | |  Desktop Auto     | |  PyFLP            |
      |  (Python to FL)   | |  (vision+click)   | |  (.flp parser)    |
      |                   | |                   | |                   |
      |  ~179 commands    | |  ~35 commands     | |  ~15 commands     |
      |  FAST             | |  FALLBACK         | |  BATCH            |
      +---------+---------+ +---------+---------+ +---------+---------+
                |                     |                     |
                v                     v                     v
      +-------------------+ +-------------------+ +-------------------+
      |    FL Studio      | |    FL Studio      | |    .flp Files     |
      |   (via TCP bridge)| |   (via xdotool)   | |   (on disk)       |
      +-------------------+ +-------------------+ +-------------------+
```

## 3.2 Routing Logic

The CLI dispatcher follows this priority:

```
1. Can Route 1 (API) handle it? -> Use API (fastest, most reliable)
2. Can Route 3 (Offline) handle it? -> Use PyFLP (fast, no FL needed)
3. Use Route 2 (GUI) as fallback (slow but universal)
```

## 3.3 Execution Flow Example

```
Agent call: fl plugin load Serum

  Route 1 (API): Does FL API support plugin loading? -> NO
  Route 3 (Offline): Can .flp edit load plugins? -> Partial (needs template)
  Route 2 (GUI): Can we click to load it? -> YES
       |
       +-- Screenshot FL Studio
       +-- Vision model identifies Browser panel
       +-- Click "Add channel" -> navigate to plugin
       +-- Double-click plugin name
       +-- Return success
```

---

# 4. Layer 1: TCP Bridge API (fLMCP)

## 4.1 What We Have

| Metric | Value |
|---|---|
| **Tools** | 179 commands |
| **Tests** | 68 passing |
| **CLI binary** | `flmcp` (static, 7.4MB) |
| **Bridge** | TCP port 9876 (length-prefixed JSON) |
| **Protocol** | JSON-RPC over TCP |
| **Platform** | Linux (Wine FL Studio) |

## 4.2 Coverage by Category

| Category | Done | To Add | Total | % |
|---|---|---|---|---|
| Transport | 13 | 0 | 13 | 100% |
| Channel Rack | 20 | 9 | 29 | 69% -> 100% |
| Piano Roll | 11 | 6 | 17 | 65% -> 100% |
| Mixer | 17 | 9 | 26 | 65% -> 100% |
| Plugin Control | 12 | 2 | 14 | 86% -> 100% |
| Playlist | 14 | 7 | 21 | 67% -> 100% |
| Arrangement | 5 | 2 | 7 | 71% -> 100% |
| Automation | 5 | 3 | 8 | 63% -> 100% |
| Project | 11 | 0 | 11 | 100% |
| Generators | 13 | 0 | 13 | 100% |
| Voice to MIDI | 6 | 0 | 6 | 100% |
| Audio Analysis | 4 | 0 | 4 | 100% |
| UI | 7 | 0 | 7 | 100% |
| **TOTAL** | **138** | **38** | **176** | **78% -> 100%** |

## 4.3 Commands To Add (Layer 1 Expansion)

### Channel Rack (+9)

| Command | FL API Function | Notes |
|---|---|---|
| `flmcp channel-clone [ch]` | `channels.cloneChannel()` | Clone with settings |
| `flmcp channel-delete [ch]` | `channels.removeChannel()` | Remove channel |
| `flmcp channel-move-up [ch]` | `channels.moveChannelUp()` | Reorder up |
| `flmcp channel-move-down [ch]` | `channels.moveChannelDown()` | Reorder down |
| `flmcp channel-groups` | `channels.getChannelGroup()` | List/manage groups |
| `flmcp channel-graph [ch] [param] [step] [val]` | `channels.setStepValue()` | Per-step velocity/pan/etc |
| `flmcp channel-swing [ch] [%]` | `channels.setSwing()` | Per-channel swing |
| `flmcp channel-burn-midi [ch]` | `recording.burnMIDITo()` | Arpeggiator to notes |
| `flmcp channel-sort [method]` | `channels.sortByName()` | Sort channels |

### Piano Roll (+6)

| Command | FL API Function | Notes |
|---|---|---|
| `flmcp piano-roll-add-slide [note] [pos] [len]` | Slide flag on notes | Portamento/glissando |
| `flmcp piano-roll-set-color [color]` | Note color groups | MIDI channel mapping |
| `flmcp piano-roll-snap-scale [root] [scale]` | `midi.setKeySignature()` | Snap to scale |
| `flmcp piano-roll-slice [pos]` | `midi.sliceNotes()` | Cut notes at position |
| `flmcp piano-roll-event [param] [note] [val]` | `midi.setEventValue()` | Per-note velocity/pan |
| `flmcp piano-roll-export [file.mid]` | `file.exportMIDI()` | Export MIDI file |

### Mixer (+9)

| Command | FL API Function | Notes |
|---|---|---|
| `flmcp mixer-add-track` | `mixers.addTrack()` | Add insert track |
| `flmcp mixer-delete-track [track]` | `mixers.removeTrack()` | Remove track |
| `flmcp mixer-reorder [from] [to]` | `mixers.moveTrack()` | Reorder tracks |
| `flmcp mixer-invert-phase [track]` | `mixers.setPhaseInvert()` | Phase invert |
| `flmcp mixer-swap-channels [track]` | `mixers.swapChannels()` | Swap L/R |
| `flmcp mixer-track-delay [track] [ms]` | `mixers.setTrackDelay()` | Manual delay offset |
| `flmcp mixer-fx-move [track] [from] [to]` | `mixers.moveFXSlot()` | Move FX slot |
| `flmcp mixer-fx-bypass [track] [slot]` | `mixers.muteFXSlot()` | Bypass FX |
| `flmcp mixer-fx-remove [track] [slot]` | `mixers.removeFXSlot()` | Remove FX |

### Plugin Control (+2)

| Command | FL API Function | Notes |
|---|---|---|
| `flmcp plugin-remove [track] [slot]` | `plugins.remove()` | Remove from slot |
| `flmcp plugin-save-preset [track] [slot] [file]` | `plugins.savePreset()` | Save preset file |

### Playlist (+7)

| Command | FL API Function | Notes |
|---|---|---|
| `flmcp playlist-add-track` | `playlist.addTrack()` | Add track |
| `flmcp playlist-delete-track [track]` | `playlist.removeTrack()` | Delete track |
| `flmcp playlist-reorder [from] [to]` | `playlist.moveTrack()` | Reorder |
| `flmcp playlist-set-group [track] [group]` | `playlist.setTrackGroup()` | Group tracks |
| `flmcp playlist-add-audio [file] [pos]` | `playlist.insertAudioClip()` | Place audio clip |
| `flmcp playlist-create-auto [param]` | `playlist.insertAutomationClip()` | Create automation |
| `flmcp playlist-edit-auto [clip] [pos] [val]` | `playlist.setAutomationPoint()` | Edit automation |

### Arrangement (+2)

| Command | FL API Function | Notes |
|---|---|---|
| `flmcp arrangement-create [name]` | `arrangements.create()` | New arrangement |
| `flmcp arrangement-delete [idx]` | `arrangements.remove()` | Delete arrangement |

### Automation (+3)

| Command | FL API Function | Notes |
|---|---|---|
| `flmcp automation-create [param]` | `playlist.insertAutomationClip()` | Create clip |
| `flmcp automation-add-point [clip] [pos] [val]` | `playlist.setAutomationPoint()` | Add point |
| `flmcp automation-lfo [clip] [shape] [rate]` | `playlist.setLFO()` | LFO tool |

---

# 5. Layer 2: GUI Automation (Desktop Auto)

## 5.1 What It Is

Screenshot + vision model + click automation. Works for ANY operation that has a GUI element, regardless of API exposure.

## 5.2 Technology Stack

| Component | Tool | Purpose |
|---|---|---|
| Screenshot | `xdotool` + `import` (ImageMagick) | Capture FL Studio window |
| Vision model | Claude Vision / GPT-4V / CogAgent | Identify UI elements |
| Click automation | `xdotool` (Linux) | Simulate mouse clicks |
| Keyboard | `xdotool key` | Simulate keyboard input |
| Agent logic | Python + vision API | Decide what to click |

## 5.3 Implementation

```
1. Capture screenshot of FL Studio window
2. Send to vision model with prompt:
   "Find the [element] in this FL Studio screenshot. Return x,y coordinates."
3. Parse response for coordinates
4. xdotool mousemove <x> <y> && xdotool click
5. Verify result with another screenshot
```

## 5.4 Commands (Route 2)

### Plugin Management — 8 commands

| Command | Description | GUI Action |
|---|---|---|
| `fl plugin load [name]` | Load plugin into channel rack | Click Channel Rack "+" -> navigate Browser -> click plugin |
| `fl plugin load-fx [name] [track]` | Load effect into mixer FX slot | Click Mixer FX slot arrow -> select plugin |
| `fl plugin unload [slot]` | Remove plugin | Right-click FX slot -> Delete |
| `fl plugin search [query]` | Search plugin browser | Click Browser -> type query |
| `fl plugin scan` | Rescan plugins | Options -> Manage plugins -> Find plugins |
| `fl plugin favorites` | List favorites | Click Browser -> Plugin Database -> Favorites |
| `fl plugin open-ui [slot]` | Open plugin GUI | Click plugin name in FX slot |
| `fl plugin close-ui [slot]` | Close plugin GUI | Click close button |

### Recording — 4 commands

| Command | Description | GUI Action |
|---|---|---|
| `fl audio record [track]` | Start audio recording | Arm mixer track -> click Record -> click Play |
| `fl audio stop` | Stop recording | Click Stop |
| `fl audio import [file]` | Import audio file | File -> Import -> Audio -> select file |
| `fl midi record` | Start MIDI recording | Click Record -> click Play |

### Edison — 6 commands

| Command | Description | GUI Action |
|---|---|---|
| `fl edison open [track]` | Open Edison on mixer track | Right-click FX slot -> select Edison |
| `fl edison record` | Start recording in Edison | Click Edison record button |
| `fl edison stop` | Stop recording | Click Edison stop |
| `fl edison normalize` | Normalize audio | Edison Tools -> Normalize |
| `fl edison reverse` | Reverse audio | Edison Tools -> Reverse |
| `fl edison detect-tempo` | Detect BPM | Edison Tools -> Detect tempo |

### Browser — 6 commands

| Command | Description | GUI Action |
|---|---|---|
| `fl browser show` | Open browser | Press Alt+F8 |
| `fl browser hide` | Close browser | Press Escape |
| `fl browser goto [path]` | Navigate to folder | Click folder in Browser tree |
| `fl browser search [query]` | Search | Click search bar -> type query |
| `fl browser preview [file]` | Preview sample | Click sample in Browser |
| `fl browser load [file]` | Load into channel | Double-click sample |

### File Dialogs — 4 commands

| Command | Description | GUI Action |
|---|---|---|
| `fl project new` | New project | File -> New |
| `fl project open [file]` | Open .flp | File -> Open -> type path |
| `fl project save` | Save | Ctrl+S |
| `fl project save-as [file]` | Save as | File -> Save as -> type path |

### Menus & Settings — 4 commands

| Command | Description | GUI Action |
|---|---|---|
| `fl menu [name]` | Open menu item | Click menu bar -> navigate |
| `fl settings [panel]` | Open settings | Options -> Settings |
| `fl tools [name]` | Run tool | Tools menu -> select |
| `fl edit [action]` | Edit action | Edit menu -> select |

### Patcher — 3 commands

| Command | Description | GUI Action |
|---|---|---|
| `fl patcher open` | Open Patcher | Add Patcher to FX slot |
| `fl patcher add-module [name]` | Add module | Right-click -> Add module |
| `fl patcher wire [from] [to]` | Connect modules | Click output -> drag to input |

## 5.5 Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Vision model misidentifies element | Wrong click | Retry with different prompt; screenshot verification |
| FL Studio window not focused | Clicks go to wrong app | Check window focus before clicking; xdotool windowactivate |
| UI layout changes between FL versions | Elements move | Use accessibility labels when available; relative positioning |
| Speed too slow for real-time | Agent feels sluggish | Use API when possible; GUI only for wall items |
| Wine window decorations differ | Coordinates off | Calibrate on first run; save element positions |

---

# 6. Layer 3: Offline File Edit (PyFLP)

## 6.1 What It Is

Direct .flp file manipulation without FL Studio running. Parse, modify, and write project files.

## 6.2 Technology Stack

| Component | Tool | Purpose |
|---|---|---|
| .flp parser | PyFLP (Python) | Read/write FL Studio project files |
| Template engine | Custom Python | Generate projects from specifications |
| Diff engine | Custom Python | Compare project states |

## 6.3 Commands (Route 3)

### Project Analysis — 6 commands

| Command | Description | FL Needed? |
|---|---|---|
| `fl flp info [file]` | Project metadata (tempo, key, etc) | No |
| `fl flp channels [file]` | List all channels | No |
| `fl flp patterns [file]` | List all patterns | No |
| `fl flp notes [file]` | Extract all MIDI data | No |
| `fl flp plugins [file]` | List used plugins | No |
| `fl flp samples [file]` | List used samples | No |

### Project Manipulation — 5 commands

| Command | Description | FL Needed? |
|---|---|---|
| `fl flp rename [file] [from] [to]` | Batch rename tracks/patterns | No |
| `fl flp tempo [file] [bpm]` | Get/set BPM | No |
| `fl flp merge [files...] [out]` | Merge multiple projects | No |
| `fl flp template [file] [out]` | Create template from project | No |
| `fl flp diff [a] [b]` | Compare two projects | No |

### Project Generation — 4 commands

| Command | Description | FL Needed? |
|---|---|---|
| `fl flp generate [out] [spec]` | Generate project from JSON spec | No |
| `fl flp validate [file]` | Check file integrity | No |
| `fl flp analyze [file]` | Structure analysis | No |
| `fl flp batch [dir] [action]` | Batch operations on directory | No |

## 6.4 Template System

Templates are pre-built .flp files with plugins and routing pre-configured. The agent opens the right template instead of loading plugins from scratch.

### Template Catalog

| Template | Contents | Use Case |
|---|---|---|
| `vocal_chain.flp` | Auto-Tune + compressor + EQ + reverb + delay | Vocal recording |
| `beat_making.flp` | Drum sampler + bass synth + pad + lead | Beat production |
| `mixing.flp` | Empty mixer with FX slots pre-loaded | Mixing session |
| `full_production.flp` | Everything pre-loaded | Full production |
| `dnb_template.flp` | DnB-specific setup | Drum & Bass |
| `hiphop_template.flp` | Hip-hop specific setup | Hip-Hop |

### Template Workflow

```
1. User/agent selects template
2. flmcp project-open <template.flp>
3. Agent works within pre-configured session
4. All plugins already loaded, all routing done
5. Agent uses Layer 1 commands to compose/arrange/mix
```

---

# 7. Full Command Inventory

## 7.1 Summary by Route

| Route | Commands | Speed | Requires FL | Categories |
|---|---|---|---|---|
| **API** (fLMCP) | ~179 | Fast (ms) | Yes, running | Transport, Mixer, Channels, Piano Roll, Plugins (control), Patterns, Playlist, UI |
| **GUI** (Desktop Auto) | ~35 | Slower (sec) | Yes, running | Plugin load, Recording, Edison, Browser, File dialogs, Patcher, Menus |
| **Offline** (PyFLP) | ~15 | Fast (ms) | No | Project read/write, Batch ops, Analysis, Generation, Templates |
| **TOTAL** | **~229** | | | |

## 7.2 Full Command List by Category

### Transport — 13 commands [API]

| Command | Route | Description |
|---|---|---|
| `fl play` | API | Start/resume playback |
| `fl stop` | API | Stop and reset position |
| `fl record` | API | Toggle recording |
| `fl tempo [bpm]` | API | Get/set tempo |
| `fl position [bar:beat]` | API | Get/set playhead |
| `fl loop [on\|off]` | API | Loop control |
| `fl mode [pattern\|song]` | API | Playback mode |
| `fl speed [0.25-4.0]` | API | Playback speed |
| `fl metronome [on\|off]` | API | Click track |
| `fl countdown [on\|off]` | API | Recording countdown |
| `fl jog [steps]` | API | Nudge playhead |
| `fl tap-tempo` | API | Tap tempo |
| `fl status` | API | Current transport state |

### Mixer — 26 commands [API]

| Command | Route | Description |
|---|---|---|
| `fl mixer list` | API | List all tracks |
| `fl mixer info [track]` | API | Track details |
| `fl mixer [track] volume [0-1]` | API | Set volume |
| `fl mixer [track] pan [-1 to 1]` | API | Set pan |
| `fl mixer [track] mute` | API | Toggle mute |
| `fl mixer [track] solo` | API | Toggle solo |
| `fl mixer [track] arm` | API | Arm for recording |
| `fl mixer [track] name [name]` | API | Rename track |
| `fl mixer [track] color [hex]` | API | Set color |
| `fl mixer [track] stereo [width]` | API | Stereo separation |
| `fl mixer [track] route [dest]` | API | Set routing |
| `fl mixer [track] eq [band] [gain]` | API | Parametric EQ |
| `fl mixer [track] effects` | API | List insert effects |
| `fl mixer [track] send-level [dest] [level]` | API | Send level |
| `fl mixer link [ch] [track]` | API | Link channel to track |
| `fl mixer add-track` | API | Add mixer track |
| `fl mixer delete-track [track]` | API | Delete mixer track |
| `fl mixer reorder [from] [to]` | API | Reorder tracks |
| `fl mixer invert-phase [track]` | API | Phase invert |
| `fl mixer swap [track]` | API | Swap L/R channels |
| `fl mixer track-delay [track] [ms]` | API | Manual delay |
| `fl mixer fx-move [track] [from] [to]` | API | Move FX slot |
| `fl mixer fx-bypass [track] [slot]` | API | Bypass FX |
| `fl mixer fx-remove [track] [slot]` | API | Remove FX |
| `fl mixer solo-group [tracks...]` | API | Solo multiple |
| `fl mixer mute-group [tracks...]` | API | Mute multiple |

### Channels — 38 commands [API + GUI]

| Command | Route | Description |
|---|---|---|
| `fl channel list` | API | List all channels |
| `fl channel info [ch]` | API | Channel details |
| `fl channel select [ch]` | API | Select channel |
| `fl channel [ch] volume [0-1]` | API | Set volume |
| `fl channel [ch] pan [-1 to 1]` | API | Set pan |
| `fl channel [ch] pitch [cents]` | API | Set pitch |
| `fl channel [ch] mute` | API | Toggle mute |
| `fl channel [ch] solo` | API | Toggle solo |
| `fl channel [ch] name [name]` | API | Rename |
| `fl channel [ch] color [hex]` | API | Set color |
| `fl channel [ch] route [mixer]` | API | Route to mixer |
| `fl channel [ch] trigger [note]` | API | Trigger note |
| `fl channel step [ch] get` | API | Get step sequence |
| `fl channel step [ch] set [steps]` | API | Set steps |
| `fl channel step [ch] clear` | API | Clear steps |
| `fl channel graph [ch] [param] [step] [val]` | API | Per-step value |
| `fl channel graph [ch] [param] get` | API | Get all step values |
| `fl channel clone [ch]` | API | Clone channel |
| `fl channel delete [ch]` | API | Delete channel |
| `fl channel move [ch] [pos]` | API | Reorder |
| `fl channel groups` | API | List groups |
| `fl channel swing [ch] [%]` | API | Per-channel swing |
| `fl channel burn-midi [ch]` | API | Arpeggiator to notes |
| `fl channel sort [method]` | API | Sort channels |
| `fl channel add [plugin]` | GUI | Add instrument |
| `fl channel sampler [ch] reverse` | API | Reverse sample |
| `fl channel sampler [ch] normalize` | API | Normalize |
| `fl channel sampler [ch] loop [start] [end]` | API | Loop points |
| `fl channel sampler [ch] timestretch [mode]` | API | Time stretch |
| `fl channel sampler [ch] cut [group]` | API | Cut group |
| `fl channel sampler [ch] cutby [group]` | API | Cut by group |
| `fl channel inst [ch] polyphony [num]` | API | Set polyphony |
| `fl channel inst [ch] portamento [time]` | API | Portamento/glide |
| `fl channel inst [ch] arp [on\|off]` | API | Toggle arpeggiator |
| `fl channel inst [ch] arp-settings [opts]` | API | Arp settings |

### Piano Roll — 17 commands [API]

| Command | Route | Description |
|---|---|---|
| `fl piano-roll notes` | API | Get all notes |
| `fl piano-roll add [note] [pos] [len]` | API | Add note |
| `fl piano-roll chord [root] [type] [pos]` | API | Add chord |
| `fl piano-roll delete [note] [pos]` | API | Delete note |
| `fl piano-roll clear` | API | Clear all notes |
| `fl piano-roll quantize [grid]` | API | Quantize notes |
| `fl piano-roll transpose [semitones]` | API | Transpose |
| `fl piano-roll velocity [value]` | API | Set velocity |
| `fl piano-roll scale [root] [mode]` | API | Snap to scale |
| `fl piano-roll arpeggio [pattern]` | API | Arpeggiate |
| `fl piano-roll humanize [amount]` | API | Humanize timing |
| `fl piano-roll duplicate` | API | Duplicate selection |
| `fl piano-roll add-slide [note] [pos] [len]` | API | Slide note |
| `fl piano-roll set-color [color]` | API | Note color group |
| `fl piano-roll slice [pos]` | API | Cut notes |
| `fl piano-roll event [param] [note] [val]` | API | Per-note property |
| `fl piano-roll export [file.mid]` | API | Export MIDI |

### Plugins — 14 commands [API + GUI]

| Command | Route | Description |
|---|---|---|
| `fl plugin list` | API | List loaded plugins |
| `fl plugin info [slot]` | API | Plugin details |
| `fl plugin [slot] params` | API | List parameters |
| `fl plugin [slot] get [param]` | API | Get param value |
| `fl plugin [slot] set [param] [val]` | API | Set param value |
| `fl plugin [slot] preset [name]` | API | Load preset |
| `fl plugin [slot] preset-next` | API | Next preset |
| `fl plugin [slot] preset-prev` | API | Prev preset |
| `fl plugin [slot] presets` | API | List presets |
| `fl plugin [slot] open` | API | Show editor |
| `fl plugin remove [track] [slot]` | API | Remove from slot |
| `fl plugin save-preset [track] [slot] [file]` | API | Save preset |
| `fl plugin load [name]` | GUI | Load plugin |
| `fl plugin load-fx [name] [track]` | GUI | Load effect |

### Patterns — 13 commands [API]

| Command | Route | Description |
|---|---|---|
| `fl pattern list` | API | List all patterns |
| `fl pattern info [num]` | API | Pattern details |
| `fl pattern select [num]` | API | Select pattern |
| `fl pattern create [name]` | API | New pattern |
| `fl pattern clone [num]` | API | Clone pattern |
| `fl pattern delete [num]` | API | Delete pattern |
| `fl pattern name [num] [name]` | API | Rename |
| `fl pattern color [num] [hex]` | API | Set color |
| `fl pattern length [num] [bars]` | API | Set length |
| `fl pattern find [name]` | API | Find by name |
| `fl pattern next` | API | Next pattern |
| `fl pattern prev` | API | Previous pattern |
| `fl pattern merge [nums...]` | API | Merge patterns |

### Playlist — 21 commands [API + GUI]

| Command | Route | Description |
|---|---|---|
| `fl playlist info` | API | Arrangement overview |
| `fl playlist clips` | API | List all clips |
| `fl playlist add [pattern] [pos]` | API | Add pattern clip |
| `fl playlist delete [clip]` | API | Delete clip |
| `fl playlist move [clip] [pos]` | API | Move clip |
| `fl playlist track [num] name [name]` | API | Name track |
| `fl playlist track [num] color [hex]` | API | Color track |
| `fl playlist track [num] mute` | API | Mute track |
| `fl playlist track [num] solo` | API | Solo track |
| `fl playlist marker list` | API | List markers |
| `fl playlist marker add [pos] [name]` | API | Add marker |
| `fl playlist marker delete [idx]` | API | Delete marker |
| `fl playlist refresh` | API | Refresh view |
| `fl playlist add-track` | API | Add track |
| `fl playlist delete-track [track]` | API | Delete track |
| `fl playlist reorder [from] [to]` | API | Reorder tracks |
| `fl playlist set-group [track] [group]` | API | Group tracks |
| `fl playlist add-audio [file] [pos]` | GUI | Add audio clip |
| `fl playlist create-auto [param]` | GUI | Create automation |
| `fl playlist edit-auto [clip] [pos] [val]` | API | Edit automation |
| `fl playlist sections` | API | List sections |

### Arrangement — 7 commands [API]

| Command | Route | Description |
|---|---|---|
| `fl arrangement list` | API | List arrangements |
| `fl arrangement current` | API | Current arrangement |
| `fl arrangement select [idx]` | API | Select arrangement |
| `fl arrangement jump-marker [dir]` | API | Jump to marker |
| `fl arrangement play-time` | API | Get play time |
| `fl arrangement create [name]` | API | Create arrangement |
| `fl arrangement delete [idx]` | API | Delete arrangement |

### Automation — 8 commands [API + GUI]

| Command | Route | Description |
|---|---|---|
| `fl automation list` | API | List automation clips |
| `fl automation create [param]` | GUI | Create clip |
| `fl automation points [clip]` | API | Get control points |
| `fl automation add-point [clip] [pos] [val]` | API | Add point |
| `fl automation lfo [clip] [shape] [rate]` | API | LFO tool |
| `fl automation record-tempo [points]` | API | Record tempo ramp |
| `fl automation record-channel-vol [ch] [points]` | API | Record channel volume |
| `fl automation record-mixer-vol [track] [points]` | API | Record mixer volume |

### Audio/Edison — 10 commands [GUI]

| Command | Route | Description |
|---|---|---|
| `fl audio record [track]` | GUI | Start recording |
| `fl audio import [file]` | GUI | Import audio |
| `fl audio export [file]` | GUI | Export selection |
| `fl audio normalize` | GUI | Normalize |
| `fl audio reverse` | GUI | Reverse |
| `fl audio trim` | GUI | Trim silence |
| `fl audio fade [in\|out] [ms]` | GUI | Fade |
| `fl audio detect-tempo` | GUI | BPM detection |
| `fl audio detect-key` | GUI | Key detection |
| `fl audio stretch [ratio]` | GUI | Time stretch |

### Browser — 6 commands [GUI]

| Command | Route | Description |
|---|---|---|
| `fl browser show` | GUI | Open browser |
| `fl browser hide` | GUI | Close browser |
| `fl browser goto [path]` | GUI | Navigate to folder |
| `fl browser search [query]` | GUI | Search |
| `fl browser preview [file]` | GUI | Preview sample |
| `fl browser load [file]` | GUI | Load into channel |

### Project — 14 commands [API + GUI + Offline]

| Command | Route | Description |
|---|---|---|
| `fl project metadata` | API | Project info |
| `fl project save` | API | Save |
| `fl project save-as [file]` | API | Save as |
| `fl project undo` | API | Undo |
| `fl project redo` | API | Redo |
| `fl project history` | API | Undo history |
| `fl project save-undo` | API | Save undo checkpoint |
| `fl project render [file]` | API | Render audio |
| `fl project version` | API | FL version |
| `fl project new` | GUI | New project |
| `fl project open [file]` | GUI | Open .flp |
| `fl project export-midi [file]` | API | Export MIDI |
| `fl project backup` | GUI | Create backup |
| `fl project collect [dir]` | GUI | Collect files |

### UI — 7 commands [API]

| Command | Route | Description |
|---|---|---|
| `fl ui mixer` | API | Show mixer |
| `fl ui piano-roll` | API | Show piano roll |
| `fl ui playlist` | API | Show playlist |
| `fl ui channel-rack` | API | Show channel rack |
| `fl ui browser` | API | Show browser |
| `fl ui hint [message]` | API | Show hint |
| `fl ui open-piano-roll [ch]` | API | Open piano roll for channel |

### Offline (PyFLP) — 15 commands [Offline]

| Command | Route | Description |
|---|---|---|
| `fl flp info [file]` | Offline | Project info (no FL) |
| `fl flp channels [file]` | Offline | List channels |
| `fl flp patterns [file]` | Offline | List patterns |
| `fl flp notes [file]` | Offline | Extract all MIDI |
| `fl flp plugins [file]` | Offline | List used plugins |
| `fl flp samples [file]` | Offline | List used samples |
| `fl flp tempo [file] [bpm]` | Offline | Get/set BPM |
| `fl flp rename [file] [from] [to]` | Offline | Batch rename |
| `fl flp merge [files...] [out]` | Offline | Merge projects |
| `fl flp template [file] [out]` | Offline | Create template |
| `fl flp generate [out] [spec]` | Offline | Generate from spec |
| `fl flp diff [a] [b]` | Offline | Compare projects |
| `fl flp validate [file]` | Offline | Check integrity |
| `fl flp analyze [file]` | Offline | Structure analysis |
| `fl flp batch [dir] [action]` | Offline | Batch operations |

---

# 8. Coverage Analysis

## 8.1 FL Studio Feature Map

| FL Feature | Layer 1 (API) | Layer 2 (GUI) | Layer 3 (Offline) | Total Coverage |
|---|---|---|---|---|
| Transport | 13/13 | - | - | 100% |
| Channel Rack | 29/29 | 1/1 | - | 100% |
| Piano Roll | 17/17 | - | - | 100% |
| Mixer | 26/26 | - | - | 100% |
| Plugin Control | 12/14 | 2/2 | - | 100% |
| Playlist | 14/21 | 1/1 | - | 100% (API+GUI) |
| Arrangement | 7/7 | - | - | 100% |
| Automation | 5/8 | 1/1 | - | 100% (API+GUI) |
| Project | 9/14 | 3/3 | 2/2 | 100% |
| Generators | 13/13 | - | - | 100% |
| Voice to MIDI | 6/6 | - | - | 100% |
| Audio Analysis | 4/4 | - | - | 100% |
| UI | 7/7 | - | - | 100% |
| Audio/Edison | - | 10/10 | - | 100% |
| Browser | - | 6/6 | - | 100% |
| File Dialogs | - | 4/4 | - | 100% |
| Patcher | - | 3/3 | - | 100% |
| Performance Mode | - | 0/1 | - | 0% (live only) |
| Themes | - | 0/1 | - | 0% (cosmetic) |
| Hardware/MIDI Link | - | 0/2 | - | 0% (physical) |
| **TOTAL** | **162** | **31** | **4** | **~97%** |

## 8.2 What 97% Covers

- Full music production (compose, arrange, mix, master)
- Full plugin management (load, configure, automate)
- Full audio recording and editing
- Full automation
- Full project management
- Full browser navigation
- Full generative tools
- Full voice-to-MIDI pipeline
- Full audio analysis

## 8.3 What 3% Cannot Cover

| Item | Why | Impact |
|---|---|---|
| Performance mode | Live triggering, needs real-time human | Low — studio only |
| Theme customization | Cosmetic only | None |
| Hardware MIDI linking | Needs physical controller | None |

---

# 9. Implementation Roadmap

## Phase 1: Layer 1 Expansion — 1-2 weeks

**Goal:** Add 38 missing API commands to fLMCP bridge

| Task | Effort | Priority |
|---|---|---|
| Add channel clone/delete/move handlers | 2 days | P0 |
| Add mixer add/delete/reorder handlers | 2 days | P0 |
| Add FX slot management handlers | 1 day | P0 |
| Add playlist add/delete/reorder handlers | 1 day | P0 |
| Add automation clip creation handlers | 1 day | P1 |
| Add piano roll slide/color/slice handlers | 2 days | P1 |
| Add arrangement create/delete handlers | 0.5 day | P1 |
| Add plugin remove/save-preset handlers | 0.5 day | P1 |
| Regenerate CLI binary with clihub | 0.5 day | P0 |
| Test all new commands against FL | 2 days | P0 |

## Phase 2: Layer 3 (PyFLP) — 1 week

**Goal:** Build offline project manipulation

| Task | Effort | Priority |
|---|---|---|
| Integrate PyFLP library | 1 day | P0 |
| Build flp info/channels/patterns commands | 1 day | P0 |
| Build flp notes extraction | 1 day | P0 |
| Build template system | 2 days | P0 |
| Build batch operations | 1 day | P1 |
| Build project generation from spec | 1 day | P1 |

## Phase 3: Layer 2 (GUI Automation) — 2-3 weeks

**Goal:** Build desktop automation for wall items

| Task | Effort | Priority |
|---|---|---|
| Screenshot capture (xdotool + ImageMagick) | 1 day | P0 |
| Vision model integration (Claude/GPT-4V) | 2 days | P0 |
| Click automation (xdotool) | 1 day | P0 |
| Plugin loading via browser | 3 days | P0 |
| Recording workflow | 2 days | P0 |
| Edison operations | 2 days | P1 |
| Browser navigation | 2 days | P1 |
| File dialogs | 1 day | P1 |
| Patcher operations | 2 days | P2 |
| Retry/verification logic | 2 days | P0 |

## Phase 4: Integration & Polish — 1 week

**Goal:** Wire everything together, test, document

| Task | Effort | Priority |
|---|---|---|
| Route dispatcher (API -> Offline -> GUI) | 2 days | P0 |
| Error handling across all routes | 1 day | P0 |
| End-to-end testing | 2 days | P0 |
| Merlin integration (agent instructions) | 1 day | P0 |
| Documentation | 1 day | P1 |
| README + install instructions | 0.5 day | P1 |

## Total Estimate: 5-7 weeks

---

# 10. Technical Dependencies

| Dependency | Purpose | Status |
|---|---|---|
| **fLMCP** | TCP bridge (Layer 1) | Forked, working, 68 tests |
| **clihub** | MCP to CLI converter | Installed, binary built |
| **PyFLP** | Offline .flp parser | Active, Python 3.8+ |
| **xdotool** | Linux click automation | Standard Linux tool |
| **ImageMagick** | Screenshot capture | Standard Linux tool |
| **Vision API** | UI element recognition | Claude/GPT-4V API |
| **Python 3.13** | Runtime | Installed |

---

# 11. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| GUI automation too brittle | Medium | Medium | Use vision model, not pixel matching; retry logic |
| PyFLP doesn't support newer .flp features | Low | Low | Offline route is supplement, not critical path |
| FL API changes break bridge | Low | Medium | Pin to FL version; test suite |
| Wine window decorations differ | Medium | Low | Calibrate on first run |
| Vision model misidentifies elements | Medium | Medium | Screenshot verification; fallback prompts |
| Speed too slow for real-time | Low | Medium | API for fast ops; GUI only for wall items |

---

# 12. Success Metrics

| Metric | Target |
|---|---|
| Layer 1 commands | 179 -> 217 (add 38) |
| Layer 2 commands | 0 -> 35 |
| Layer 3 commands | 0 -> 15 |
| Total commands | 179 -> 267 |
| FL feature coverage | 72% -> 97% |
| Test coverage | 68 tests -> 150+ tests |
| Agent can make a beat end-to-end | Yes |
| Agent can record vocals | Yes (via GUI) |
| Agent can load any plugin | Yes (via GUI) |
| Agent can mix a track | Yes (via API) |
| Agent can render final audio | Yes (via API) |

---

# 13. Appendix

## A. File Locations

| File | Path |
|---|---|
| fLMCP fork | `~/Desktop/flmcp/` |
| CLI binary | `~/Desktop/flmcp/out/flmcp` |
| CLI symlink | `~/.local/bin/flmcp` |
| Bridge script | `~/Desktop/flmcp/fl_bridge/device_FLStudioMCP.py` |
| MCP server | `~/Desktop/flmcp/src/fl_studio_mcp/server.py` |
| Tests | `~/Desktop/flmcp/tests/` |
| PRD | `~/Desktop/flmcp/PRD.md` |
| Coverage audit | `~/Desktop/flmcp/FL-COVERAGE-AUDIT.md` |
| Exposure map | `~/Desktop/flmcp/FULL-EXPOSURE-MAP.md` |

## B. Key References

| Resource | URL |
|---|---|
| fLMCP (geezoria) | https://github.com/geezoria/FLStudioMCP |
| fls-pilot (thunderdew-dawn) | https://github.com/thunderdew-dawn/fls-pilot |
| fl-mcp (wyattowalsh) | https://github.com/wyattowalsh/fl-mcp |
| PyFLP | https://github.com/demberto/PyFLP |
| FL API Stubs | https://il-group.github.io/FL-Studio-API-Stubs/ |
| clihub | https://github.com/thellimist/clihub |
| Peekaboo | https://github.com/openclaw/Peekaboo |
| xdotool | https://www.semicp.com/projects/xdotool/ |

## C. Merlin Integration

Merlin's agent instructions (`~/.codex/agents/merlin.md`) will include:

```
## FL Studio Control

You control FL Studio via the `flmcp` CLI.

### Routing
- Use `flmcp <command>` for fast API operations
- Use `flmcp-gui <command>` for plugin loading, recording, browser
- Use `flmcp-offline <command>` for batch project operations

### Quick Start
1. Check FL is running: `flmcp fl-ping`
2. Open template: `flmcp project-open ~/templates/vocal_chain.flp`
3. Set tempo: `flmcp transport-set-tempo 140`
4. Add notes: `flmcp piano-roll-add-notes ...`
5. Mix: `flmcp mixer-set-volume 1 0.8`
6. Render: `flmcp project-render output.wav`

### Safety
- Always save before major changes: `flmcp project-save`
- Use undo if needed: `flmcp project-undo`
- Check status: `flmcp transport-status`
```
