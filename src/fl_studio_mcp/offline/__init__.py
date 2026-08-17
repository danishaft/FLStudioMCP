"""Offline .flp layer: parse and write .flp files without FL Studio running.

Tools here run purely on Python (pyflp) and are fully testable in CI.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from . import flp


def register(mcp: FastMCP) -> None:
    flp.register(mcp)