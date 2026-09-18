"""Savitzky-Golay smoothing helpers.

Module documentation: ``docs/modules/filters.md``.
"""

from __future__ import annotations

import numpy as np
from scipy.signal import savgol_filter

# Defaults used when a quantity has no explicit filter parameters yet.
DEFAULT_FILTER_PARAMS = {
    "enabled": True,
    "window_length": 51,
    "poly_order": 2,
    "num_passes": 3,
}


def apply_filter(data, window_length, poly_order, num_passes):
    """Apply ``num_passes`` of Savitzky-Golay smoothing.

    The requested window is used on the first pass; later passes shrink to a
    smaller window (31 then 15) so repeated smoothing does not over-flatten the
    signal. The window is forced odd and capped to the available length.
    Short series (<= window) are returned unchanged.
    """
    data = np.asarray(data, dtype=float)
    window_length = int(window_length)
    poly_order = int(poly_order)
    num_passes = int(num_passes)

    if len(data) <= window_length or window_length < 3:
        return data

    filtered = data.copy()
    for i in range(num_passes):
        current_window = window_length
        if i == 1 and num_passes >= 2:
            current_window = min(31, current_window)
        elif i == 2 and num_passes >= 3:
            current_window = min(15, current_window)

        current_window = min(current_window, len(filtered) - 1)
        if current_window % 2 == 0:
            current_window -= 1
        if current_window < 3:
            break

        filtered = savgol_filter(filtered, current_window, min(poly_order, current_window - 1))

    return filtered
