"""Optional warehouse flatten from FHIR bundle for analytics joins."""
from __future__ import annotations

from typing import Any

import pandas as pd


def observations_flat(bundle: dict[str, Any]) -> pd.DataFrame:
    rows = []
    for e in bundle.get("entry", []):
        r = e["resource"]
        if r["resourceType"] != "Observation":
            continue
        rows.append(
            {
                "observation_id": r["id"],
                "patient_id": r["subject"]["reference"].split("/")[-1],
                "encounter_id": r["encounter"]["reference"].split("/")[-1],
                "loinc": r["code"]["coding"][0]["code"],
                "value": r["valueQuantity"]["value"],
                "unit": r["valueQuantity"].get("unit", ""),
                "effective_ts": r["effectiveDateTime"],
            }
        )
    return pd.DataFrame(rows)
