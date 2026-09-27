"""Matplotlib figure construction for multi-quantity comparisons.

Renders one vertically stacked subplot per selected quantity. The row trim is
synchronous for the whole report (a single shared time base), while the
Savitzky-Golay filter parameters are configured independently per quantity.
Every subplot shows its own date/time axis so each chart is self-contained.

Filtering is applied per contiguous segment (split only on gaps longer than
2 h) and clamped to the observed range, so AquaScan's irregular timestamps do
not produce misleading smoothed lines or physically impossible values.

Module documentation: ``docs/modules/plotting.md``.
"""

from __future__ import annotations

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from filters import DEFAULT_FILTER_PARAMS, apply_filter

_COLORS = [
    "#1f77b4", "#d62728", "#2ca02c", "#ff7f0e", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#17becf", "#bcbd22",
]

# Gaps larger than this are treated as separate sampling segments / line breaks.
# Normal AquaScan sampling is ~15 min, so 2 h keeps the series contiguous while
# still breaking on real device outages.
_MAX_GAP_S = 7200  # 2 hours


def _break_at_gaps(times, values, max_gap_s: int = _MAX_GAP_S):
    """Insert NaN separators into ``values`` where consecutive timestamps are
    farther apart than ``max_gap_s`` seconds, breaking the line across gaps."""
    t_list = []
    v_list = []
    prev = None
    for t, v in zip(times, values):
        if prev is not None and (t - prev) > pd.Timedelta(seconds=max_gap_s):
            t_list.append(prev + pd.Timedelta(seconds=1))
            v_list.append(np.nan)
        t_list.append(t)
        v_list.append(v)
        prev = t
    return t_list, np.asarray(v_list, dtype=float)


def _smooth_segment(segment, filter_params):
    """Smooth one contiguous segment and clamp to its observed range.

    Savitzky-Golay can overshoot (e.g. below zero) at sharp transitions; the
    clamp keeps physical quantities inside their measured interval.
    """
    if len(segment) < 3:
        return segment
    smoothed = apply_filter(
        segment,
        filter_params["window_length"],
        filter_params["poly_order"],
        filter_params["num_passes"],
    )
    lo = float(np.nanmin(segment))
    hi = float(np.nanmax(segment))
    return np.clip(smoothed, lo, hi)


def _filter_with_gaps(times, values, filter_params, max_gap_s: int = _MAX_GAP_S):
    """Smooth each contiguous sampling segment independently.

    Returns an array of the same length as ``values``. Segments are only split
    when the gap exceeds ``max_gap_s``; the regular ~15 min sampling therefore
    stays in a single segment and the filter controls take full effect.
    """
    values = np.asarray(values, dtype=float)
    out = values.copy()
    if not filter_params["enabled"] or len(values) < 3:
        return out

    start = 0
    for i in range(1, len(values)):
        gap = (times.iloc[i] - times.iloc[i - 1]) > pd.Timedelta(seconds=max_gap_s)
        if gap:
            out[start:i] = _smooth_segment(values[start:i], filter_params)
            start = i
    out[start:] = _smooth_segment(values[start:], filter_params)
    return out


def _join_zero_gaps(times, values):
    """Replace interior zero runs with a straight line between the adjacent
    non-zero samples.

    Zeros are treated as missing; the gap is filled by time-based linear
    interpolation so the plotted line runs directly from the last non-zero
    sample to the next one. Zeros at the edges (no non-zero anchor on one side)
    are kept unchanged.
    """
    series = pd.Series(np.asarray(values, dtype=float), index=pd.to_datetime(times))
    masked = series.mask(series == 0)
    interpolated = masked.interpolate(method="time", limit_area="inside")
    return interpolated.where(interpolated.notna(), series).to_numpy()


def _params_for(quantity_params, key):
    """Return the filter parameters for one quantity, filled with defaults."""
    params = dict(DEFAULT_FILTER_PARAMS)
    params.update(quantity_params.get(key, {}) or {})
    return params


def _trim(df: pd.DataFrame, trim_start: int, trim_end: int):
    """Apply the synchronous row trim shared by every quantity.

    Returns ``None`` when the trim would remove the whole report.
    """
    if trim_start + trim_end >= len(df):
        return None
    if trim_end > 0:
        return df.iloc[trim_start : len(df) - trim_end]
    return df.iloc[trim_start:]


def _valid_series(df: pd.DataFrame, key: str, scale: float):
    """Return (times, values) for a column with NaN rows removed and scaled."""
    values = pd.to_numeric(df[key], errors="coerce") * scale
    valid = values.notna()
    return df["Time"][valid].reset_index(drop=True), values[valid].reset_index(drop=True)


def create_plot(datasets, quantities, quantity_params, trim_params, display_options, ntu_thresholds=None):
    """Build the comparison figure.

    ``datasets`` is a list of dicts with ``name``, ``data`` (DataFrame),
    ``enabled`` and ``scale_factor``. ``quantities`` is a list of
    :class:`schema.Quantity`. ``quantity_params`` maps each quantity key to its
    own filter settings (see :data:`filters.DEFAULT_FILTER_PARAMS`).
    ``trim_params`` is the synchronous ``{trim_start, trim_end}`` row trim used
    for every quantity and dataset. ``ntu_thresholds`` optionally provides
    ``(low, high)`` NTU guard thresholds; when given, the ``Turbidity NTU``
    subplot draws a yellow warning band between them and a red alarm band above
    the high threshold.
    """
    trim_start = max(0, int(trim_params.get("trim_start", 0)))
    trim_end = max(0, int(trim_params.get("trim_end", 0)))

    # Trim each enabled dataset once: all quantities share the same time base.
    prepared = []
    for ds in datasets:
        if not ds["enabled"]:
            continue
        trimmed = _trim(ds["data"], trim_start, trim_end)
        if trimmed is None or trimmed.empty:
            continue
        prepared.append((ds, trimmed))

    n = len(quantities)
    height_per_plot = float(display_options.get("plot_height", 3.4)) or 3.4
    fig, axes = plt.subplots(
        n, 1,
        figsize=(16, max(3.6, height_per_plot * n)),
        sharex=False,  # every subplot carries its own date/time axis
        squeeze=False,
    )
    axes = axes[:, 0]

    if prepared:
        x_min = min(df["Time"].min() for _, df in prepared)
        x_max = max(df["Time"].max() for _, df in prepared)

    for qi, q in enumerate(quantities):
        ax = axes[qi]
        plotted = False
        params = _params_for(quantity_params, q.key)

        for idx, (ds, df) in enumerate(prepared):
            times, values = _valid_series(df, q.key, q.scale * ds["scale_factor"])
            if len(values) == 0:
                continue

            # Optional per-quantity cleaning: bridge zero runs with a straight line.
            if params.get("join_zeros"):
                values = pd.Series(_join_zero_gaps(times, values))

            color = _COLORS[idx % len(_COLORS)]
            label_base = ds["name"][:25]
            t_break, v_break = _break_at_gaps(times, values)

            if display_options["show_original"]:
                ax.plot(
                    t_break, v_break,
                    label=f"{label_base} (orig)",
                    linewidth=0.8, alpha=0.35, color=color,
                    marker="o", markersize=2,
                )

            if display_options["show_filtered"] and params["enabled"] and len(values) >= 3:
                try:
                    filtered = _filter_with_gaps(times, values, params)
                    _, f_break = _break_at_gaps(times, filtered)
                    ax.plot(t_break, f_break, label=f"{label_base} (filt)", linewidth=2.0, color=color)
                except Exception:
                    # Filtering is best-effort; original data is already plotted.
                    continue

            plotted = True

        # Date/time axis repeated on every subplot.
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m %H:%M"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.tick_params(axis="x", labelbottom=True, labelrotation=45)
        for label in ax.get_xticklabels():
            label.set_ha("right")
        if prepared:
            ax.set_xlim(x_min, x_max)
        ax.set_xlabel("Date & Time", fontsize=8)

        if plotted:
            ylabel = f"{q.label} [{q.unit}]" if q.unit else q.label
            ax.set_ylabel(ylabel, fontsize=9)
            ax.grid(True, alpha=0.3, linestyle="--")
            if qi == 0:
                ax.legend(fontsize=8, loc="best", ncol=min(3, max(1, len(prepared))))

            # NTU guard-threshold bands: yellow warning zone between the two
            # thresholds, red alarm zone above the high threshold. Bands are
            # clipped to the auto y-range so they never distort the axis.
            if q.key == "Turbidity NTU" and ntu_thresholds is not None:
                low, high = ntu_thresholds
                ymin, ymax = ax.get_ylim()
                yellow_top = min(high, ymax)
                if low < yellow_top:
                    ax.axhspan(max(low, ymin), yellow_top, color="yellow", alpha=0.25, zorder=0)
                red_bottom = max(high, ymin)
                if red_bottom < ymax:
                    ax.axhspan(red_bottom, ymax, color="red", alpha=0.25, zorder=0)
                ax.set_ylim(ymin, ymax)
        else:
            ax.text(0.5, 0.5, "No data", transform=ax.transAxes,
                    ha="center", va="center", fontsize=12, color="gray")
            ax.set_ylabel(q.label, fontsize=9)

    axes[0].set_title("AquaScan multi-quantity comparison", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig
