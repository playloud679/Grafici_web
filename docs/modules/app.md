# Module: app.py

Streamlit entry point and user interface for the AquaScan report viewer.

## Responsibility

- Renders the sidebar (upload, filter parameters, display options including
  per-plot height).
- Loads and pairs uploaded reports into in-session datasets.
- Lets the user enable/disable datasets, apply a per-dataset scale factor,
  and select which quantities to plot.
- Renders an editable **per-quantity filter table** (enabled/window/poly/passes
  and "Unisci zeri"), so each quantity is filtered and cleaned independently.
- Provides a **synchronous row trim** in the sidebar, shared by every quantity
  and dataset (single time base).
- Calls `src/plotting.py` to build the figure and offers PNG/CSV downloads.

## Public interface

- `main()` — top-level Streamlit render; invoked at module import.

## Dependencies

- `src/schema` (quantity detection), `src/loader` (report loading),
  `src/filters` and `src/plotting` (chart).
- `streamlit`, `pandas`.

## Behavior notes

- Backend modules are reloaded on every rerun (`importlib.reload`) because
  Streamlit runs in a long-lived process (Streamlit & SaaS addendum §2).
- `st.session_state["datasets"]` holds persistent dataset state;
  `st.session_state["quantity_params"]` holds per-quantity filter/trim settings;
  widget keys (`enabled_*`, `scale_*`, `dl_*`, `quantity_params_editor_*`) keep
  interactive/action keys separate from these collections to avoid
  `StreamlitAPIException` key collisions.
- Sidebar values are **defaults**; the per-quantity editor is authoritative.
  The sidebar "Applica i predefiniti a tutte le grandezze" button overwrites all
  per-quantity rows and bumps `params_version` to reset the editor state.
- The row trim (`trim_start`/`trim_end`) is **global**: it is applied once to
  the report rows, so all quantities share the same time base.
- A dataset is kept across reruns only while all of its source file names are
  still present in the uploader.

## Edge cases

- Quantities with no data across all datasets are listed but not selected by
  default and render an empty "No data" subplot if chosen.
- A missing companion location file is tolerated: the dataset loads without
  merged positions.

## Validation

```bash
python -m py_compile app.py src/*.py
python -m unittest discover -s tests -v
python -c 'from streamlit.testing.v1 import AppTest; at = AppTest.from_file("app.py", default_timeout=30); at.run(); assert not at.exception, at.exception'
```
