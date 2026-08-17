"""Offline .flp tools: read project metadata from .flp files without FL Studio."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .core import load_project, safe_get


def flp_info(path: str) -> dict:
    """Read project metadata from an .flp file: title, artists, genre, URL,
    comments, tempo (BPM), PPQ, FL version, file format, creation date, time
    spent, data path, and licensing. Note: .flp files do not store a musical
    key or time signature, so neither is reported."""
    project = load_project(path)
    return {
        "path": str(path),
        "title": safe_get(project, "title"),
        "artists": safe_get(project, "artists"),
        "genre": safe_get(project, "genre"),
        "url": safe_get(project, "url"),
        "comments": safe_get(project, "comments"),
        "tempo_bpm": safe_get(project, "tempo"),
        "ppq": safe_get(project, "ppq"),
        "fl_version": _version_str(safe_get(project, "version")),
        "format": _enum_name_or_none(safe_get(project, "format")),
        "created_on": _iso_or_none(safe_get(project, "created_on")),
        "time_spent_seconds": _seconds_or_none(safe_get(project, "time_spent")),
        "data_path": safe_get(project, "data_path"),
        "licensed": safe_get(project, "licensed"),
        "licensee": safe_get(project, "licensee"),
        "looped": safe_get(project, "looped"),
        "show_info": safe_get(project, "show_info"),
        "pan_law": _enum_name_or_none(safe_get(project, "pan_law")),
    }


def _version_str(value) -> str | None:
    if value is None:
        return None
    try:
        build = value.build
        base = f"{value.major}.{value.minor}.{value.patch}"
        return base if build is None else f"{base}.{build}"
    except AttributeError:
        return str(value)


def _iso_or_none(value) -> str | None:
    if value is None:
        return None
    try:
        return value.isoformat()
    except (AttributeError, ValueError):
        return None


def _seconds_or_none(value) -> float | None:
    if value is None:
        return None
    try:
        return round(value.total_seconds(), 1)
    except AttributeError:
        return None


def _enum_name_or_none(value) -> str | None:
    if value is None:
        return None
    try:
        return value.name
    except AttributeError:
        return None


def _channel_entry(channel) -> dict:
    """Serialize a pyflp Channel for JSON output."""
    entry = {
        "iid": getattr(channel, "iid", None),
        "name": getattr(channel, "name", None),
        "type": type(channel).__name__,
        "internal_name": getattr(channel, "internal_name", None),
    }
    color = getattr(channel, "color", None)
    if color is not None:
        entry["color"] = str(color)
    sample_path = getattr(channel, "sample_path", None)
    if sample_path:
        entry["sample_path"] = str(sample_path)
    return entry


def _channels(project) -> list:
    """Iterate channels, tolerating projects without any channel events
    (pyflp raises KeyError or NoModelsFound depending on context)."""
    try:
        return list(project.channels)
    except (KeyError, Exception):
        return []


def _patterns(project) -> list:
    try:
        return list(project.patterns)
    except Exception:
        return []


def flp_channels(path: str) -> dict:
    """List every channel in the channel rack: index, name, type (Sampler,
    Instrument, Layer, Automation), plugin internal name, color, and sample
    path for sampler channels."""
    project = load_project(path)
    channels = [_channel_entry(c) for c in _channels(project)]
    return {"path": str(path), "count": len(channels), "channels": channels}


def flp_patterns(path: str) -> dict:
    """List every pattern: index, name, length in ticks, and note count."""
    project = load_project(path)
    patterns = []
    for pat in _patterns(project):
        patterns.append({
            "iid": getattr(pat, "iid", None),
            "name": getattr(pat, "name", None),
            "length": getattr(pat, "length", None),
            "note_count": len(list(pat.notes)),
        })
    return {"path": str(path), "count": len(patterns), "patterns": patterns}


def flp_notes(path: str, pattern_iid: int | None = None) -> dict:
    """Extract all MIDI notes, optionally filtered to one pattern. Each note
    reports key name, MIDI pitch, position and length in ticks, velocity
    (0-255), and the rack channel it plays on."""
    project = load_project(path)
    patterns = []
    for pat in _patterns(project):
        if pattern_iid is not None and getattr(pat, "iid", None) != pattern_iid:
            continue
        notes = [{
            "key": getattr(n, "key", None),
            "midi": n["key"],
            "position": getattr(n, "position", None),
            "length": getattr(n, "length", None),
            "velocity": getattr(n, "velocity", None),
            "rack_channel": getattr(n, "rack_channel", None),
        } for n in pat.notes]
        patterns.append({
            "iid": getattr(pat, "iid", None),
            "name": getattr(pat, "name", None),
            "notes": notes,
        })
    return {
        "path": str(path),
        "pattern": pattern_iid,
        "count": len(patterns),
        "patterns": patterns,
    }


def flp_plugins(path: str) -> dict:
    """List plugins loaded in channels: channel, internal name, plugin type,
    and the parsed parameter values stored in the plugin data."""
    project = load_project(path)
    plugins = []
    for c in _channels(project):
        plugin = getattr(c, "plugin", None)
        entry = {
            "channel_iid": getattr(c, "iid", None),
            "channel_name": getattr(c, "name", None),
            "internal_name": getattr(c, "internal_name", None),
        }
        if plugin is None:
            entry["plugin_type"] = None
            entry["params"] = {}
        else:
            entry["plugin_type"] = type(plugin).__name__
            entry["params"] = _plugin_params(plugin)
        plugins.append(entry)
    return {"path": str(path), "count": len(plugins), "plugins": plugins}


def _plugin_params(plugin) -> dict:
    """Extract named parameter values from the plugin's Data event container
    (e.g. Plucked: decay/color/normalize/gate/widen)."""
    try:
        event = plugin.events.first(213)
    except (KeyError, AttributeError):
        return {}
    value = getattr(event, "value", None)
    if not hasattr(value, "items"):
        return {}
    return {
        k: v if isinstance(v, (int, float, bool, str)) else str(v)
        for k, v in value.items()
    }


def flp_samples(path: str) -> dict:
    """List every sample referenced by sampler channels: channel and the
    stored sample path."""
    project = load_project(path)
    samples = []
    for c in _channels(project):
        sample_path = getattr(c, "sample_path", None)
        if not sample_path:
            continue
        samples.append({
            "channel_iid": getattr(c, "iid", None),
            "channel_name": getattr(c, "name", None),
            "sample_path": str(sample_path),
        })
    return {"path": str(path), "count": len(samples), "samples": samples}


def flp_tempo(path: str, bpm: float | None = None) -> dict:
    """Read the project tempo (BPM); when bpm is given, set it and save back
    to the same file."""
    project = load_project(path)
    if bpm is not None:
        if not 10 <= bpm <= 999:
            raise ValueError(f"tempo out of range: {bpm} (FL supports 10-999 BPM)")
        project.tempo = bpm
        _save(project, path)
    return {"path": str(path), "tempo_bpm": project.tempo, "ppq": project.ppq}


def flp_rename(path: str, renames: list[dict]) -> dict:
    """Rename channels and/or patterns in place. Each entry must be exactly
    one of {"channel_iid": int, "name": str} or {"pattern_iid": int,
    "name": str}. Returns what was applied."""
    project = load_project(path)
    applied = []
    for entry in renames:
        name = entry["name"]
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"invalid name in {entry!r}")
        if "channel_iid" in entry:
            target = next(
                (c for c in project.channels if getattr(c, "iid", None) == entry["channel_iid"]),
                None,
            )
            if target is None:
                raise ValueError(f"no channel with iid {entry['channel_iid']}")
            target.name = name
            applied.append({"kind": "channel", "iid": target.iid, "name": name})
        elif "pattern_iid" in entry:
            target = next(
                (p for p in project.patterns if getattr(p, "iid", None) == entry["pattern_iid"]),
                None,
            )
            if target is None:
                raise ValueError(f"no pattern with iid {entry['pattern_iid']}")
            target.name = name
            applied.append({"kind": "pattern", "iid": target.iid, "name": name})
        else:
            raise ValueError(f"entry must have channel_iid or pattern_iid: {entry!r}")
    _save(project, path)
    return {"path": str(path), "renamed": applied}


def flp_diff(base: str, other: str) -> dict:
    """Structural diff of two .flp files: tempo, PPQ, channels, patterns, and
    note counts. Reports what was added, removed, and changed in `other`
    relative to `base`."""
    a = load_project(base)
    b = load_project(other)
    out: dict = {"base": str(base), "other": str(other)}

    if a.tempo != b.tempo:
        out["tempo"] = {"base": a.tempo, "other": b.tempo}
    if a.ppq != b.ppq:
        out["ppq"] = {"base": a.ppq, "other": b.ppq}

    try:
        a_ch = {getattr(c, "iid", None): c for c in a.channels}
    except KeyError:
        a_ch = {}
    try:
        b_ch = {getattr(c, "iid", None): c for c in b.channels}
    except KeyError:
        b_ch = {}
    removed = []
    for iid, c in a_ch.items():
        if iid not in b_ch:
            removed.append({"iid": iid, "name": getattr(c, "name", None)})
    added = []
    changed = []
    for iid, c in b_ch.items():
        if iid not in a_ch:
            added.append({"iid": iid, "name": getattr(c, "name", None)})
            continue
        old = a_ch[iid]
        fields = {
            "name": (getattr(old, "name", None), getattr(c, "name", None)),
            "type": (type(old).__name__, type(c).__name__),
            "sample_path": (
                str(getattr(old, "sample_path", None) or ""),
                str(getattr(c, "sample_path", None) or ""),
            ),
        }
        diffs = {k: {"base": x, "other": y} for k, (x, y) in fields.items() if x != y}
        if diffs:
            changed.append({"iid": iid, **diffs})
    if removed:
        out["channels_removed"] = removed
    if added:
        out["channels_added"] = added
    if changed:
        out["channels_changed"] = changed

    a_pat = {getattr(p, "iid", None): p for p in a.patterns}
    b_pat = {getattr(p, "iid", None): p for p in b.patterns}
    removed = [{"iid": iid, "name": getattr(p, "name", None)} for iid, p in a_pat.items() if iid not in b_pat]
    added = [{"iid": iid, "name": getattr(p, "name", None)} for iid, p in b_pat.items() if iid not in a_pat]
    changed = []
    for iid, p in b_pat.items():
        if iid not in a_pat:
            continue
        old = a_pat[iid]
        old_count = len(list(old.notes))
        new_count = len(list(p.notes))
        diffs = {}
        if getattr(old, "name", None) != getattr(p, "name", None):
            diffs["name"] = {"base": getattr(old, "name", None), "other": getattr(p, "name", None)}
        if getattr(old, "length", None) != getattr(p, "length", None):
            diffs["length"] = {"base": getattr(old, "length", None), "other": getattr(p, "length", None)}
        if old_count != new_count:
            diffs["note_count"] = {"base": old_count, "other": new_count}
        if diffs:
            changed.append({"iid": iid, **diffs})
    if removed:
        out["patterns_removed"] = removed
    if added:
        out["patterns_added"] = added
    if changed:
        out["patterns_changed"] = changed
    return out


def flp_template(source: str, output: str) -> dict:
    """Create a project template from an existing project: copy it with all
    patterns (and their notes) removed, keeping channels, plugins, and
    project settings."""
    project = load_project(source)
    _strip_patterns(project)
    _save(project, output)
    return {"source": str(source), "output": str(output), "template": True}


def flp_merge(base: str, other: str, output: str) -> dict:
    """Merge two projects: keep `base` as-is, append `other`'s channels and
    patterns with renumbered ids. Note references are remapped to the merged
    channel ids. Project metadata (tempo, title, ...) is taken from `base`."""
    from pyflp._events import IndexedEvent

    a = load_project(base)
    b = load_project(other)

    a_channels = _channels(a)
    b_channels = _channels(b)
    channel_offset = len(a_channels)

    a_patterns = _patterns(a)
    b_patterns = _patterns(b)
    pattern_offset = len(a_patterns)

    for c in b_channels:
        c.events.first(64).value += channel_offset
    for pat in b_patterns:
        pat.events.first(65).value += pattern_offset
        for note in pat.notes:
            note.rack_channel += channel_offset
        for ie in pat.events.lst:
            if ie.e.id == 160:  # PatternID.ChannelIID
                ie.e.value += channel_offset

    root_offset = max(ie.r for ie in a.events.lst) + 1
    for ie in b.events.lst:
        a.events.lst.add(IndexedEvent(ie.r + root_offset, ie.e))

    _save(a, output)
    return {
        "base": str(base),
        "other": str(other),
        "output": str(output),
        "channels": len(a_channels) + len(b_channels),
        "patterns": len(a_patterns) + len(b_patterns),
    }


def _strip_patterns(project) -> int:
    """Remove all pattern events (PatternID.*) from a project. Returns how
    many events were removed."""
    from pyflp.pattern import PatternID

    pattern_ids = {e.value for e in PatternID}
    kept = [ie for ie in project.events.lst if ie.e.id not in pattern_ids]
    removed = len(project.events.lst) - len(kept)
    project.events.lst.clear()
    project.events.lst.update(kept)
    return removed


def _save(project, path: str) -> None:
    import pyflp

    pyflp.save(project, path)


def flp_generate(path: str, spec: dict) -> dict:
    """Generate a new .flp project from a JSON spec and write it to disk.
    spec keys: title/artists/genre/url/comments (str|None), tempo_bpm (float),
    ppq (int), channels [{name, type ("sampler"/"native"/"layer"/
    "instrument"/"automation" or int), sample_path, internal_name,
    plugin_data (base64)}], patterns [{name, length,
    notes [{rack_channel, key (MIDI 0-131), position, length, velocity}]}].
    Channel and pattern ids are assigned automatically in list order."""
    from .writer import write_flp_from_spec

    write_flp_from_spec(path, spec)
    return {"path": str(path), "written": True}


def flp_validate(path: str) -> dict:
    """Integrity-check an .flp file: verifies it parses, and reports
    consistency warnings (notes pointing at missing channels, patterns
    without names, zero-length patterns, duplicate channel/pattern ids)."""
    import pyflp
    from pyflp.channel import ChannelID
    from pyflp.pattern import PatternID

    warnings: list[str] = []
    try:
        project = load_project(path)
    except ValueError as exc:
        return {"path": str(path), "ok": False, "errors": [str(exc)], "warnings": []}
    channels = _channels(project)
    patterns = _patterns(project)

    channel_iids = [getattr(c, "iid", None) for c in channels]
    seen = set()
    for iid in channel_iids:
        if iid in seen:
            warnings.append(f"duplicate channel iid {iid}")
        seen.add(iid)
    pattern_iids = [getattr(p, "iid", None) for p in patterns]
    seen = set()
    for iid in pattern_iids:
        if iid in seen:
            warnings.append(f"duplicate pattern iid {iid}")
        seen.add(iid)

    for pat in patterns:
        if not getattr(pat, "name", None):
            warnings.append(f"pattern {getattr(pat, 'iid', None)} has no name")
        if getattr(pat, "length", 0) <= 0:
            warnings.append(f"pattern {getattr(pat, 'iid', None)} has zero length")
        for note in pat.notes:
            rack = getattr(note, "rack_channel", None)
            if rack not in channel_iids:
                warnings.append(
                    f"pattern {getattr(pat, 'iid', None)}: note {getattr(note, 'key', None)} "
                    f"at {getattr(note, 'position', None)} references missing channel {rack}"
                )
    return {
        "path": str(path),
        "ok": not warnings,
        "errors": [],
        "warnings": warnings,
        "channels": len(channels),
        "patterns": len(patterns),
    }


def flp_analyze(path: str) -> dict:
    """Structural report of a project: channel and pattern counts, tempo, PPQ,
    FL version, note totals, MIDI range, and per-pattern density."""
    project = load_project(path)
    channels = _channels(project)
    patterns = _patterns(project)

    type_counts: dict[str, int] = {}
    for c in channels:
        type_counts[type(c).__name__] = type_counts.get(type(c).__name__, 0) + 1

    all_midi = []
    pattern_stats = []
    for pat in patterns:
        midis = [n["key"] for n in pat.notes]
        all_midi.extend(midis)
        pattern_stats.append({
            "iid": getattr(pat, "iid", None),
            "name": getattr(pat, "name", None),
            "length": getattr(pat, "length", None),
            "notes": len(midis),
        })
    return {
        "path": str(path),
        "tempo_bpm": getattr(project, "tempo", None),
        "ppq": getattr(project, "ppq", None),
        "fl_version": _version_str(getattr(project, "version", None)),
        "channels": len(channels),
        "channel_types": type_counts,
        "patterns": len(patterns),
        "total_notes": len(all_midi),
        "midi_range": (
            {"lowest": min(all_midi), "highest": max(all_midi)} if all_midi else None
        ),
        "pattern_stats": pattern_stats,
    }


def flp_batch(directory: str, action: str, bpm: float | None = None) -> dict:
    """Apply an action to every .flp file in a directory.

    actions:
      info      - metadata summary per file (flp-info style)
      validate  - integrity check per file
      analyze   - structural report per file
      tempo     - set all files to the given bpm (requires bpm)
      template  - write <name>_template.flp with patterns stripped
    """
    from pathlib import Path

    root = Path(directory)
    if not root.is_dir():
        raise ValueError(f"not a directory: {directory}")
    if action == "tempo" and bpm is None:
        raise ValueError("tempo action requires bpm")

    files = sorted(root.glob("*.flp"))
    results = []
    failures = []
    for f in files:
        try:
            if action == "info":
                info = flp_info(str(f))
                results.append({"file": str(f), "title": info["title"],
                                "tempo_bpm": info["tempo_bpm"]})
            elif action == "validate":
                results.append({"file": str(f), **flp_validate(str(f))})
            elif action == "analyze":
                results.append({"file": str(f), **flp_analyze(str(f))})
            elif action == "tempo":
                flp_tempo(str(f), bpm=bpm)
                results.append({"file": str(f), "tempo_bpm": bpm})
            elif action == "template":
                out = f.with_name(f.stem + "_template.flp")
                flp_template(str(f), str(out))
                results.append({"file": str(f), "template": str(out)})
            else:
                raise ValueError(f"unknown action {action!r} "
                                 f"(use info, validate, analyze, tempo, template)")
        except Exception as exc:
            failures.append({"file": str(f), "error": str(exc)})
    return {
        "directory": str(root),
        "action": action,
        "files": len(files),
        "results": results,
        "failures": failures,
    }


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def flp_info(path: str) -> dict:
        """Read project metadata from an .flp file: title, artists, genre, URL,
        comments, tempo (BPM), PPQ, FL version, file format, creation date, time
        spent, data path, and licensing. Note: .flp files do not store a musical
        key or time signature, so neither is reported."""
        return globals()["flp_info"](path)

    @mcp.tool()
    def flp_channels(path: str) -> dict:
        """List every channel in the channel rack: index, name, type (Sampler,
        Instrument, Layer, Automation), plugin internal name, color, and sample
        path for sampler channels."""
        return globals()["flp_channels"](path)

    @mcp.tool()
    def flp_patterns(path: str) -> dict:
        """List every pattern: index, name, length in ticks, and note count."""
        return globals()["flp_patterns"](path)

    @mcp.tool()
    def flp_notes(path: str, pattern_iid: int | None = None) -> dict:
        """Extract all MIDI notes, optionally filtered to one pattern. Each note
        reports key name, MIDI pitch, position and length in ticks, velocity
        (0-255), and the rack channel it plays on."""
        return globals()["flp_notes"](path, pattern_iid)

    @mcp.tool()
    def flp_plugins(path: str) -> dict:
        """List plugins loaded in channels: channel, internal name, plugin type,
        and the parsed parameter values stored in the plugin data."""
        return globals()["flp_plugins"](path)

    @mcp.tool()
    def flp_samples(path: str) -> dict:
        """List every sample referenced by sampler channels: channel and the
        stored sample path."""
        return globals()["flp_samples"](path)

    @mcp.tool()
    def flp_tempo(path: str, bpm: float | None = None) -> dict:
        """Read the project tempo (BPM); when bpm is given, set it and save back
        to the same file."""
        return globals()["flp_tempo"](path, bpm)

    @mcp.tool()
    def flp_rename(path: str, renames: list[dict]) -> dict:
        """Rename channels and/or patterns in place. Each entry must be exactly
        one of {"channel_iid": int, "name": str} or {"pattern_iid": int,
        "name": str}. Returns what was applied."""
        return globals()["flp_rename"](path, renames)

    @mcp.tool()
    def flp_diff(base: str, other: str) -> dict:
        """Structural diff of two .flp files: tempo, PPQ, channels, patterns,
        and note counts. Reports what was added, removed, and changed in
        `other` relative to `base`."""
        return globals()["flp_diff"](base, other)

    @mcp.tool()
    def flp_template(source: str, output: str) -> dict:
        """Create a project template from an existing project: copy it with all
        patterns (and their notes) removed, keeping channels, plugins, and
        project settings."""
        return globals()["flp_template"](source, output)

    @mcp.tool()
    def flp_merge(base: str, other: str, output: str) -> dict:
        """Merge two projects: keep `base` as-is, append `other`'s channels and
        patterns with renumbered ids. Note references are remapped to the
        merged channel ids. Project metadata (tempo, title, ...) is taken from
        `base`."""
        return globals()["flp_merge"](base, other, output)

    @mcp.tool()
    def flp_generate(path: str, spec: dict) -> dict:
        """Generate a new .flp project from a JSON spec and write it to disk.
        spec keys: title/artists/genre/url/comments (str|None), tempo_bpm
        (float), ppq (int), channels [{name, type ("sampler"/"native"/"layer"/
        "instrument"/"automation" or int), sample_path, internal_name,
        plugin_data (base64)}], patterns [{name, length,
        notes [{rack_channel, key (MIDI 0-131), position, length, velocity}]}].
        Channel and pattern ids are assigned automatically in list order."""
        return globals()["flp_generate"](path, spec)

    @mcp.tool()
    def flp_validate(path: str) -> dict:
        """Integrity-check an .flp file: verifies it parses, and reports
        consistency warnings (notes pointing at missing channels, patterns
        without names, zero-length patterns, duplicate channel/pattern ids)."""
        return globals()["flp_validate"](path)

    @mcp.tool()
    def flp_analyze(path: str) -> dict:
        """Structural report of a project: channel and pattern counts, tempo,
        PPQ, FL version, note totals, MIDI range, and per-pattern density."""
        return globals()["flp_analyze"](path)

    @mcp.tool()
    def flp_batch(directory: str, action: str, bpm: float | None = None) -> dict:
        """Apply an action to every .flp file in a directory.
        actions: info (metadata summary), validate (integrity check),
        analyze (structural report), tempo (set all to `bpm`), template (write
        <name>_template.flp with patterns stripped)."""
        return globals()["flp_batch"](directory, action, bpm)