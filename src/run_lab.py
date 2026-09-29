"""Build FHIR JSON from seeds and validate with fhir.resources."""
import json
from pathlib import Path
import pandas as pd
from fhir.resources.patient import Patient
from fhir.resources.encounter import Encounter
from fhir.resources.humanname import HumanName

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "data" / "fhir_store"
STORE.mkdir(parents=True, exist_ok=True)
patients = pd.read_csv(ROOT / "data" / "patients_seed.csv")
encounters = pd.read_csv(ROOT / "data" / "encounters_seed.csv")

for _, row in patients.iterrows():
    p = Patient(
        resourceType="Patient",
        id=row.patient_key,
        name=[HumanName(family=row.family_name, given=[row.given_name])],
        birthDate=str(row.birth_date),
        gender=row.gender,
    )
    (STORE / f"Patient-{row.patient_key}.json").write_text(p.model_dump_json(indent=2, by_alias=True), encoding="utf-8")

for _, row in encounters.iterrows():
    e = Encounter.model_validate({
        "resourceType": "Encounter",
        "id": row.encounter_id,
        "status": "finished",
        "class": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": row.class_code,
            }]
        }],
        "subject": {"reference": f"Patient/{row.patient_key}"},
    })
    (STORE / f"Encounter-{row.encounter_id}.json").write_text(e.model_dump_json(indent=2, by_alias=True), encoding="utf-8")

print(f"Wrote {len(list(STORE.glob('*.json')))} FHIR JSON files to {STORE}")
