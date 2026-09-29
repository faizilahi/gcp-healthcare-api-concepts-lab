#!/usr/bin/env python3
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.flatten import observations_flat
from src.mapper import build_bundle, resource_counts
from src.validate import validate_bundle

DATA = ROOT / "data"
OUTPUT = ROOT / "output"


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    patients = pd.read_csv(DATA / "patients.csv")
    encounters = pd.read_csv(DATA / "encounters.csv").fillna("")
    observations = pd.read_csv(DATA / "observations.csv")
    bundle = build_bundle(patients, encounters, observations)
    errors = validate_bundle(bundle)
    counts = resource_counts(bundle)
    print("=== FHIR bundle resource counts ===")
    print(json.dumps(counts, indent=2))
    print("validation_errors:", errors)
    (OUTPUT / "bundle.json").write_text(json.dumps(bundle, indent=2), encoding="utf-8")
    observations_flat(bundle).to_csv(OUTPUT / "observations_flat.csv", index=False)
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
