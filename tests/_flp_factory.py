"""Build minimal, valid .flp files byte-by-byte for tests.

FLP layout (verified against pyflp 2.2.1 and the real format docs):

    header:  b"FLhd" + u32 version(6) + i16 format(0) + u16 channel_count + u16 ppq
    data:    b"FLdt" + u32 payload_size + events...

Event framing by event id range:
    id < 64   -> 1 byte payload
    64 <= id < 128 -> 2 bytes
    128 <= id < 192 -> 4 bytes
    id >= 192 (TEXT) -> VarInt size byte + payload

TEXT events are UTF-16-LE when FL version >= 11.5 (pyflp decides from the
FLVersion event, so it must come first in the payload).
"""

from __future__ import annotations

import struct
from pathlib import Path


def _obfuscate_licensee(name: str) -> str:
    """Mirror FL Studio's Licensee obfuscation (reverse of pyflp's decoder:
    for each char index i, FL stores a value such that either
    stored-26+i or stored+49+i is alphanumeric; pyflp picks the alnum one)."""
    out = []
    for idx, ch in enumerate(name):
        target = ord(ch)
        c1 = target + 26 - idx
        if chr(c1).isalnum():
            out.append(chr(c1))
            continue
        c2 = target - 49 - idx
        out.append(chr(c2))
    return "".join(out)


def _text_event(event_id: int, text: str) -> bytes:
    payload = text.encode("utf-16-le")
    return bytes([event_id, len(payload)]) + payload


def _u32_event(event_id: int, value: int) -> bytes:
    return bytes([event_id]) + struct.pack("<I", value)


def _u16_event(event_id: int, value: int) -> bytes:
    return bytes([event_id]) + struct.pack("<H", value)


def _u8_event(event_id: int, value: int) -> bytes:
    return bytes([event_id, value])


def build_flp(
    path: str | Path,
    *,
    fl_version: str = "21.0.0",
    tempo_bpm: float = 128.5,
    ppq: int = 96,
    title: str | None = "Test Track",
    artists: str | None = None,
    genre: str | None = None,
    url: str | None = None,
    comments: str | None = None,
    licensee: str | None = None,
    created_on_days: float | None = 46258.5,
    time_spent_days: float | None = 0.25,
    looped: int | None = 0,
    show_info: int | None = 1,
    licensed: int | None = 1,
) -> None:
    """Write a minimal .flp file. Only events for non-None fields are written."""
    body = bytearray()
    body += bytes([199, len(fl_version)]) + fl_version.encode("ascii")
    body += _u32_event(156, round(tempo_bpm * 1000))
    if title is not None:
        body += _text_event(194, title)
    if artists is not None:
        body += _text_event(207, artists)
    if genre is not None:
        body += _text_event(206, genre)
    if url is not None:
        body += _text_event(197, url)
    if comments is not None:
        body += _text_event(195, comments)
    if licensee is not None:
        body += _text_event(200, _obfuscate_licensee(licensee))
    if looped is not None:
        body += _u8_event(9, looped)
    if show_info is not None:
        body += _u8_event(10, show_info)
    if licensed is not None:
        body += _u8_event(28, licensed)
    if created_on_days is not None or time_spent_days is not None:
        ts = struct.pack(
            "<dd", created_on_days or 0.0, time_spent_days or 0.0
        )
        body += bytes([237, len(ts)]) + ts

    header = struct.pack("4sIh2H", b"FLhd", 6, 0, 0, ppq)
    payload = bytes(body)
    data = b"FLdt" + struct.pack("<I", len(payload)) + payload
    Path(path).write_bytes(header + data)