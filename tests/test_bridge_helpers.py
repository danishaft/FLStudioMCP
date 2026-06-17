"""Tests for the FL-side bridge's pure helper functions.

`device_FLStudioMCP.py` normally runs inside FL Studio, but it now guards its
FL-only imports so it can be loaded offline. We import it by file path and test
the colour conversion (a real bug was fixed here: FL uses 0xRRGGBB, the bridge
previously used 0xBBGGRR and swapped red/blue) plus the small mappers.
"""

from __future__ import annotations

import importlib.util
import pathlib

import pytest


def _load_bridge():
    p = pathlib.Path(__file__).resolve().parents[1] / "fl_bridge" / "device_FLStudioMCP.py"
    spec = importlib.util.spec_from_file_location("flmcp_device_bridge", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


bridge = _load_bridge()


def test_color_uses_rrggbb_byte_order():
    # FL Studio: utils.RGBToColor(255,0,0) == 0xFF0000. Red must be the high byte.
    assert bridge._color_to_int("#FF0000") == 0xFF0000
    assert bridge._color_to_int("#00FF00") == 0x00FF00
    assert bridge._color_to_int("#0000FF") == 0x0000FF


def test_color_from_rgb_string():
    assert bridge._color_to_int("rgb(255, 0, 0)") == 0xFF0000
    assert bridge._color_to_int("rgb(0,128,255)") == 0x0080FF


def test_color_from_list():
    assert bridge._color_to_int([16, 32, 48]) == 0x102030


def test_color_int_passthrough():
    assert bridge._color_to_int(0x123456) == 0x123456


def test_color_bad_input_is_zero():
    assert bridge._color_to_int("not-a-color") == 0


@pytest.mark.parametrize("hexs", ["#000000", "#FFFFFF", "#102030", "#A1B2C3", "#FF0000"])
def test_color_roundtrip(hexs):
    assert bridge._int_to_color_hex(bridge._color_to_int(hexs)) == hexs


def test_int_to_hex_masks_high_bits():
    # FL sometimes returns colours with the alpha/high byte set; ignore it.
    assert bridge._int_to_color_hex(0xFF123456) == "#123456"


def test_position_unit_mapping():
    assert bridge._position_unit("ms") == 0
    assert bridge._position_unit("seconds") == 1
    assert bridge._position_unit("ticks") == 2
    assert bridge._position_unit("bars") == 3
    assert bridge._position_unit("steps") == 4
    assert bridge._position_unit("nonsense") == 3  # defaults to bars


def test_bool_int():
    assert bridge._bool_int(True) == 1
    assert bridge._bool_int(False) == 0
    assert bridge._bool_int(None) == 0
    assert bridge._bool_int(5) == 1


def test_handler_table_is_complete():
    for action in [
        "meta.ping", "transport.start", "transport.setTempo",
        "patterns.create", "channels.setColor", "channels.setStepSequence",
        "mixer.setEQBand", "mixer.arm", "playlist.muteTrack",
        "automation.recordTempo", "pianoroll.addNotes", "ui.focusedWindow",
    ]:
        assert action in bridge._HANDLERS, f"missing handler: {action}"


def test_safe_swallows_exceptions():
    def boom():
        raise RuntimeError("nope")
    assert bridge._safe(boom) is None
    assert bridge._safe(lambda x: x + 1, 41) == 42
