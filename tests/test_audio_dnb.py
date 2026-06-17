"""Tests for the Drum & Bass groove data + note expansion in tools/audio.py.

These are pure data / arithmetic checks — no audio deps required.
"""

from __future__ import annotations

import pytest

from fl_studio_mcp.tools.audio import DNB_STYLES, _dnb_drum_notes, _reese_bass


def test_dnb_grids_are_32_steps_of_bits():
    assert set(DNB_STYLES) == {"amen", "think", "modern", "halftime"}
    for style, grid in DNB_STYLES.items():
        for midi_num, hits in grid.items():
            assert len(hits) == 32, f"{style}/{midi_num} has {len(hits)} steps"
            assert all(h in (0, 1) for h in hits), f"{style}/{midi_num} has non-bit values"


def test_dnb_drum_notes_repeats_scale_linearly():
    one = _dnb_drum_notes("amen", repeats=1)
    two = _dnb_drum_notes("amen", repeats=2)
    assert one, "expected some notes"
    assert len(two) == 2 * len(one)


def test_dnb_drum_notes_time_in_quarters():
    # One loop is 2 bars = 8 quarter-notes; all times must fall inside that.
    notes = _dnb_drum_notes("modern", repeats=1)
    assert max(n["time"] for n in notes) < 8.0
    # Two loops -> up to 16 quarters.
    notes2 = _dnb_drum_notes("modern", repeats=2)
    assert max(n["time"] for n in notes2) < 16.0


def test_dnb_unknown_style_raises():
    with pytest.raises(ValueError):
        _dnb_drum_notes("definitely-not-a-style", 1)


def test_reese_bass_on_root():
    notes = _reese_bass(24, length_bars=2.0, step_bars=0.25)
    assert notes
    assert all(n["midi"] == 24 for n in notes)
    # 2 bars / 0.25-bar steps = 8 notes.
    assert len(notes) == 8
