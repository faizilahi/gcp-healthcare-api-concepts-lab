#!/usr/bin/env python3
from __future__ import annotations

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
RNG = random.Random(7)


def main() -> None:
    patients, encounters, observations = [], [], []
    obs_n = 0
    for i in range(1, 201):
        pid = f"P{i:04d}"
        patients.append(
            {
                "patient_id": pid,
                "mrn": f"MRN{i:06d}",
                "family": RNG.choice(["Nguyen", "Brooks", "Ali", "Cohen", "Diaz"]),
                "given": RNG.choice(["Alex", "Sam", "Jordan", "Riley", "Casey"]),
                "sex": RNG.choice(["F", "M"]),
                "birth_date": f"{RNG.randint(1948,2002)}-{RNG.randint(1,12):02d}-{RNG.randint(1,28):02d}",
            }
        )
        for j in range(RNG.randint(1, 3)):
            eid = f"E{i:04d}-{j}"
            admit = datetime(2024, 1, 1) + timedelta(days=RNG.randint(0, 300), hours=RNG.randint(0, 20))
            inpatient = RNG.random() < 0.45
            discharge = admit + timedelta(days=RNG.randint(1, 8)) if inpatient else ""
            encounters.append(
                {
                    "encounter_id": eid,
                    "patient_id": pid,
                    "pat_class": "I" if inpatient else "O",
                    "admit_ts": admit.isoformat(sep=" "),
                    "discharge_ts": discharge.isoformat(sep=" ") if discharge else "",
                }
            )
            # BP as two observations
            for loinc, display, unit, lo, hi in (
                ("8480-6", "Systolic blood pressure", "mmHg", 100, 170),
                ("8462-4", "Diastolic blood pressure", "mmHg", 60, 110),
            ):
                obs_n += 1
                observations.append(
                    {
                        "observation_id": f"O{obs_n:06d}",
                        "patient_id": pid,
                        "encounter_id": eid,
                        "loinc": loinc,
                        "loinc_display": display,
                        "value": RNG.randint(lo, hi),
                        "unit": unit,
                        "effective_ts": (admit + timedelta(minutes=30)).isoformat(sep=" "),
                    }
                )
    pd.DataFrame(patients).to_csv(DATA / "patients.csv", index=False)
    pd.DataFrame(encounters).to_csv(DATA / "encounters.csv", index=False)
    pd.DataFrame(observations).to_csv(DATA / "observations.csv", index=False)
    print(f"events: {len(patients)} patients, {len(encounters)} encounters, {len(observations)} observations")


if __name__ == "__main__":
    main()
