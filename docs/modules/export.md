# Module: src/export.py

Raw measurement export preparation for the AquaScan report viewer.

## Responsibility

- Combines every enabled dataset into a single raw export frame.
- Applies the same synchronous initial/final row trim used by the chart, so
  the exported rows match exactly what is plotted.
- Sorts the combined rows by `Time` and prepends a `Campione` column with
  values `1..n` starting from the first acquired sample in time order.
- Selects the exported columns: `Campione` and `Time` are fixed (always
  included); every other column is toggleable by the user and disabled by
  default. When data columns are selected, rows where every selected column is
  empty are dropped and `Campione` is renumbered `1..n` in time order.
- Computes two NTU guard-threshold exceedance columns (`Soglia {low} NTU`,
  `Soglia {high} NTU`) with adjustable thresholds (defaults 4 and 7).
- Writes the XLSX with row highlighting: yellow when only the first threshold
  is exceeded, red when the second threshold is exceeded.

## Public interface

- `SAMPLE_COLUMN` — the name of the added sample-number column (`"Campione"`).
- `FIXED_COLUMNS` — tuple of columns always exported (`Campione`, `Time`).
- `build_export_frame(datasets, trim_params) -> DataFrame` — builds the
  combined, trimmed, sample-numbered frame; returns an empty DataFrame when no
  enabled data remains.
- `selectable_columns(frame) -> list[str]` — the data columns the user can
  toggle (everything except the fixed columns).
- `subset_export(frame, selected_columns, thresholds=None) -> DataFrame` —
  returns `Campione` + `Time` + the chosen columns, ignoring unknown/fixed
  names; drops rows with no value in any selected column, renumbers
  `Campione`, and appends the threshold columns when `thresholds` is given.
- `threshold_columns(frame, low, high) -> DataFrame` — two exceedance columns
  for `Turbidity NTU` (1 when `>=` threshold, 0 otherwise, NaN when no data).
- `threshold_column_names(low, high) -> tuple[str, str]` — the two exceedance
  column names.
- `write_export_xlsx(frame, thresholds, buffer) -> None` — writes the frame as
  XLSX and applies yellow/red row fills based on the threshold columns.

## Invariants

- `datasets` items are dicts with a `data` DataFrame and an `enabled` flag;
  disabled datasets are skipped.
- `trim_params` provides `trim_start` and `trim_end` (row counts removed from
  each report's head/tail respectively).
- The trim matches `plotting._trim`, so a given configuration exports the same
  rows that are plotted. The small duplication avoids importing the heavy
  matplotlib plotting module in the export path.
- The `Campione` column is the first column and is assigned after the global
  time sort, so sample 1 is the earliest acquired row across all datasets.
- Exported columns are always ordered `Campione`, `Time`, then the selected
  data columns in their original order; fixed columns can never be duplicated
  or removed by `subset_export`.
- When one or more data columns are selected, rows where all of them are NaN
  are dropped (the interleaved AquaScan format would otherwise export mostly
  empty rows), and `Campione` is renumbered `1..n` in time order over the
  surviving rows. With no data columns selected, all rows are kept.
- Threshold columns are appended after the selected data columns, are computed
  from the raw `Turbidity NTU` values, and use inclusive ``>=`` comparison
  (1 at or above the threshold, 0 otherwise, empty when turbidity is missing).
- Row highlighting takes precedence: the second threshold (red) wins over the
  first (yellow) when both are exceeded; the fill spans the whole row.

## Edge cases

- When the trim removes an entire report (`trim_start + trim_end >= len`), that
  report is dropped.
- When no enabled data remains, the result is an empty DataFrame (the UI shows
  an informational message instead of a download button).

## Validation

```bash
python -m unittest tests.test_export -v
```
