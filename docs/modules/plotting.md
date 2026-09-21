# Module: src/plotting.py

Matplotlib figure construction for multi-quantity comparisons.

## Responsibility

- Renders one stacked subplot per selected quantity, sharing the time axis.
- Draws original (thin, low-alpha) and filtered (bold) series per dataset.
- Applies the quantity scale and the per-dataset scale factor.
- Breaks lines across sampling gaps to avoid misleading connections.
- Draws NTU guard-threshold bands on the `Turbidity NTU` subplot: a yellow
  warning band between the two thresholds and a red alarm band above the high
  threshold.

## Public interface

- `create_plot(datasets, quantities, quantity_params, trim_params, display_options, ntu_thresholds=None) -> Figure`
- `_join_zero_gaps(times, values) -> ndarray` — replace interior zero runs with a
  straight line between the adjacent non-zero samples (per-quantity `join_zeros`).

`quantity_params` maps each quantity key to its own filter settings, falling
back to `filters.DEFAULT_FILTER_PARAMS`. `trim_params` is the synchronous
`{trim_start, trim_end}` row trim shared by every quantity. `display_options`
may include `plot_height` (inches per subplot, default 3.4).
`ntu_thresholds` optionally provides `(low, high)` NTU guard thresholds.

## Invariants

- Each subplot y-label carries the quantity unit (`label [unit]`).
- Only rows with valid (non-NaN) values for a quantity are plotted.
- The row trim is applied once per dataset, so every subplot shares the same
  time base and `xlim`.
- Every subplot shows its own date/time tick labels (`sharex=False`), so each
  chart is self-contained.

## Behavior notes

- If a quantity has `join_zeros` enabled, zeros are treated as missing and the
  interior runs are filled by time-based linear interpolation, so the line runs
  straight from the last non-zero sample to the next one. Zeros at the edges are
  kept.
- Filtering is applied per contiguous sampling segment (`_filter_with_gaps`),
  split only on gaps longer than 2 h. The regular ~15 min AquaScan sampling
  therefore stays in a single segment, so the filter controls take full effect.
- Smoothed values are clamped to the segment's observed range (`_smooth_segment`)
  so Savitzky-Golay overshoot (e.g. below zero) never appears.
- Filtering is best-effort: on failure the original series is kept and the
  exception is swallowed (original data is already drawn).
- The NTU bands are clipped to the auto y-range (they never force the axis to
  expand) and are drawn behind the data with ``zorder=0``.

## Edge cases

- Gaps larger than 2 h break lines (`_break_at_gaps`) and delimit filtering
  segments (`_filter_with_gaps`).
- Empty quantities render a "No data" placeholder instead of raising.

## Validation

```bash
python -m py_compile src/plotting.py
python -m unittest discover -s tests -v
```
