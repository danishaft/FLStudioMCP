"""Offline .flp layer tests: flp-info and the shared parse machinery."""

from __future__ import annotations

import pytest

from fl_studio_mcp.offline.core import load_project, safe_get
from fl_studio_mcp.offline.flp import flp_info

from _flp_factory import build_flp


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