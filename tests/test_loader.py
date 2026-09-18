"""Tests for CSV/location loading, pairing, and merging."""
import io
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import loader

DATA_CSV = "Time,Turbidity NTU\n2026-01-02 10:00:00,2\n2026-01-01 10:00:00,1\n"
LOC_CSV = (
    "Time,Location\n"
    '2026-01-01 09:00:00,"7.9,43.8"\n'
    '2026-01-02 09:00:00,"7.91,43.81"\n'
)


class _FakeFile:
    def __init__(self, name):
        self.name = name


class TestLoadDataCsv(unittest.TestCase):
    def test_parses_and_sorts_by_time(self):
        df = loader.load_data_csv(io.StringIO(DATA_CSV))
        self.assertEqual(list(df["Turbidity NTU"]), [1, 2])
        self.assertEqual(list(df["Time"]), [df["Time"].iloc[0], df["Time"].iloc[1]])

    def test_missing_time_column_raises(self):
        with self.assertRaises(ValueError):
            loader.load_data_csv(io.StringIO("A,B\n1,2\n"))


class TestLoadLocationCsv(unittest.TestCase):
    def test_parses_longitude_latitude(self):
        loc = loader.load_location_csv(io.StringIO(LOC_CSV))
        self.assertAlmostEqual(loc.iloc[0]["Latitude"], 43.8)
        self.assertAlmostEqual(loc.iloc[0]["Longitude"], 7.9)


class TestMergeLocation(unittest.TestCase):
    def test_backward_fill(self):
        df = loader.load_data_csv(io.StringIO(DATA_CSV))
        loc = loader.load_location_csv(io.StringIO(LOC_CSV))
        merged = loader.merge_location(df, loc)
        self.assertAlmostEqual(merged.iloc[0]["Latitude"], 43.8)
        self.assertAlmostEqual(merged.iloc[1]["Latitude"], 43.81)

    def test_no_location_returns_original(self):
        df = loader.load_data_csv(io.StringIO(DATA_CSV))
        self.assertIs(loader.merge_location(df, None), df)


class TestPairing(unittest.TestCase):
    def test_pairs_data_and_location_by_stem(self):
        files = [
            _FakeFile("aqua_1_data.csv"),
            _FakeFile("aqua_1_location_data.csv"),
            _FakeFile("standalone.csv"),
        ]
        sources = loader.pair_uploaded_files(files)
        self.assertEqual(len(sources), 2)
        paired = [s for s in sources if s.location_file is not None]
        self.assertEqual(len(paired), 1)
        self.assertEqual(paired[0].name, "aqua_1")
        standalone = [s for s in sources if s.location_file is None]
        self.assertEqual(standalone[0].name, "standalone.csv")


if __name__ == "__main__":
    unittest.main()
