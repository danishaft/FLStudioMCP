"""Test fixture helpers built on the package .flp writer.

Delegates to fl_studio_mcp.offline.writer so the byte-level format knowledge
lives in exactly one place.
"""

from __future__ import annotations

import struct

from fl_studio_mcp.offline.writer import write_flp


def build_flp(path, **kwargs):
    return write_flp(path, **kwargs)


def build_demo_project(path):
    return write_flp(
        path,
        title="Demo Track",
        artists="Ejeh Daniel",
        genre="DnB",
        tempo_bpm=174.0,
        licensee="danishaft",
        channels=[
            {"iid": 0, "name": "Kick", "type": 0, "sample_path": "Kits/Kick.wav"},
            {"iid": 1, "name": "Bass", "type": 4, "internal_name": "Plucked!",
             "plugin_data": struct.pack("<IIIII", 32768, 65536, 1, 0, 1)},
        ],
        patterns=[
            {"iid": 1, "name": "Drums", "length": 16,
             "notes": [(0, 36, 0, 96), (0, 36, 96, 96), (0, 36, 192, 96)]},
            {"iid": 2, "name": "Melody", "length": 32,
             "notes": [(1, 64, 0, 192), (1, 67, 192, 192)]},
        ],
    )
