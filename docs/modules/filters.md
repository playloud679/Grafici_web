# Module: src/filters.py

Savitzky-Golay smoothing helpers.

## Responsibility

- Applies one or more Savitzky-Golay passes with an odd, capped window.

## Public interface

- `DEFAULT_FILTER_PARAMS` — default filter/trim settings dict.
- `apply_filter(data, window_length, poly_order, num_passes) -> ndarray`

## Behavior notes

- First pass keeps the requested window; subsequent passes shrink to 31 then
  15 to avoid over-flattening.
- The window is forced odd and capped to `len(data) - 1`.
- Short series (`len <= window`) are returned unchanged.

## Edge cases

- Non-finite input is passed through to `savgol_filter` unchanged; callers
  (plotting) already drop NaN before filtering.

## Validation

```bash
python -m unittest tests.test_filters -v
```
