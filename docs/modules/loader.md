# Module: src/loader.py

Loading and pairing of AquaScan CSV reports.

## Responsibility

- Parses measurement CSVs (`*_data.csv`) sorted by `Time`.
- Parses location CSVs (`*_location_data.csv`) with `"longitude,latitude"`
  strings into `Latitude`/`Longitude`.
- Pairs companion files by stem and merges positions onto measurement rows.

## Public interface

- `DatasetSource` — dataclass (`name`, `data_file`, `location_file`).
- `classify_file(name) -> (kind, base)`
- `pair_uploaded_files(uploaded_files) -> list[DatasetSource]`
- `load_data_csv(file_obj) -> DataFrame`
- `load_location_csv(file_obj) -> DataFrame`
- `merge_location(df, loc) -> DataFrame`

## Invariants

- DataFrames are returned sorted by `Time` ascending.
- Location merge uses `merge_asof(direction="backward")`: each measurement row
  gets the last known position at or before its timestamp.
- Existing non-empty `Latitude`/`Longitude` columns in the data file win over
  the location file.

## Edge cases

- Location rows with unparsable coordinates are dropped.
- Missing `Time` raises `ValueError`; missing `Location` raises `ValueError`.

## Validation

```bash
python -m unittest tests.test_loader -v
```
