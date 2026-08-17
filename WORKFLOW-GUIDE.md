# Merlin Workflow Guide — 159 Tools A → Z

How Merlin produces a track, from the first thing a producer does to the final
render. Every section = a tool group that ALREADY EXISTS and works.

## How every tool works (the mechanism)

One pattern for all 159 tools:

```
You ask Merlin          MCP tool call            TCP bridge (127.0.0.1:9876)
"start playback"  -->  transport_play()   -->   "transport.start"
                                                    |
                                          device_FLStudioMCP.py in FL Studio
                                          (_HANDLERS dict -> FL API call -> JSON)
                                                    |
                                            playback starts, JSON returned
```

- Tool names here use MCP form (`transport_play`); the CLI spells them kebab-case (`flmcp transport-play`)
- Every call returns a JSON dict (status, values, errors)
- If FL isn't running or the bridge isn't loaded, calls return `bridge unavailable` — see README troubleshooting

---

## 1. Orient & connect — Meta (4 tools)

What it's for: make sure Merlin is talking to FL before anything else.

- `fl_ping` — is FL alive? Round-trip check
- `fl_reconnect` — re-attach the bridge if the connection dropped
- `fl_bridge_info` — bridge version, channel count, sample rate, state
- `fl_call_raw` — escape hatch: raw FL API call by name (power users)

Plus **7 read-only resources** (no tool call, Merlin reads them like context):
`fl://status`, `fl://project`, `fl://transport`, `fl://channels`, `fl://mixer`,
`fl://patterns`, `fl://playlist` — instant project snapshot before editing.

## 2. Set up the project — Project (11 tools)

What it's for: open/start a project and never lose work.

- `project_new` / `project_open` / `project_save` / `project_save_as` — lifecycle
- `project_metadata` — title, artist, tempo, key, comments
- `project_version` — which FL version the project is from
- `project_undo` / `project_redo` / `project_undo_history` — native undo
- `project_save_undo` — manual undo checkpoint before a risky edit
- `project_render` — render the song to WAV/MP3/OGG (the finish line)

## 3. Set the stage — Transport (14 tools)

What it's for: tempo, timing, and playback control — the producer's first knob.

- `transport_set_tempo` — BPM (with bounds checking)
- `transport_tap_tempo` — let FL tap the BPM for you
- `transport_set_time_signature` — 4/4, 7/8, whatever
- `transport_set_position` — seek (bars / seconds / ticks)
- `transport_jog` — nudge by 16ths
- `transport_song_length` — length in ticks, bars, steps
- `transport_status` — playing? recording? loop mode? tempo? (read before acting)
- `transport_play` / `transport_stop` / `transport_record` — the big three
- `transport_set_loop_mode` — pattern vs song loop
- `transport_set_playback_speed` — 0.25x–4x (practice mode)
- `transport_toggle_metronome` / `transport_toggle_countdown_before_recording`

## 4. Sound & channels — Channel Rack (20 tools)

What it's for: instruments live here. (Loading NEW plugins is a Layer-2 GUI tool —
existing instruments are fully controllable.)

- `channel_all` / `channel_count` / `channel_info` / `channel_selected` / `channel_select` — see and pick instruments
- `channel_set_volume` / `channel_set_pan` / `channel_set_pitch` — level, placement, tune
- `channel_mute` / `channel_solo` — focus a sound
- `channel_set_name` / `channel_set_color` — organize the rack
- `channel_route_to_mixer` — send instrument to a mixer track
- `channel_trigger_note` — fire a one-shot hit
- `channel_get_step_sequence` / `channel_set_step_sequence` — read/write the whole 16-step drum pattern
- `channel_get_grid_bit` / `channel_set_grid_bit` — single step on/off
- `channel_clear_step_sequence` — wipe the pattern
- `channel_quick_quantize` — snap steps to the grid

## 5. Write patterns & notes — Patterns (13) + Piano Roll (11)

What it's for: the musical content — patterns in the rack, notes in the piano roll.

Patterns:
- `pattern_list` / `pattern_count` / `pattern_current` / `pattern_select` — navigate
- `pattern_create` / `pattern_rename` / `pattern_clone` / `pattern_delete` — manage
- `pattern_set_color` / `pattern_set_length` — organize
- `pattern_find_by_name` — "find the chorus"
- `pattern_jump_to_next` / `pattern_jump_to_previous` — move between

Piano roll:
- `piano_roll_add_notes` — drop MIDI notes (pitch, time, duration, velocity)
- `piano_roll_add_chord` / `piano_roll_add_arpeggio` — instant harmony
- `piano_roll_read` — what's actually in the roll (verify after writes)
- `piano_roll_delete_notes` / `piano_roll_clear` — remove
- `piano_roll_quantize` / `piano_roll_humanize` / `piano_roll_transpose` — edit
- `piano_roll_duplicate` — copy a time range
- `piano_roll_status` — note count, range, selected channel

## 6. Generate ideas — Generators (12 tools)

What it's for: Merlin writing the first draft so you don't start from silence.

- `gen_scale_notes` / `gen_chord_notes` — music theory on demand
- `gen_emit_chord_progression` — progressions (i-iv-v, etc.)
- `gen_emit_melody` / `gen_emit_bassline` / `gen_emit_arpeggio` — melodic ideas
- `gen_emit_drum_pattern_notes` / `gen_emit_drum_pattern_step_seq` — drums as notes or step-sequencer data
- `gen_emit_dnb_groove` / `gen_list_dnb_styles` — drum & bass grooves
- `gen_list_scales` / `gen_list_chord_qualities` / `gen_list_progressions` / `gen_list_drum_patterns` — see the menus

## 7. Arrange the song — Playlist (14) + Arrangement (5)

What it's for: turning patterns into a song.

Playlist:
- `playlist_all_tracks` / `playlist_track_count` / `playlist_track_info` — see the timeline
- `playlist_list_clips` / `playlist_place_pattern` / `playlist_delete_clip` — place/remove pattern clips
- `playlist_mute_track` / `playlist_solo_track` — audition
- `playlist_set_track_name` / `playlist_set_track_color` — organize
- `playlist_list_markers` / `playlist_add_marker` / `playlist_delete_marker` — sections (intro, drop…)
- `playlist_refresh` — resync FL's playlist view

Arrangement:
- `arrangement_list` / `arrangement_select` / `arrangement_current` — multiple arrangements
- `arrangement_jump_marker` — hop to a section
- `arrangement_play_time` — timeline position of the playhead

## 8. Automate — Automation (5 tools)

What it's for: movement over time (volume swells, filter opens, tempo ramps).

- `automation_record_channel_volume` / `automation_record_channel_pan` — instrument moves
- `automation_record_mixer_volume` — mix moves
- `automation_record_plugin_param` — any plugin knob
- `automation_record_tempo` — BPM ramp (build/drop)

Pattern: call the record tool, move the knob via plugin/channel tools, done —
FL writes the automation clip.

## 9. Mix — Mixer (18 tools)

What it's for: levels, placement, routing, and FX.

- `mixer_count` / `mixer_all_tracks` / `mixer_track_info` — see the console
- `mixer_set_volume` / `mixer_set_pan` / `mixer_mute` / `mixer_solo` / `mixer_arm` — control per track
- `mixer_set_name` / `mixer_set_color` — organize
- `mixer_set_stereo_separation` — width
- `mixer_get_eq` / `mixer_set_eq_band` — the 3-band EQ
- `mixer_fx_slots` — what's loaded per track
- `mixer_set_send_level` — parallel sends (reverb/delay buses)
- `mixer_route` — routing & sidechain
- `mixer_link_to_channel` — instrument ↔ mixer track binding
- `mixer_select` — focus a track

## 10. Tweak plugins — Plugins (13 tools)

What it's for: every knob of loaded instruments/effects.

- `plugin_list_mixer_track` / `plugin_name` / `plugin_is_valid` — what's loaded
- `plugin_param_count` / `plugin_params` / `plugin_find_param` — see the knobs
- `plugin_get_param` / `plugin_set_param` — turn the knobs (with range checks)
- `plugin_preset_count` / `plugin_next_preset` / `plugin_prev_preset` / `plugin_set_preset` — sound browse
- `plugin_show_editor` — open the plugin window

## 11. Voice & audio content — Voice (6) + Audio (6)

What it's for: turning voice/samples into musical material (no recording needed —
feed it files or mic on Windows).

Voice → MIDI:
- `voice_list_devices` — find input devices
- `voice_record_and_transcribe` — record voice → notes
- `voice_transcribe_file` — existing recording → notes
- `voice_to_piano_roll` — notes straight into FL
- `voice_notes_to_piano_roll` — manual notes in
- `voice_open_gui` — visual editor window

Audio analysis:
- `audio_analyze` — tempo, key, onsets, loudness of a file
- `audio_melody_to_piano_roll` — hummed/sung line → piano roll
- `audio_slice` — chop at onsets
- `song_to_dnb_flip` — turn a song into a DnB bootleg
- `gen_emit_dnb_groove` / `gen_list_dnb_styles` — (also under generators)

## 12. Window control — UI (7 tools)

What it's for: FL's windows, for the moments the API needs eyes.

- `ui_show_window` / `ui_hide_window` — bring FL forward or hide it
- `ui_focused_window` — what has focus right now
- `ui_open_piano_roll_for_channel` — open the roll for a specific instrument
- `ui_scroll_to_channel` / `ui_selected_channel` — rack navigation
- `ui_hint` — show a message inside FL

## 13. Finish — Render & save

- `project_render` — WAV/MP3/OGG out
- `project_save` / `project_save_as` — save the project
- `transport_status` last check — did it all stick?

---

## The producer's day, compressed

```
orient (fl://project) -> stage (tempo/sig) -> sounds (channels) -> ideas (generators)
-> patterns & notes (patterns/piano_roll) -> arrange (playlist) -> automate (automation)
-> mix (mixer/plugins) -> content (voice/audio) -> render (project_render)
```

## Are they all present?

Yes — all 159 verified in `src/fl_studio_mcp/tools/` (15 files):

| Area | Count | Area | Count |
|---|---|---|---|
| Transport | 14 | Patterns | 13 |
| Channels | 20 | Mixer | 18 |
| Plugins | 13 | Piano roll | 11 |
| Playlist | 14 | Arrangement | 5 |
| Automation | 5 | Project | 11 |
| UI | 7 | Generators | 12 |
| Voice | 6 | Audio | 6 |
| Meta | 4 | **Total** | **159** |

The 88 tools still to build (and their layers) are tracked in
[`SPRINT.md`](SPRINT.md).