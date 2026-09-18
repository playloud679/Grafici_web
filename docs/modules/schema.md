# Module: src/schema.py

Quantity catalog and column detection for AquaScan reports.

## Responsibility

- Maps every known AquaScan CSV column to a `Quantity` (label, unit, default
  scale, category, description).
- Auto-detects unknown numeric columns so no measurement is dropped.
- Provides UI grouping and display-label helpers.

## Public interface

- `Quantity` — frozen dataclass (`key`, `label`, `unit`, `scale`, `category`,
  `description`).
- `QUANTITY_SCHEMA` — dict keyed by exact CSV header.
- `CATEGORY_ORDER` — UI grouping order.
- `quantity_for(column) -> Quantity | None`
- `detect_quantities(df) -> list[Quantity]`
- `group_quantities(quantities) -> dict[str, list[Quantity]]`
- `display_label(q) -> str`

## Invariants

- `key` is always the exact CSV header so lookups and plotting stay aligned.
- `scale` is a multiplier applied to raw values before display. `Vbatt` uses
  `0.001` because the report stores millivolts.
- The ``Time`` column is never reported as a quantity.

## Edge cases

- Object columns holding numeric strings are detected via `pd.to_numeric`.
- Unknown columns get unit `""` and category `"Other"`.

## Validation

```bash
python -m unittest tests.test_schema -v
```
