"""Tests for plotting helpers (gap handling and segment-aware filtering)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import matplotlib

matplotlib.use("Agg")  # headless

import matplotlib.dates as mdates
import numpy as np
import pandas as pd

import plotting


def _series(n=120, step_s=900, noise=0.2, seed=0):
    """Regular ~15 min series (the real AquaScan sampling interval)."""
    rng = np.random.default_rng(seed)
    times = pd.Series(pd.date_range("2026-01-01", periods=n, freq=f"{step_s}s"))
    values = pd.Series(np.sin(np.linspace(0, 10, n)) + rng.normal(0, noise, n))
    return times, values


def _params(window=21, poly=2, passes=1, enabled=True):
    return {
        "enabled": enabled,
        "window_length": window,
        "poly_order": poly,
        "num_passes": passes,
        "trim_start": 0,
        "trim_end": 0,
    }


class TestFilterHasEffect(unittest.TestCase):
    def test_filter_changes_regular_15min_series(self):
        times, values = _series()
        out = plotting._filter_with_gaps(times, values, _params(window=21))
        self.assertEqual(len(out), len(values))
        # The filter must actually change the data (regression: threshold used
        # to split every ~15 min point and leave the data untouched).
        self.assertFalse(np.allclose(out, values.to_numpy()))

    def test_window_parameter_changes_result(self):
        times, values = _series()
        out11 = plotting._filter_with_gaps(times, values, _params(window=11))
        out51 = plotting._filter_with_gaps(times, values, _params(window=51))
        self.assertFalse(np.allclose(out11, out51))

    def test_disabled_filter_is_identity(self):
        times, values = _series()
        out = plotting._filter_with_gaps(times, values, _params(enabled=False))
        np.testing.assert_array_equal(out, values.to_numpy())


class TestClamp(unittest.TestCase):
    def test_no_values_outside_observed_range(self):
        times, values = _series(noise=0.05)
        # Inject a sharp step so Savitzky-Golay would overshoot.
        values = values.copy()
        values.iloc[30:80] = values.iloc[30:80] + 5
        out = plotting._filter_with_gaps(times, values, _params(window=51, passes=3))
        self.assertGreaterEqual(out.min(), values.min() - 1e-9)
        self.assertLessEqual(out.max(), values.max() + 1e-9)


class TestPerQuantityParams(unittest.TestCase):
    def _df(self):
        return pd.DataFrame(
            {
                "Time": pd.date_range("2026-01-01", periods=100, freq="15min"),
                "Turbidity NTU": np.sin(np.linspace(0, 10, 100)),
                "DO2": np.cos(np.linspace(0, 10, 100)),
            }
        )

    def test_params_for_fills_defaults(self):
        p = plotting._params_for({"DO2": {"window_length": 11}}, "DO2")
        self.assertEqual(p["window_length"], 11)
        self.assertEqual(p["poly_order"], plotting.DEFAULT_FILTER_PARAMS["poly_order"])

    def test_create_plot_uses_per_quantity_params(self):
        from schema import detect_quantities

        df = self._df()
        qs = [q for q in detect_quantities(df) if q.key in ("Turbidity NTU", "DO2")]
        quantity_params = {
            "Turbidity NTU": _params(window=11),
            "DO2": _params(window=51, enabled=False),
        }
        fig = plotting.create_plot(
            [{"name": "a", "data": df, "enabled": True, "scale_factor": 1.0}],
            qs,
            quantity_params,
            {"trim_start": 0, "trim_end": 0},
            {"show_original": True, "show_filtered": True, "plot_height": 3.0},
        )
        self.assertEqual(len(fig.axes), 2)

    def test_time_axis_visible_on_every_subplot(self):
        from schema import detect_quantities

        df = self._df()
        qs = [q for q in detect_quantities(df) if q.key in ("Turbidity NTU", "DO2")]
        fig = plotting.create_plot(
            [{"name": "a", "data": df, "enabled": True, "scale_factor": 1.0}],
            qs,
            {},
            {"trim_start": 0, "trim_end": 0},
            {"show_original": True, "show_filtered": True, "plot_height": 3.0},
        )
        fig.canvas.draw()
        for ax in fig.axes:
            visible = [t.get_text() for t in ax.get_xticklabels() if t.get_visible()]
            self.assertTrue(any(t for t in visible), "subplot without time labels")
            self.assertIn("Date", ax.get_xlabel())


class TestSynchronousTrim(unittest.TestCase):
    def test_trim_removes_rows_at_both_ends(self):
        df = pd.DataFrame({"Time": pd.date_range("2026-01-01", periods=20, freq="15min"), "x": range(20)})
        out = plotting._trim(df, 3, 4)
        self.assertEqual(list(out["x"]), list(range(3, 16)))

    def test_trim_too_large_returns_none(self):
        df = pd.DataFrame({"Time": pd.date_range("2026-01-01", periods=5, freq="15min"), "x": range(5)})
        self.assertIsNone(plotting._trim(df, 3, 3))

    def test_trim_is_shared_by_all_quantities(self):
        from schema import detect_quantities

        df = pd.DataFrame(
            {
                "Time": pd.date_range("2026-01-01", periods=50, freq="15min"),
                "Turbidity NTU": np.arange(50.0),
                "DO2": np.arange(50.0),
            }
        )
        qs = [q for q in detect_quantities(df) if q.key in ("Turbidity NTU", "DO2")]
        fig = plotting.create_plot(
            [{"name": "a", "data": df, "enabled": True, "scale_factor": 1.0}],
            qs,
            {},
            {"trim_start": 10, "trim_end": 5},
            {"show_original": True, "show_filtered": False, "plot_height": 3.0},
        )
        for ax in fig.axes:
            self.assertAlmostEqual(ax.get_xlim()[0], mdates.date2num(df["Time"].iloc[10]), places=3)
            self.assertAlmostEqual(ax.get_xlim()[1], mdates.date2num(df["Time"].iloc[44]), places=3)


class TestJoinZeros(unittest.TestCase):
    def _times(self, n):
        return pd.date_range("2026-01-01", periods=n, freq="15min")

    def test_interior_zero_run_becomes_straight_line(self):
        times = self._times(5)
        values = pd.Series([2.0, 0.0, 0.0, 0.0, 4.0])
        out = plotting._join_zero_gaps(times, values)
        np.testing.assert_allclose(out, [2.0, 2.5, 3.0, 3.5, 4.0])

    def test_edge_zeros_are_kept(self):
        times = self._times(5)
        values = pd.Series([0.0, 2.0, 0.0, 4.0, 0.0])
        out = plotting._join_zero_gaps(times, values)
        self.assertEqual(out[0], 0.0)
        self.assertEqual(out[-1], 0.0)
        self.assertAlmostEqual(out[2], 3.0)

    def test_all_zeros_unchanged(self):
        times = self._times(4)
        values = pd.Series([0.0, 0.0, 0.0, 0.0])
        out = plotting._join_zero_gaps(times, values)
        np.testing.assert_array_equal(out, values.to_numpy())

    def test_create_plot_with_join_zeros(self):
        from schema import detect_quantities

        df = pd.DataFrame(
            {
                "Time": self._times(40),
                "Turbidity NTU": [0.0 if 10 <= i <= 20 else 5.0 for i in range(40)],
            }
        )
        qs = [q for q in detect_quantities(df) if q.key == "Turbidity NTU"]
        fig = plotting.create_plot(
            [{"name": "a", "data": df, "enabled": True, "scale_factor": 1.0}],
            qs,
            {"Turbidity NTU": {"enabled": False, "join_zeros": True}},
            {"trim_start": 0, "trim_end": 0},
            {"show_original": True, "show_filtered": False, "plot_height": 3.0},
        )
        self.assertEqual(len(fig.axes), 1)


class TestGapHandling(unittest.TestCase):
    def test_regular_sampling_is_not_broken(self):
        times, values = _series()
        _, v_break = plotting._break_at_gaps(times, values)
        self.assertEqual(len(v_break), len(values))
        self.assertFalse(np.isnan(v_break).any())

    def test_long_gap_is_broken(self):
        times = pd.Series(pd.to_datetime(
            ["2026-01-01 00:00", "2026-01-01 00:15", "2026-01-01 04:00", "2026-01-01 04:15"]
        ))
        values = pd.Series([1.0, 2.0, 3.0, 4.0])
        _, v_break = plotting._break_at_gaps(times, values)
        self.assertEqual(len(v_break), len(values) + 1)
        self.assertTrue(np.isnan(v_break).any())


class TestNtuThresholdBands(unittest.TestCase):
    def _df(self):
        from schema import detect_quantities

        df = pd.DataFrame(
            {
                "Time": pd.date_range("2026-01-01", periods=50, freq="15min"),
                "Turbidity NTU": np.linspace(0, 8, 50),
            }
        )
        qs = [q for q in detect_quantities(df) if q.key == "Turbidity NTU"]
        return df, qs

    def test_draws_yellow_and_red_bands(self):
        df, qs = self._df()
        fig = plotting.create_plot(
            [{"name": "a", "data": df, "enabled": True, "scale_factor": 1.0}],
            qs,
            {},
            {"trim_start": 0, "trim_end": 0},
            {"show_original": True, "show_filtered": False, "plot_height": 3.0},
            ntu_thresholds=(4.0, 7.0),
        )
        ax = fig.axes[0]
        self.assertEqual(len(ax.patches), 2)
        yellow = ax.patches[0].get_facecolor()
        red = ax.patches[1].get_facecolor()
        self.assertAlmostEqual(yellow[0], 1.0)
        self.assertAlmostEqual(yellow[1], 1.0)
        self.assertAlmostEqual(yellow[2], 0.0)
        self.assertAlmostEqual(red[0], 1.0)
        self.assertAlmostEqual(red[1], 0.0)
        self.assertAlmostEqual(red[2], 0.0)

    def test_no_bands_without_thresholds(self):
        df, qs = self._df()
        fig = plotting.create_plot(
            [{"name": "a", "data": df, "enabled": True, "scale_factor": 1.0}],
            qs,
            {},
            {"trim_start": 0, "trim_end": 0},
            {"show_original": True, "show_filtered": False, "plot_height": 3.0},
        )
        self.assertEqual(len(fig.axes[0].patches), 0)


if __name__ == "__main__":
    unittest.main()
