"""Tests for the audio-analysis key detection (Krumhansl-Schmuckler).

Only the pure key-estimation maths is tested here; full tempo/onset analysis
needs real audio + librosa and is covered by the live smoke test instead.
"""

from __future__ import annotations

import pytest

np = pytest.importorskip("numpy")

from fl_studio_mcp.audio_analysis import (  # noqa: E402
    _KEY_PROFILE_MAJOR,
    _KEY_PROFILE_MINOR,
    _estimate_key,
)


def test_detect_c_major():
    name, scale, conf = _estimate_key(np.array(_KEY_PROFILE_MAJOR))
    assert (name, scale) == ("C", "major")
    assert conf > 0.9


def test_detect_d_major():
    name, scale, _ = _estimate_key(np.roll(np.array(_KEY_PROFILE_MAJOR), 2))
    assert (name, scale) == ("D", "major")


def test_detect_a_minor():
    name, scale, _ = _estimate_key(np.roll(np.array(_KEY_PROFILE_MINOR), 9))
    assert (name, scale) == ("A", "minor")


def test_detect_f_sharp_minor():
    name, scale, _ = _estimate_key(np.roll(np.array(_KEY_PROFILE_MINOR), 6))
    assert (name, scale) == ("F#", "minor")


def test_estimate_key_accepts_plain_list():
    # _estimate_key should coerce a non-numpy sequence too.
    name, scale, _ = _estimate_key(list(_KEY_PROFILE_MAJOR))
    assert (name, scale) == ("C", "major")


def test_confidence_in_unit_range():
    _, _, conf = _estimate_key(np.ones(12))
    assert 0.0 <= conf <= 1.0
