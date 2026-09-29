"""Synthetic FHIR-like CSV seeds; JSON resources built in src."""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)

patients = pd.DataFrame({
    "patient_key": [f"P{i:04d}" for i in range(1, 41)],
    "given_name": ["Alex", "Jordan", "Sam", "Taylor", "Casey"] * 8,
    "family_name": ["Lee", "Patel", "Garcia", "Kim", "Nguyen"] * 8,
    "birth_date": pd.date_range("1965-01-01", periods=40, freq="200D").strftime("%Y-%m-%d"),
    "gender": ["male", "female", "other", "unknown"] * 10,
})
patients.to_csv(DATA / "patients_seed.csv", index=False)

encounters = pd.DataFrame({
    "encounter_id": [f"ENC{i:04d}" for i in range(1, 61)],
    "patient_key": [f"P{(i % 40) + 1:04d}" for i in range(1, 61)],
    "class_code": ["AMB", "EMER", "IMP", "VR"] * 15,
    "reason": ["checkup", "flu", "followup", "telehealth"] * 15,
})
encounters.to_csv(DATA / "encounters_seed.csv", index=False)
print("Wrote patients_seed.csv and encounters_seed.csv")
