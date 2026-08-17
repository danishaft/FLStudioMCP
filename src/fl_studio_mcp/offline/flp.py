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


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def flp_info(path: str) -> dict:
        """Read project metadata from an .flp file: title, artists, genre, URL,
        comments, tempo (BPM), PPQ, FL version, file format, creation date, time
        spent, data path, and licensing. Note: .flp files do not store a musical
        key or time signature, so neither is reported."""
        return globals()["flp_info"](path)