"""Shared machinery for the offline .flp layer: parsing and safe extraction.

All offline tools use exactly one entry point: :func:`load_project`, which
normalises every failure mode (missing file, corrupt data, unsupported format)
into a single clear :class:`ValueError`. Field extraction is defensive: any
field a given .flp does not store comes back as ``None`` instead of crashing,
because real-world files (trial exports, old versions) omit events.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pyflp

from . import _compat  # noqa: F401  (must run before any parse)


def load_project(path: str | Path) -> pyflp.Project:
    """Parse an .flp file, raising ValueError with a precise reason on failure."""
    p = Path(path)
    if not p.exists():
        raise ValueError(f"file not found: {p}")
    if not p.is_file():
        raise ValueError(f"not a file: {p}")
    try:
        return pyflp.parse(p)
    except pyflp.HeaderCorrupted as exc:
        raise ValueError(f"corrupt .flp header: {exc}") from exc
    except pyflp.VersionNotDetected as exc:
        raise ValueError(f"unrecognised .flp version: {exc}") from exc
    except Exception as exc:
        raise ValueError(f"failed to parse {p}: {exc}") from exc


def safe_get(obj: Any, name: str, default: Any = None) -> Any:
    """Read a model attribute defensively; absent events become None."""
    try:
        return getattr(obj, name)
    except (KeyError, ValueError, TypeError, AttributeError):
        return default