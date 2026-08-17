# Merlin Examples — Real JSON In, Real JSON Out

Every example below uses the ACTUAL shapes from the code (`device_FLStudioMCP.py`
handlers, `tools/*.py`, `protocol.py`). Nothing invented.

## 0. The wire

One TCP frame = `[4-byte length][UTF-8 JSON]` to `127.0.0.1:9876`:

```
REQUEST   {"id":7,"action":"transport.status","params":{}}
RESPONSE  {"id":7,"ok":true,"result":{...},"error":null}
ERROR     {"id":7,"ok":false,"result":null,"error":"bridge unavailable"}
```

The tool layer in Python (this is ALL the tool does — 1 line):

```python
@mcp.tool()
def transport_status() -> dict:
    """Get is_playing, is_recording, position, loop mode, tempo, signature."""
    return get_client().call("transport.status")   # <- TCP round trip
```

`transport.status` -> `transport.start` (snake -> dot) -> `_HANDLERS` dict in FL -> FL API.

---

## 1. Meta — check the bridge

```
fl_ping
> {"ok": true, "result": "pong", "error": null}

fl_bridge_info
> {"ok": true, "result": {"version": "fLMCP 1.0.0", "channels": 12,
                          "sample_rate": 48000, "state": "ready"}, "error": null}
```

## 2. Transport — the producer's first knobs

```
transport_set_tempo   bpm=128
> {"ok": true, "result": {"bpm": 128.0}, "error": null}

transport_status
> {"ok": true, "result": {"is_playing": true, "is_recording": false,
   "position_ticks": 960, "position_bars": 1.0, "position_seconds": 2.5,
   "loop_mode": "pattern", "bpm": 128.0}, "error": null}
```

## 3. Channels — see the rack, twist an instrument

```
channel_all
> {"ok": true, "result": {"channels": [
    {"index": 0, "name": "Kick",   "color": "#C0C0C0", "volume": 0.85, "volume_db": -2.1,
     "pan": 0.0, "pitch_semitones": 0.0, "pitch_cents": 0, "is_muted": false,
     "is_solo": false, "is_selected": false, "fx_track": 1, "type": "sampler"},
    {"index": 1, "name": "Bass",   ... },
    ...]}, "error": null}

channel_set_volume   index=0, volume=0.7        # 0..1 normalized
> {"ok": true, "result": {"volume": 0.7, "volume_db": -3.1}, "error": null}

channel_trigger_note  index=1                   # fire one note
> {"ok": true, "result": {"triggered": true}, "error": null}
```

## 4. Patterns — 13 tools, 13 handlers

```
pattern_create   name="Chorus"
> {"ok": true, "result": {"index": 4}, "error": null}

pattern_find_by_name  name="Chorus"
> {"ok": true, "result": {"index": 4}, "error": null}
```

## 5. Piano roll — notes go through the FILE bridge (staged, not immediate)

This is the one different flow — notes land in `fLMCP_request.json`, the
FL-internal script (`ComposeWithLLM.pyscript`) applies them on `Ctrl+Alt+Y`:

```
piano_roll_add_notes   channel=2, clear_first=true, notes=[
    {"midi": 48, "time": 0.0,  "duration": 0.5, "velocity": 0.8},
    {"midi": 55, "time": 0.5,  "duration": 0.5, "velocity": 0.7},
    {"midi": 60, "time": 1.0,  "duration": 1.0, "velocity": 0.9}]

> {"ok": true, "result": {"staged": true, "needs_keystroke": true,
   "request_file": "C:/Users/.../fLMCP_request.json"}, "error": null}
```

piano_roll_read is the verify step:

```
piano_roll_read
> {"ok": true, "result": {"channel": 2, "notes": [
    {"midi": 48, "time": 0.0, "duration": 0.5, "velocity": 0.8},
    {"midi": 55, "time": 0.5, "duration": 0.5, "velocity": 0.7},
    {"midi": 60, "time": 1.0, "duration": 1.0, "velocity": 0.9}]}, "error": null}
```

## 6. Generators — computed LOCALLY in Python, then staged to piano roll

```
gen_emit_chord_progression   channel=2, progression="I-V-vi-IV",
                             root="C4", scale="major", clear_first=true

# the theory happens on your machine (Python), then:
> {"ok": true, "result": {"staged": true, "needs_keystroke": true,
   "request_file": "...fLMCP_request.json", "notes": 16}, "error": null}
```

## 7. Playlist + arrangement — the honest ones

```
playlist_all_tracks
> {"ok": true, "result": {"tracks": [
    {"index": 0, "name": "Drums", "color": "#D0D0D0", "is_muted": false, "is_solo": false},
    ...]}, "error": null}

playlist_place_pattern        # FL API limitation — tool says so:
> {"ok": false, "result": null,
   "error": "playlist.placePattern is not yet supported by FL's Python API;
             use ui.showWindow('playlist') + manual placement or arrangement jumps."}

arrangement_jump_marker   name="Chorus"
> {"ok": true, "result": {"jumped_to": "Chorus"}, "error": null}
```

## 8. Automation — record, then let FL write the clip

```
automation_record_channel_volume   channel=1
> {"ok": true, "result": {"recording": true, "target": "channel.volume"},
   "error": null}
# ...move the fader with channel_set_volume calls... then stop by calling again
```

## 9. Mixer

```
mixer_track_info   track=3
> {"ok": true, "result": {"index": 3, "name": "Lead", "volume": 0.8, "volume_db": -1.9,
   "pan": 0.1, "stereo_separation": 1.0, "is_muted": false, "is_solo": false,
   "is_armed": false, "color": "#4080FF"}, "error": null}

mixer_fx_slots   track=3
> {"ok": true, "result": {"slots": ["", "Fruity Reeverb 2", ""]}, "error": null}
```

## 10. Plugins — knobs by param index, with human-readable value

```
plugin_list_mixer_track   track=3
> {"ok": true, "result": {"plugins": [
    {"name": "Fruity Reeverb 2", "slot": 1, "param_count": 12}]}, "error": null}

plugin_get_param   track=3, slot=1, param=7        # 7 = "Wet"
> {"ok": true, "result": {"value": 0.25, "value_string": "25%"}, "error": null}

plugin_set_param   track=3, slot=1, param=7, value=0.5
> {"ok": true, "result": {"value": 0.5, "value_string": "50%"}, "error": null}
```

## 11. Voice & audio — run LOCALLY, no bridge

```
voice_transcribe_file   path="C:/Users/you/hum.wav"
> {"ok": true, "result": {"notes": [
    {"midi": 62, "time": 0.0, "duration": 0.4, "velocity": 0.7},
    {"midi": 65, "time": 0.5, "duration": 0.3, "velocity": 0.6}],
   "bpm": 120.0}, "error": null}

audio_analyze   path="track.mp3"
> {"ok": true, "result": {"tempo_bpm": 174.0, "key_root": "A", "key_mode": "minor",
   "onsets_s": [0.0, 0.34, 0.69, ...], "loudness_db": -8.2, "duration_s": 214.0},
   "error": null}
```

## 12. Project — the "needs a human" edge

```
project_metadata
> {"ok": true, "result": {"version": 21, "tempo": 128.0, "ppq": 96,
   "channel_count": 12, "mixer_tracks": 65, "pattern_count": 8,
   "selected_pattern": 2, "selected_channel": 0, "is_playing": false,
   "is_recording": false, "loop_mode": "pattern", "metronome": false,
   "has_unsaved_changes": true}, "error": null}

project_new        # needs a human hand:
> {"ok": false, "result": null,
   "error": "project.new requires UI interaction (File > New); not exposed by the Python API."}

project_render   path="C:/out.wav", format="wav", quality=3
> {"ok": true, "result": {"path": "C:/out.wav", "success": true}, "error": null}
```

## 13. UI

```
ui_hint   message="Merge is calling. Listen."
> {"ok": true, "result": {"shown": true}, "error": null}

ui_show_window   name="mixer"
> {"ok": true, "result": {"window": "mixer", "shown": true}, "error": null}
```

---

## The mental model (3 rules)

1. **Bridge tools** (meta/transport/channels/patterns/mixer/plugins/playlist/arrangement/
   automation/project/ui) — one TCP round trip to FL, `{"id","action","params"}` in,
   `{"id","ok","result","error"}` out.
2. **File-bridge tools** (piano_roll, generators) — notes written to a JSON file,
   FL's internal script applies them on `Ctrl+Alt+Y`; response says `staged: true,
   needs_keystroke: true`.
3. **Local tools** (voice, audio) — pure Python on your machine, FL never involved;
   output is notes/analysis you then feed to the bridge tools.
4. **`ok: false` is informative, not a crash** — some FL API gaps (project.new,
   playlist.placePattern) return a plain-English reason.