"""Bundle diff helpers for mapping regressions."""
from __future__ import annotations

from typing import Any


def index_by_type_id(bundle: dict[str, Any]) -> dict[tuple[str, str], dict]:
    out = {}
    for e in bundle.get("entry", []):
        r = e["resource"]
        out[(r["resourceType"], r["id"])] = r
    return out


def added_or_removed(before: dict[str, Any], after: dict[str, Any]) -> dict[str, list]:
    b = set(index_by_type_id(before))
    a = set(index_by_type_id(after))
    return {
        "added": sorted(f"{t}/{i}" for t, i in (a - b)),
        "removed": sorted(f"{t}/{i}" for t, i in (b - a)),
    }
