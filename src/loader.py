"""Loading and pairing of AquaScan CSV reports.

An AquaScan export is a pair of files sharing a stem:

* ``<stem>_data.csv`` — timestamped measurement rows (one column per quantity).
* ``<stem>_location_data.csv`` — timestamped ``Location`` strings ``lon,lat``.

This module parses both, pairs them by stem, and merges positions onto the
measurement rows (last known location carried backward in time).

Module documentation: ``docs/modules/loader.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd

_DATA_SUFFIX = "_data.csv"
_LOCATION_SUFFIX = "_location_data.csv"


@dataclass
class DatasetSource:
    """A paired report ready to be loaded into a dataset."""

    name: str
    data_file: object
    location_file: Optional[object] = None


def classify_file(name: str) -> tuple[str, Optional[str]]:
    """Return ``(kind, base)`` for a filename.

    ``kind`` is ``"location"`` or ``"data"``; ``base`` is the shared stem used
    to pair companion files, or ``None`` for standalone files.
    """
    if name.endswith(_LOCATION_SUFFIX):
        return ("location", name[: -len(_LOCATION_SUFFIX)])
    if name.endswith(_DATA_SUFFIX):
        return ("data", name[: -len(_DATA_SUFFIX)])
    return ("data", None)


def pair_uploaded_files(uploaded_files) -> list[DatasetSource]:
    """Group uploaded files into ``DatasetSource`` objects.

    Files named ``<stem>_data.csv`` and ``<stem>_location_data.csv`` are paired
    by stem. Any other CSV is treated as a standalone dataset.
    """
    data_by_base: dict[str, object] = {}
    location_by_base: dict[str, object] = {}
    standalone: list[object] = []

    for f in uploaded_files:
        kind, base = classify_file(f.name)
        if kind == "location":
            location_by_base[base] = f
        elif base is None:
            standalone.append(f)
        else:
            data_by_base[base] = f

    sources = [
        DatasetSource(
            name=base,
            data_file=data_by_base[base],
            location_file=location_by_base.get(base),
        )
        for base in data_by_base
    ]
    sources.extend(DatasetSource(name=f.name, data_file=f, location_file=None) for f in standalone)
    return sources


def load_data_csv(file_obj) -> pd.DataFrame:
    """Parse a measurement CSV and return it sorted by ``Time``.

    Raises ``ValueError`` when the required ``Time`` column is missing.
    """
    df = pd.read_csv(file_obj)
    if "Time" not in df.columns:
        raise ValueError("missing 'Time' column")
    df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
    df = df.sort_values("Time").reset_index(drop=True)
    return df


def load_location_csv(file_obj) -> pd.DataFrame:
    """Parse a location CSV into ``Time``, ``Latitude``, ``Longitude`` columns.

    The ``Location`` field is expected as ``"longitude,latitude"``.
    Rows with unparsable coordinates are dropped.
    """
    loc = pd.read_csv(file_obj)
    if "Time" not in loc.columns or "Location" not in loc.columns:
        raise ValueError("location CSV requires 'Time' and 'Location' columns")
    loc["Time"] = pd.to_datetime(loc["Time"], errors="coerce")
    coords = loc["Location"].astype(str).str.split(",", expand=True)
    loc["Longitude"] = pd.to_numeric(coords[0], errors="coerce")
    loc["Latitude"] = pd.to_numeric(coords[1], errors="coerce")
    loc = (
        loc[["Time", "Latitude", "Longitude"]]
        .dropna(subset=["Latitude", "Longitude"])
        .sort_values("Time")
        .drop_duplicates("Time")
        .reset_index(drop=True)
    )
    return loc


def merge_location(df: pd.DataFrame, loc: Optional[pd.DataFrame]) -> pd.DataFrame:
    """Merge position columns onto measurement rows.

    Each measurement row receives the last known location at or before its
    timestamp (``merge_asof`` backward). Existing non-empty ``Latitude`` /
    ``Longitude`` columns in ``df`` are preserved and take precedence.
    """
    if loc is None or loc.empty:
        return df

    df = df.copy()
    for col in ("Latitude", "Longitude"):
        if col in df.columns and df[col].notna().any():
            continue  # data file already carries its own positions
        if col in df.columns:
            df = df.drop(columns=[col])

    return pd.merge_asof(df, loc, on="Time", direction="backward")
