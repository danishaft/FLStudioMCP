"""Offline .flp layer tests: flp-info and the shared parse machinery."""

from __future__ import annotations

import struct

import pytest

from fl_studio_mcp.offline.core import load_project, safe_get
from fl_studio_mcp.offline.flp import (flp_analyze, flp_channels, flp_diff, flp_info, flp_merge, flp_notes, flp_patterns, flp_plugins, flp_rename, flp_samples, flp_tempo, flp_template)

from _flp_factory import build_demo_project, build_flp


def test_flp_info_full_metadata(tmp_path):
    p = tmp_path / "full.flp"
    build_flp(
        p,
        title="Merlin's Groove",
        artists="Ejeh Daniel",
        genre="DnB",
        url="https://example.com",
        comments="draft one",
        licensee="danishaft",
        tempo_bpm=174.0,
    )
    info = flp_info(str(p))
    assert info["title"] == "Merlin's Groove"
    assert info["artists"] == "Ejeh Daniel"
    assert info["genre"] == "DnB"
    assert info["url"] == "https://example.com"
    assert info["comments"] == "draft one"
    assert info["licensee"] == "danishaft"
    assert info["tempo_bpm"] == 174.0
    assert info["ppq"] == 96
    assert info["fl_version"] == "21.0.0"
    assert info["format"] == "Project"
    assert info["created_on"] is not None
    assert info["time_spent_seconds"] == 21600.0
    assert info["looped"] is False
    assert info["show_info"] is True
    assert info["licensed"] is True


def test_flp_info_minimal_file(tmp_path):
    p = tmp_path / "minimal.flp"
    build_flp(p, title=None)
    info = flp_info(str(p))
    assert info["title"] is None
    assert info["artists"] is None
    assert info["genre"] is None
    assert info["comments"] is None
    assert info["tempo_bpm"] == 128.5
    assert info["ppq"] == 96


def test_flp_info_missing_file(tmp_path):
    with pytest.raises(ValueError, match="file not found"):
        flp_info(str(tmp_path / "nope.flp"))


def test_flp_info_corrupt_file(tmp_path):
    p = tmp_path / "corrupt.flp"
    p.write_bytes(b"not a flp file at all")
    with pytest.raises(ValueError, match="corrupt .flp header|failed to parse"):
        flp_info(str(p))


def test_load_project_round_trip(tmp_path):
    p = tmp_path / "rt.flp"
    build_flp(p, tempo_bpm=140.0, title="Round Trip")
    project = load_project(p)
    assert project.title == "Round Trip"
    assert project.tempo == 140.0
    assert project.ppq == 96
    assert project.version.major == 21


def test_safe_get_missing_attr():
    class Dummy:
        a = 1

    assert safe_get(Dummy(), "nonexistent") is None
    assert safe_get(Dummy(), "a") == 1

def test_flp_channels(tmp_path):
    p = tmp_path / "channels.flp"
    build_demo_project(p)
    out = flp_channels(str(p))
    assert out["count"] == 2
    kick, bass = out["channels"]
    assert kick["iid"] == 0
    assert kick["name"] == "Kick"
    assert kick["type"] == "Sampler"
    assert kick["sample_path"] == "Kits/Kick.wav"
    assert bass["iid"] == 1
    assert bass["name"] == "Bass"
    assert bass["type"] == "Instrument"
    assert bass["internal_name"] == "Plucked!"


def test_flp_channels_empty(tmp_path):
    p = tmp_path / "empty.flp"
    build_flp(p)
    out = flp_channels(str(p))
    assert out["count"] == 0
    assert out["channels"] == []


def test_flp_patterns(tmp_path):
    p = tmp_path / "patterns.flp"
    build_demo_project(p)
    out = flp_patterns(str(p))
    assert out["count"] == 2
    drums, melody = out["patterns"]
    assert drums["iid"] == 1
    assert drums["name"] == "Drums"
    assert drums["length"] == 16
    assert drums["note_count"] == 3
    assert melody["note_count"] == 2


def test_flp_notes(tmp_path):
    p = tmp_path / "notes.flp"
    build_demo_project(p)
    out = flp_notes(str(p))
    drums = out["patterns"][0]
    assert drums["name"] == "Drums"
    first = drums["notes"][0]
    assert first["key"] == "C3"
    assert first["midi"] == 36
    assert first["position"] == 0
    assert first["length"] == 96
    assert first["velocity"] == 100
    assert first["rack_channel"] == 0


def test_flp_notes_filtered(tmp_path):
    p = tmp_path / "notes.flp"
    build_demo_project(p)
    out = flp_notes(str(p), pattern_iid=2)
    assert out["pattern"] == 2
    assert out["count"] == 1
    assert out["patterns"][0]["name"] == "Melody"
    assert [n["key"] for n in out["patterns"][0]["notes"]] == ["E5", "G5"]


def test_flp_plugins(tmp_path):
    p = tmp_path / "plugins.flp"
    build_demo_project(p)
    out = flp_plugins(str(p))
    assert out["count"] == 2
    by_iid = {pl["channel_iid"]: pl for pl in out["plugins"]}
    assert by_iid[0]["internal_name"] is None
    assert by_iid[0]["plugin_type"] is None
    bass = by_iid[1]
    assert bass["internal_name"] == "Plucked!"
    assert bass["plugin_type"] == "Plucked"
    assert bass["params"]["decay"] == 32768
    assert bass["params"]["normalize"] is True


def test_flp_samples(tmp_path):
    p = tmp_path / "samples.flp"
    build_demo_project(p)
    out = flp_samples(str(p))
    assert out["count"] == 1
    assert out["samples"][0]["channel_name"] == "Kick"
    assert out["samples"][0]["sample_path"] == "Kits/Kick.wav"


def test_flp_tempo_get(tmp_path):
    p = tmp_path / "t.flp"
    build_demo_project(p)
    out = flp_tempo(str(p))
    assert out["tempo_bpm"] == 174.0
    assert out["ppq"] == 96


def test_flp_tempo_set(tmp_path):
    p = tmp_path / "t.flp"
    build_demo_project(p)
    flp_tempo(str(p), bpm=140.25)
    assert flp_tempo(str(p))["tempo_bpm"] == 140.25


def test_flp_tempo_set_out_of_range(tmp_path):
    p = tmp_path / "t.flp"
    build_demo_project(p)
    with pytest.raises(ValueError, match="out of range"):
        flp_tempo(str(p), bpm=2000)


def test_flp_rename(tmp_path):
    p = tmp_path / "r.flp"
    build_demo_project(p)
    out = flp_rename(str(p), [
        {"channel_iid": 0, "name": "Kicker"},
        {"pattern_iid": 1, "name": "Beat"},
    ])
    assert [x["name"] for x in out["renamed"]] == ["Kicker", "Beat"]
    from fl_studio_mcp.offline.flp import flp_channels, flp_patterns
    assert flp_channels(str(p))["channels"][0]["name"] == "Kicker"
    assert flp_patterns(str(p))["patterns"][0]["name"] == "Beat"


def test_flp_rename_unknown_channel(tmp_path):
    p = tmp_path / "r.flp"
    build_demo_project(p)
    with pytest.raises(ValueError, match="no channel"):
        flp_rename(str(p), [{"channel_iid": 99, "name": "x"}])


def test_flp_rename_bad_entry(tmp_path):
    p = tmp_path / "r.flp"
    build_demo_project(p)
    with pytest.raises(ValueError, match="channel_iid or pattern_iid"):
        flp_rename(str(p), [{"name": "x"}])


def test_flp_diff_same(tmp_path):
    p1 = tmp_path / "a.flp"
    p2 = tmp_path / "b.flp"
    build_demo_project(p1)
    build_demo_project(p2)
    out = flp_diff(str(p1), str(p2))
    assert "tempo" not in out
    assert "channels_changed" not in out
    assert "patterns_changed" not in out


def test_flp_diff_changes(tmp_path):
    a = tmp_path / "a.flp"
    b = tmp_path / "b.flp"
    build_demo_project(a)
    build_demo_project(b)
    flp_tempo(str(b), bpm=120.0)
    flp_rename(str(b), [{"channel_iid": 0, "name": "Kicker"}])
    out = flp_diff(str(a), str(b))
    assert out["tempo"] == {"base": 174.0, "other": 120.0}
    assert out["channels_changed"][0]["iid"] == 0
    assert out["channels_changed"][0]["name"]["other"] == "Kicker"


def test_flp_diff_added(tmp_path):
    a = tmp_path / "a.flp"
    b = tmp_path / "b.flp"
    build_demo_project(a)
    build_flp(b, title="Other")
    out = flp_diff(str(a), str(b))
    assert out["patterns_removed"]
    assert "channels_removed" in out


def test_flp_template(tmp_path):
    src = tmp_path / "src.flp"
    out_p = tmp_path / "tmpl.flp"
    build_demo_project(src)
    res = flp_template(str(src), str(out_p))
    assert res["template"] is True
    from fl_studio_mcp.offline.flp import flp_patterns
    assert flp_patterns(str(out_p))["count"] == 0
    from fl_studio_mcp.offline.flp import flp_channels
    assert flp_channels(str(out_p))["count"] == 2
    assert flp_tempo(str(out_p))["tempo_bpm"] == 174.0


def test_flp_merge(tmp_path):
    base = tmp_path / "base.flp"
    other = tmp_path / "other.flp"
    merged = tmp_path / "merged.flp"
    build_demo_project(base)
    build_flp(
        other,
        title="Second",
        channels=[
            {"iid": 0, "name": "Snare", "type": 0, "sample_path": "Kits/Snare.wav"},
            {"iid": 1, "name": "Pad", "type": 4, "internal_name": "Plucked!",
             "plugin_data": struct.pack("<IIIII", 1000, 2000, 0, 0, 0)},
        ],
        patterns=[
            {"iid": 1, "name": "Fill", "length": 8,
             "notes": [(0, 38, 0, 96)]},
        ],
    )
    res = flp_merge(str(base), str(other), str(merged))
    assert res["channels"] == 4
    assert res["patterns"] == 3
    from fl_studio_mcp.offline.flp import flp_channels, flp_notes, flp_patterns
    ch = flp_channels(str(merged))["channels"]
    assert [c["name"] for c in ch] == ["Kick", "Bass", "Snare", "Pad"]
    pat = flp_patterns(str(merged))["patterns"]
    assert [p["name"] for p in pat] == ["Drums", "Melody", "Fill"]
    fill = flp_notes(str(merged), pattern_iid=3)["patterns"][0]
    assert fill["notes"][0]["rack_channel"] == 2
    assert fill["notes"][0]["key"] == "D3"
    assert flp_tempo(str(merged))["tempo_bpm"] == 174.0


def test_flp_generate(tmp_path):
    from fl_studio_mcp.offline.flp import flp_generate
    p = tmp_path / "gen.flp"
    flp_generate(str(p), {
        "title": "Generated",
        "tempo_bpm": 140.0,
        "channels": [
            {"name": "Kick", "type": "sampler", "sample_path": "Kits/Kick.wav"},
            {"name": "Bass", "type": "instrument", "internal_name": "Plucked!"},
        ],
        "patterns": [
            {"name": "Main", "length": 32,
             "notes": [{"rack_channel": 0, "key": 36, "position": 0, "length": 96,
                        "velocity": 127}]},
        ],
    })
    out = flp_analyze(str(p))
    assert out["tempo_bpm"] == 140.0
    assert out["channels"] == 2
    assert out["channel_types"] == {"Sampler": 1, "Instrument": 1}
    assert out["patterns"] == 1
    assert out["total_notes"] == 1
    assert out["midi_range"] == {"lowest": 36, "highest": 36}


def test_flp_generate_bad_type(tmp_path):
    from fl_studio_mcp.offline.flp import flp_generate
    with pytest.raises(ValueError, match="unknown channel type"):
        flp_generate(str(tmp_path / "x.flp"), {"channels": [{"name": "A", "type": "guitar"}]})


def test_flp_generate_bad_velocity(tmp_path):
    from fl_studio_mcp.offline.flp import flp_generate
    with pytest.raises(ValueError, match="velocity out of range"):
        flp_generate(str(tmp_path / "x.flp"), {
            "patterns": [{"notes": [{"rack_channel": 0, "key": 36, "position": 0,
                                     "length": 1, "velocity": 300}]}],
        })


def test_flp_validate_ok(tmp_path):
    from fl_studio_mcp.offline.flp import flp_validate
    p = tmp_path / "v.flp"
    build_demo_project(p)
    out = flp_validate(str(p))
    assert out["ok"] is True
    assert out["warnings"] == []


def test_flp_validate_missing_channel_ref(tmp_path):
    from fl_studio_mcp.offline.flp import flp_validate
    p = tmp_path / "v.flp"
    build_flp(p, patterns=[{"iid": 1, "name": "X", "notes": [(9, 36, 0, 96)]}])
    out = flp_validate(str(p))
    assert out["ok"] is False
    assert any("missing channel 9" in w for w in out["warnings"])


def test_flp_validate_corrupt(tmp_path):
    from fl_studio_mcp.offline.flp import flp_validate
    p = tmp_path / "bad.flp"
    p.write_bytes(b"FLhd\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00garbage")
    out = flp_validate(str(p))
    assert out["ok"] is False
    assert out["errors"]


def test_flp_analyze(tmp_path):
    from fl_studio_mcp.offline.flp import flp_analyze
    p = tmp_path / "a.flp"
    build_demo_project(p)
    out = flp_analyze(str(p))
    assert out["tempo_bpm"] == 174.0
    assert out["fl_version"] == "21.0.0"
    assert out["channels"] == 2
    assert out["channel_types"] == {"Sampler": 1, "Instrument": 1}
    assert out["total_notes"] == 5
    assert out["midi_range"] == {"lowest": 36, "highest": 67}
    assert out["pattern_stats"][0]["notes"] == 3


def test_flp_batch_info(tmp_path):
    from fl_studio_mcp.offline.flp import flp_batch
    build_demo_project(tmp_path / "one.flp")
    build_demo_project(tmp_path / "two.flp")
    out = flp_batch(str(tmp_path), "info")
    assert out["files"] == 2
    assert all(r["title"] == "Demo Track" for r in out["results"])
    assert out["failures"] == []


def test_flp_batch_tempo(tmp_path):
    from fl_studio_mcp.offline.flp import flp_batch, flp_tempo
    build_demo_project(tmp_path / "one.flp")
    build_demo_project(tmp_path / "two.flp")
    flp_batch(str(tmp_path), "tempo", bpm=100.0)
    assert flp_tempo(str(tmp_path / "one.flp"))["tempo_bpm"] == 100.0
    assert flp_tempo(str(tmp_path / "two.flp"))["tempo_bpm"] == 100.0


def test_flp_batch_template(tmp_path):
    from fl_studio_mcp.offline.flp import flp_batch, flp_patterns
    build_demo_project(tmp_path / "one.flp")
    flp_batch(str(tmp_path), "template")
    assert flp_patterns(str(tmp_path / "one_template.flp"))["count"] == 0


def test_flp_batch_tempo_requires_bpm(tmp_path):
    from fl_studio_mcp.offline.flp import flp_batch
    with pytest.raises(ValueError, match="requires bpm"):
        flp_batch(str(tmp_path), "tempo")


def test_flp_batch_not_a_directory(tmp_path):
    from fl_studio_mcp.offline.flp import flp_batch
    with pytest.raises(ValueError, match="not a directory"):
        flp_batch(str(tmp_path / "nope"), "info")
