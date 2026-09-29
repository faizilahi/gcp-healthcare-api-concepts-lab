"""Map tabular clinical events to FHIR R4 resources + bundle."""
from __future__ import annotations

from typing import Any

import pandas as pd

from .codes import CLASS, GENDER, LOINC_SYSTEM, MRN_SYSTEM


class MappingError(Exception):
    pass


def map_patient(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "resourceType": "Patient",
        "id": row["patient_id"],
        "identifier": [{"system": MRN_SYSTEM, "value": row["mrn"]}],
        "name": [
            {
                "use": "official",
                "family": row["family"],
                "given": [row["given"]],
            }
        ],
        "gender": GENDER.get(str(row["sex"]).upper(), "unknown"),
        "birthDate": str(row["birth_date"])[:10],
    }


def map_encounter(row: dict[str, Any], patient_ids: set[str]) -> dict[str, Any]:
    if row["patient_id"] not in patient_ids:
        raise MappingError(f"Encounter {row['encounter_id']} references missing patient")
    return {
        "resourceType": "Encounter",
        "id": row["encounter_id"],
        "status": "finished" if row.get("discharge_ts") else "in-progress",
        "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": CLASS.get(row["pat_class"], "AMB")},
        "subject": {"reference": f"Patient/{row['patient_id']}"},
        "period": {
            "start": str(row["admit_ts"]),
            **({"end": str(row["discharge_ts"])} if row.get("discharge_ts") else {}),
        },
    }


def map_observation(row: dict[str, Any], patient_ids: set[str], encounter_ids: set[str]) -> dict[str, Any]:
    if row["patient_id"] not in patient_ids:
        raise MappingError(f"Observation {row['observation_id']} missing patient")
    if row["encounter_id"] not in encounter_ids:
        raise MappingError(f"Observation {row['observation_id']} missing encounter {row['encounter_id']}")
    return {
        "resourceType": "Observation",
        "id": row["observation_id"],
        "status": "final",
        "code": {
            "coding": [
                {
                    "system": LOINC_SYSTEM,
                    "code": row["loinc"],
                    "display": row.get("loinc_display", row["loinc"]),
                }
            ]
        },
        "subject": {"reference": f"Patient/{row['patient_id']}"},
        "encounter": {"reference": f"Encounter/{row['encounter_id']}"},
        "effectiveDateTime": str(row["effective_ts"]),
        "valueQuantity": {
            "value": float(row["value"]),
            "unit": row.get("unit", ""),
            "system": "http://unitsofmeasure.org",
            "code": row.get("unit", ""),
        },
    }


def build_bundle(
    patients: pd.DataFrame,
    encounters: pd.DataFrame,
    observations: pd.DataFrame,
) -> dict[str, Any]:
    entries = []
    patient_ids = set()
    for _, r in patients.iterrows():
        res = map_patient(r.to_dict())
        patient_ids.add(res["id"])
        entries.append({"resource": res})

    encounter_ids = set()
    for _, r in encounters.iterrows():
        res = map_encounter(r.to_dict(), patient_ids)
        encounter_ids.add(res["id"])
        entries.append({"resource": res})

    for _, r in observations.iterrows():
        res = map_observation(r.to_dict(), patient_ids, encounter_ids)
        entries.append({"resource": res})

    return {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": entries,
    }


def resource_counts(bundle: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for e in bundle.get("entry", []):
        rt = e["resource"]["resourceType"]
        counts[rt] = counts.get(rt, 0) + 1
    return counts
