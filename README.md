# AquaScan Data Viewer

[![Version](https://img.shields.io/badge/version-0.5.0-blue.svg)](VERSION)
[![Standard](https://img.shields.io/badge/standard-GOLDEN__STD-gold.svg)](GOLDEN_STD.md)
[![Addendum](https://img.shields.io/badge/addendum-STREAMLIT__SAAS-lightgrey.svg)](addenda/STREAMLIT_SAAS.md)

Streamlit web viewer for **AquaScan** device reports. It ingests every
measurement present in a report — water quality, waves, telemetry and
position — and plots selected quantities with their unit of measure.

## Features

- 📥 Upload one or more `*_data.csv` reports (and optional
  `*_location_data.csv` companions, paired automatically by stem).
- 🔎 Auto-detects all numeric columns; known AquaScan columns are mapped to a
  human label + unit catalog, unknown ones are still ingested.
- 📈 One stacked subplot per selected quantity, sharing the time axis, with
  Savitzky-Golay smoothing and gap-aware lines.
- 🚨 NTU guard thresholds shown as yellow/red bands on the turbidity subplot.
- 🎛️ **Independent filter/trim parameters for each quantity** (editable table),
  plus a per-quantity **"Unisci zeri"** option that bridges zero runs with a
  straight line between the adjacent non-zero samples.
- 📍 Merges position data (last known location carried backward).
- 💾 Exports the merged CSV and the chart as PNG.
- 📥 Downloads a single XLS with all raw rows trimmed of the configured
  initial/final records, a progressive sample-number column (`Campione`),
  user-selectable data columns (`Campione` and `Time` are always included),
  two adjustable NTU guard-threshold exceedance columns, and yellow/red row
  highlighting for threshold breaches.

## Project conventions

- **Lifecycle stage:** Alpha (`0.x.y`) — actively evolving, experimental UI.
- **Integration target:** `main` (never develop directly on it; use a
  dedicated branch).
- **Engineering standard:** [`GOLDEN_STD.md`](GOLDEN_STD.md) plus the
  [`addenda/STREAMLIT_SAAS.md`](addenda/STREAMLIT_SAAS.md) addendum.
- **Module map:** see [`docs/INDEX.md`](docs/INDEX.md).

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Test

```bash
python -m py_compile app.py src/*.py
python -m unittest discover -s tests -v
```

## Deploy

See [`DEPLOY.md`](DEPLOY.md).
