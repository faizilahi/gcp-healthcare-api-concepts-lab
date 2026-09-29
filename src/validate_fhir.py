"""Validate FHIR JSON files in data/fhir_store."""
from pathlib import Path
import json
from fhir.resources.patient import Patient
from fhir.resources.encounter import Encounter

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "data" / "fhir_store"
ok = bad = 0
for path in STORE.glob("*.json"):
    data = json.loads(path.read_text(encoding="utf-8"))
    try:
        if data["resourceType"] == "Patient":
            Patient.model_validate(data)
        elif data["resourceType"] == "Encounter":
            Encounter.model_validate(data)
        ok += 1
    except Exception as exc:
        bad += 1
        print(f"INVALID {path.name}: {exc}")
print(f"Validation complete: {ok} valid, {bad} invalid")
