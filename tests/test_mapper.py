import pandas as pd
import pytest

from src.mapper import MappingError, build_bundle, map_observation


def test_bp_becomes_two_observations():
    patients = pd.DataFrame(
        [{"patient_id": "P1", "mrn": "1", "family": "A", "given": "B", "sex": "F", "birth_date": "1980-01-01"}]
    )
    encounters = pd.DataFrame(
        [{"encounter_id": "E1", "patient_id": "P1", "pat_class": "I", "admit_ts": "2024-01-01", "discharge_ts": ""}]
    )
    observations = pd.DataFrame(
        [
            {"observation_id": "O1", "patient_id": "P1", "encounter_id": "E1", "loinc": "8480-6", "loinc_display": "SYS", "value": 120, "unit": "mmHg", "effective_ts": "2024-01-01"},
            {"observation_id": "O2", "patient_id": "P1", "encounter_id": "E1", "loinc": "8462-4", "loinc_display": "DIA", "value": 80, "unit": "mmHg", "effective_ts": "2024-01-01"},
        ]
    )
    bundle = build_bundle(patients, encounters, observations)
    obs = [e["resource"] for e in bundle["entry"] if e["resource"]["resourceType"] == "Observation"]
    assert len(obs) == 2


def test_missing_encounter_raises():
    with pytest.raises(MappingError):
        map_observation(
            {
                "observation_id": "O1",
                "patient_id": "P1",
                "encounter_id": "MISSING",
                "loinc": "8480-6",
                "value": 1,
                "unit": "mmHg",
                "effective_ts": "2024-01-01",
            },
            {"P1"},
            set(),
        )
