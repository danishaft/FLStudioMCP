"""Byte-level .flp writer used by flp-generate and test fixtures.

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

Channel grouping (ChannelRack.__iter__): events are divided into groups by
ChannelID.New (64); every ChannelID/PluginID event after it belongs to that
channel. ChannelID.GroupNum (145) must index an existing DisplayGroup event
(DisplayGroupID.Name, 231) or pyflp raises IndexError.

Patterns (Patterns.__iter__): events divided by PatternID.New (65); notes are
one NotesEvent (224) containing a list of 24-byte note structs.
"""

from __future__ import annotations

import base64
import struct
from pathlib import Path


def _text_event(event_id: int, text: str) -> bytes:
    payload = text.encode("utf-16-le")
    return bytes([event_id, len(payload)]) + payload


def _u32_event(event_id: int, value: int) -> bytes:
    return bytes([event_id]) + struct.pack("<I", value)


def _u16_event(event_id: int, value: int) -> bytes:
    return bytes([event_id]) + struct.pack("<H", value)


def _u8_event(event_id: int, value: int) -> bytes:
    return bytes([event_id, value])


def obfuscate_licensee(name: str) -> str:
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


_NOTE_STRUCT = struct.Struct("<IHHIHHBBBBBBBB")


def notes_event(notes: list[tuple[int, int, int, int]]) -> bytes:
    """Encode notes as one PatternID.Notes (224) event.

    Each note: (rack_channel, key, position_ticks, length_ticks).
    Struct layout (24 bytes): position u32, flags u16, rack_channel u16,
    length u32, key u16, group u16, fine_pitch u8, _u1 u8, release u8,
    midi_channel u8, pan u8, velocity u8, mod_x u8, mod_y u8.
    """
    payload = bytearray()
    for rack_channel, key, position, length in notes:
        payload += _NOTE_STRUCT.pack(
            position, 0, rack_channel, length, key, 0,
            120, 0, 0, 0, 64, 100, 128, 128,
        )
    return bytes([224, len(payload)]) + bytes(payload)


def write_flp(
    path: str | Path,
    *,
    fl_version: str = "21.0.0",
    tempo_bpm: float = 128.5,
    ppq: int = 96,
    title: str | None = None,
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
    channels: list[dict] | None = None,
    patterns: list[dict] | None = None,
) -> None:
    """Write a minimal .flp file.

    channels: list of dicts:
        {"iid": int, "name": str, "type": int, "sample_path": str|None,
         "internal_name": str|None, "plugin_data": bytes|None}
        plugin_data is the raw PluginID.Data payload (opaque to FL); for
        "Plucked!" it is 20 bytes: decay u32, color u32, normalize u32bool,
        gate u32bool, widen u32bool.
    patterns: list of dicts:
        {"iid": int, "name": str|None, "length": int,
         "notes": [(rack_channel, key, position, length), ...]}
    """
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
        body += _text_event(200, obfuscate_licensee(licensee))
    if looped is not None:
        body += _u8_event(9, looped)
    if show_info is not None:
        body += _u8_event(10, show_info)
    if licensed is not None:
        body += _u8_event(28, licensed)
    if created_on_days is not None or time_spent_days is not None:
        ts = struct.pack("<dd", created_on_days or 0.0, time_spent_days or 0.0)
        body += bytes([237, len(ts)]) + ts

    for ch in channels or []:
        body += _u32_event(64, ch["iid"])          # ChannelID.New
        body += _u8_event(21, ch.get("type", 4))   # ChannelID.Type
        body += _u32_event(145, 0)                 # ChannelID.GroupNum
        body += _text_event(203, ch["name"])       # PluginID.Name
        if ch.get("internal_name"):
            body += _text_event(201, ch["internal_name"])
        if ch.get("plugin_data"):
            body += bytes([213, len(ch["plugin_data"])]) + ch["plugin_data"]
        if ch.get("sample_path"):
            body += _text_event(196, ch["sample_path"])

    if channels:
        body += _text_event(231, "Default")        # DisplayGroupID.Name

    for pat in patterns or []:
        body += _u32_event(65, pat["iid"])         # PatternID.New
        if pat.get("name"):
            body += _text_event(193, pat["name"])  # PatternID.Name
        body += _u32_event(164, pat.get("length", 16))  # PatternID.Length
        if pat.get("notes"):
            body += notes_event(pat["notes"])

    header = struct.pack("4sIh2H", b"FLhd", 6, 0, 0, ppq)
    payload = bytes(body)
    data = b"FLdt" + struct.pack("<I", len(payload)) + payload
    Path(path).write_bytes(header + data)


def write_flp_from_spec(path: str | Path, spec: dict) -> None:
    """Build a project from a user-facing JSON spec (flp-generate).

    spec keys:
        title, artists, genre, url, comments (str|None)
        tempo_bpm (float), ppq (int), fl_version (str)
        channels: [{name (str), type (str|int), sample_path (str|None),
                    internal_name (str|None), plugin_data (base64 str|None)}]
        patterns: [{name (str|None), length (int),
                    notes: [{rack_channel (int), key (int, MIDI),
                             position (int), length (int),
                             velocity (int, 0-255)}]}]
    Channel and pattern ids are assigned automatically in list order.
    """
    channel_types = {
        "sampler": 0, "native": 2, "layer": 3, "instrument": 4, "automation": 5,
    }
    channels = []
    for i, ch in enumerate(spec.get("channels", [])):
        typ = ch.get("type", "instrument")
        if isinstance(typ, str):
            try:
                typ = channel_types[typ.lower()]
            except KeyError:
                raise ValueError(f"unknown channel type {typ!r} "
                                 f"(use one of {sorted(channel_types)})")
        plugin_data = ch.get("plugin_data")
        channels.append({
            "iid": i,
            "name": ch["name"],
            "type": typ,
            "sample_path": ch.get("sample_path"),
            "internal_name": ch.get("internal_name"),
            "plugin_data": base64.b64decode(plugin_data) if plugin_data else None,
        })
    patterns = []
    for i, pat in enumerate(spec.get("patterns", [])):
        notes = []
        for n in pat.get("notes", []):
            velocity = n.get("velocity", 100)
            if not 0 <= velocity <= 255:
                raise ValueError(f"velocity out of range (0-255): {velocity}")
            notes.append((n["rack_channel"], n["key"], n["position"], n["length"]))
        patterns.append({
            "iid": i + 1,
            "name": pat.get("name"),
            "length": pat.get("length", 16),
            "notes": notes,
        })
    write_flp(
        path,
        fl_version=spec.get("fl_version", "21.0.0"),
        tempo_bpm=spec.get("tempo_bpm", 128.5),
        ppq=spec.get("ppq", 96),
        title=spec.get("title"),
        artists=spec.get("artists"),
        genre=spec.get("genre"),
        url=spec.get("url"),
        comments=spec.get("comments"),
        channels=channels,
        patterns=patterns,
    )