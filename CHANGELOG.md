# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-09-18

### Added
- **Per-quantity filter parameters**: editable table where each quantity has its
  own Savitzky-Golay filter (enabled/window/poly/passes), independent of the
  others.
- **Synchronous row trim**: `trim_start`/`trim_end` in the sidebar apply once to
  the whole report, so all quantities share the same time base.
- **Repeated time axis**: every subplot now shows its own date/time ticks.
- Sidebar filter values act as global defaults with an
  "Applica i predefiniti a tutte le grandezze" action.

## [0.2.1] - 2026-09-18

### Fixed
- **Charts**: larger figure (16" wide) and full container width so stacked
  subplots are readable; added a per-plot height slider (sidebar).
- **Data consistency**: Savitzky-Golay overshoot is clamped to each segment's
  observed range, so physically impossible values (e.g. negative oxygen or
  turbidity) no longer appear.
- **Filter controls**: gap threshold raised from 15 min to 2 h. AquaScan samples
  every ~15 min, so the previous threshold split almost every point and the
  filter had no visible effect; filter parameters now work as expected.

## [0.2.0] - 2026-09-18

### Added
- **Ingestion**: viewer now auto-detects and plots every quantity in AquaScan
  reports (temperature, turbidity, dissolved oxygen, conductivity, pH, redox,
  waves, telemetry, position, etc.), showing units of measure on each axis.
- **Location data**: companion `*_location_data.csv` files are paired by stem
  and merged onto measurement rows (last known position carried backward).
- **Multi-quantity chart**: one stacked subplot per selected quantity.
- **Exports**: per-report merged CSV download and PNG chart download.
- **Quantity catalog** (`src/schema.py`) with units and default scales for all
  known AquaScan columns; unknown numeric columns are still ingested.

### Changed
- **Refactor**: split the single-file app into modules `src/schema.py`,
  `src/loader.py`, `src/filters.py`, `src/plotting.py`, with `app.py` as the
  Streamlit entry point.
- **Entry point**: renamed `turbidity_app_web.py` → `app.py`; `Procfile` and
  `DEPLOY.md` updated accordingly.

### Docs
- Added `docs/INDEX.md` and `docs/modules/*.md`, `AGENTS.md`, this changelog,
  `VERSION`, and `GOLDEN_STD.md` + `addenda/STREAMLIT_SAAS.md`.
- Declared Alpha lifecycle stage and `main` integration target.

### Validation
- `python -m py_compile app.py src/*.py`
- `python -m unittest discover -s tests -v`

## [0.1.0] - 2025-11-17

### Added
- Initial turbidity-only Streamlit viewer with Savitzky-Golay filtering.
