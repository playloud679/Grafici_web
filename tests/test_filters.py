"""Tests for the Savitzky-Golay smoothing helper."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np

import filters


class TestApplyFilter(unittest.TestCase):
    def test_short_series_unchanged(self):
        data = np.array([1.0, 2.0])
        out = filters.apply_filter(data, 5, 2, 1)
        np.testing.assert_array_equal(out, data)

    def test_output_preserves_length_and_is_finite(self):
        rng = np.random.default_rng(0)
        data = np.sin(np.linspace(0, 10, 200)) + rng.normal(0, 0.05, 200)
        out = filters.apply_filter(data, 21, 2, 2)
        self.assertEqual(len(out), len(data))
        self.assertTrue(np.all(np.isfinite(out)))

    def test_smoothing_reduces_variance(self):
        rng = np.random.default_rng(1)
        data = np.sin(np.linspace(0, 20, 300)) + rng.normal(0, 0.3, 300)
        out = filters.apply_filter(data, 31, 2, 1)
        self.assertLess(np.std(out), np.std(data))


if __name__ == "__main__":
    unittest.main()
