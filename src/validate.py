"""Structural checks on mapped bundles."""
from __future__ import annotations

from typing import Any


def validate_bundle(bundle: dict[str, Any]) -> list[str]:
    errors = []
    ids = {}
    for e in bundle.get("entry", []):
        r = e["resource"]
        key = (r["resourceType"], r["id"])
        if key in ids:
            errors.append(f"duplicate {key}")
        ids[key] = True
    patient_ids = {i for (rt, i) in ids if rt == "Patient"}
    encounter_ids = {i for (rt, i) in ids if rt == "Encounter"}
    for e in bundle.get("entry", []):
        r = e["resource"]
        if r["resourceType"] == "Encounter":
            ref = r["subject"]["reference"].split("/", 1)[-1]
            if ref not in patient_ids:
                errors.append(f"Encounter {r['id']} bad subject {ref}")
        if r["resourceType"] == "Observation":
            pref = r["subject"]["reference"].split("/", 1)[-1]
            eref = r["encounter"]["reference"].split("/", 1)[-1]
            if pref not in patient_ids:
                errors.append(f"Observation {r['id']} bad subject")
            if eref not in encounter_ids:
                errors.append(f"Observation {r['id']} bad encounter")
    return errors
