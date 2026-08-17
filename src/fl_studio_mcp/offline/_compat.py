"""Compatibility shim for pyflp on Python 3.13+.

Python 3.13 changed ``EnumMeta.__call__``: calling an *empty* enum with a value
now raises ``TypeError`` before ``_missing_`` is ever consulted. pyflp relies on
``EventEnum(id)`` (an empty enum) to resolve *unknown* event IDs from the file
via ``_missing_``, so every ``pyflp.parse()`` crashes on 3.13 with:

    TypeError: <enum 'EventEnum'> has no members; ...

This patch restores the pre-3.13 behaviour only for the empty-enum case; normal
member lookups still go through the standard ``__new__`` path. It is a no-op on
Python < 3.13, so the package keeps working on 3.11/3.12 (e.g. on Windows).

Verified against pyflp 2.2.1.
"""

from __future__ import annotations

from pyflp._events import EventEnum, _EventEnumMeta

_orig_call = _EventEnumMeta.__call__


def _patched_call(cls, value, names=None, *values, **kw):
    if names is None:
        if cls._member_map_:
            return cls.__new__(cls, value)
        member = cls._missing_(value)
        if member is not None:
            return member
        raise TypeError(
            f"{cls} has no members; specify `names=()` if you meant to "
            "create a new, empty, enum"
        )
    return _orig_call(cls, value, names, *values, **kw)


_EventEnumMeta.__call__ = _patched_call