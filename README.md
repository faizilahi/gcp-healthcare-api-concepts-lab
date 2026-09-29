# FHIR Resource Mapping Notes - Patient, Encounter, Observation

Faiz Elahi - https://www.linkedin.com/in/faizilahi - https://pendataco.com - https://github.com/faizilahi

Portfolio notes + code for mapping synthetic clinical events into FHIR R4 resources the way a Healthcare API store would expect them. This is not a GCP product brochure and not a claim of a Google Cloud customer project.

## Patient

| Source column | FHIR path | Rule |
|---------------|-----------|------|
| `mrn` | `Patient.identifier[0].value` | system `urn:synthetic:mrn` |
| `family` / `given` | `Patient.name[0]` | official use |
| `birth_date` | `Patient.birthDate` | ISO date |
| `sex` | `Patient.gender` | F->female, M->male |

## Encounter

Inpatient rows become `Encounter.class = IMP` with `period.start` from admit. Ambulatory rows use `AMB`. `Encounter.subject.reference` must resolve to a Patient id already in the bundle.

## Observation (labs)

LOINC goes in `Observation.code.coding[0].code`. Quantity values use `valueQuantity`. BP panels that arrive as SYS/DIA pairs become **two** Observation resources sharing `Encounter` reference - never one Observation with two LOINCs smashed together.

## Bundle assembly order

1. Patient  
2. Encounter (subject -> Patient)  
3. Observation(s) (subject -> Patient, encounter -> Encounter)

`src/mapper.py` enforces that order and fails if an Observation references a missing Encounter.

```bash
pip install -r requirements.txt
python scripts/generate_clinical_events.py
python scripts/run_fhir_map.py
pytest -q
```

Synthetic events under `data/`; small enough for git.

---

Faiz Elahi - [LinkedIn](https://www.linkedin.com/in/faizilahi) - [pendataco.com](https://pendataco.com) - [GitHub](https://github.com/faizilahi)

