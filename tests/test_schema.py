"""Tests for the quantity catalog and column detection."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pandas as pd

import schema


class TestQuantityCatalog(unittest.TestCase):
    def test_turbidity_unit(self):
        self.assertEqual(schema.QUANTITY_SCHEMA["Turbidity NTU"].unit, "NTU")

    def test_vbatt_scale_is_millivolts_to_volts(self):
        self.assertEqual(schema.QUANTITY_SCHEMA["Vbatt"].scale, 0.001)

    def test_wave_height_unit(self):
        self.assertEqual(schema.QUANTITY_SCHEMA["Altezza Onda"].unit, "m")

    def test_display_label_with_unit(self):
        q = schema.QUANTITY_SCHEMA["Turbidity NTU"]
        self.assertEqual(schema.display_label(q), "Turbidity (NTU)")

    def test_display_label_without_unit(self):
        q = schema.Quantity("custom", "Custom", "", 1.0, "Other")
        self.assertEqual(schema.display_label(q), "Custom")


class TestDetectQuantities(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame(
            {
                "Time": pd.to_datetime(["2026-01-01 00:00:00"]),
                "Turbidity NTU": [1.5],
                "Vbatt": [4237],
                "custom_metric": [10],
                "note": ["abc"],
            }
        )

    def test_detects_known_columns(self):
        keys = {q.key for q in schema.detect_quantities(self.df)}
        self.assertIn("Turbidity NTU", keys)
        self.assertIn("Vbatt", keys)

    def test_detects_generic_numeric_column(self):
        generic = [q for q in schema.detect_quantities(self.df) if q.key == "custom_metric"]
        self.assertEqual(len(generic), 1)
        self.assertEqual(generic[0].category, "Other")

    def test_excludes_non_numeric_and_time(self):
        keys = {q.key for q in schema.detect_quantities(self.df)}
        self.assertNotIn("note", keys)
        self.assertNotIn("Time", keys)


if __name__ == "__main__":
    unittest.main()
