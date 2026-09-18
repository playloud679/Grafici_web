#!/usr/bin/env python3
"""AquaScan report viewer (Streamlit UI).

Loads one or more AquaScan CSV reports, auto-detects every measurement column
(with its unit of measure), merges companion location files, and renders a
stacked comparison chart. Filter (Savitzky-Golay) and row-trim parameters are
configured **independently per quantity**.

Module documentation: ``docs/modules/app.md``.
"""

from __future__ import annotations

import importlib
import sys
from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st

# Make backend modules importable and reload them on every rerun (long-lived
# process pattern from the Streamlit & SaaS addendum).
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import filters  # noqa: E402
import loader  # noqa: E402
import plotting  # noqa: E402
import schema  # noqa: E402

for _mod in (schema, loader, filters, plotting):
    importlib.reload(_mod)

st.set_page_config(
    page_title="AquaScan Data Viewer",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .main { padding: 0rem 1rem; }
        .stAlert { margin-top: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------------------------------- #
# State helpers
# --------------------------------------------------------------------------- #
def _init_state() -> None:
    st.session_state.setdefault("datasets", [])
    st.session_state.setdefault("quantity_params", {})
    st.session_state.setdefault("params_version", 0)


def _all_quantities(datasets) -> list[schema.Quantity]:
    """Union of quantities across datasets, ordered by category then label."""
    by_key: dict[str, schema.Quantity] = {}
    for ds in datasets:
        for q in schema.detect_quantities(ds["data"]):
            by_key.setdefault(q.key, q)

    cat_rank = {c: i for i, c in enumerate(schema.CATEGORY_ORDER)}
    return sorted(
        by_key.values(),
        key=lambda q: (cat_rank.get(q.category, len(cat_rank)), q.label.lower()),
    )


def _quantity_has_data(q: schema.Quantity, datasets) -> bool:
    for ds in datasets:
        if not ds["enabled"]:
            continue
        if q.key in ds["data"].columns and pd.to_numeric(
            ds["data"][q.key], errors="coerce"
        ).notna().any():
            return True
    return False


def _load_uploads(uploaded_files) -> None:
    current_names = {f.name for f in uploaded_files}
    st.session_state.datasets = [
        d for d in st.session_state.datasets if d["file_names"] <= current_names
    ]
    existing = {d["file_names"] for d in st.session_state.datasets}

    for source in loader.pair_uploaded_files(uploaded_files):
        names = frozenset(
            [source.data_file.name]
            + ([source.location_file.name] if source.location_file else [])
        )
        if names in existing:
            continue

        try:
            df = loader.load_data_csv(source.data_file)
        except Exception as exc:
            st.error(f"❌ {source.data_file.name}: {exc}")
            continue

        location_rows = None
        if source.location_file is not None:
            try:
                loc = loader.load_location_csv(source.location_file)
                df = loader.merge_location(df, loc)
                location_rows = len(loc)
            except Exception as exc:
                st.warning(f"⚠️ Location {source.location_file.name} ignorato: {exc}")

        st.session_state.datasets.append(
            {
                "name": source.name,
                "file_names": names,
                "data": df,
                "enabled": True,
                "scale_factor": 1.0,
                "location_rows": location_rows,
            }
        )
        tail = f", 📍 {location_rows} posizioni" if location_rows else ""
        st.success(f"✅ {source.name} caricato ({len(df)} righe{tail})")


# --------------------------------------------------------------------------- #
# Sidebar
# --------------------------------------------------------------------------- #
def _render_sidebar():
    """Render global defaults + display options. Returns (defaults, options)."""
    with st.sidebar:
        st.header("⚙️ Configurazione")

        st.subheader("📁 Carica File CSV")
        uploaded_files = st.file_uploader(
            "Seleziona uno o più report",
            type=["csv"],
            accept_multiple_files=True,
            help=(
                "Report dati (`*_data.csv`) e, facoltativamente, i corrispondenti "
                "file posizione (`*_location_data.csv`) vengono abbinati automaticamente."
            ),
        )
        if uploaded_files:
            _load_uploads(uploaded_files)

        st.divider()

        st.subheader("🔧 Filtro Savitzky-Golay (predefiniti)")
        st.caption("Valori iniziali; ogni grandezza può poi essere regolata nella tabella dei parametri.")
        defaults = {"enabled": st.checkbox("Abilita Filtro", value=True)}

        col1, col2 = st.columns(2)
        with col1:
            window = st.number_input(
                "Window Length", min_value=5, max_value=101, value=51, step=2,
                help="Dimensione finestra (deve essere dispari)",
            )
            if window % 2 == 0:
                window += 1
            defaults["window_length"] = window
            defaults["poly_order"] = st.number_input(
                "Poly Order", min_value=1, max_value=5, value=2,
                help="Ordine del polinomio",
            )
        with col2:
            defaults["num_passes"] = st.number_input(
                "Num Passaggi", min_value=1, max_value=5, value=3,
                help="Numero di passaggi del filtro",
            )

        if st.button("⬇️ Applica i predefiniti a tutte le grandezze"):
            for key in list(st.session_state.quantity_params.keys()):
                st.session_state.quantity_params[key] = dict(defaults)
            st.session_state.params_version += 1
            st.rerun()

        st.divider()

        st.subheader("✂️ Taglio righe (sincrono)")
        st.caption("Applicato una volta a tutti i report e a tutte le grandezze.")
        trim_col1, trim_col2 = st.columns(2)
        with trim_col1:
            trim_start = st.number_input(
                "Taglia inizio (righe)", min_value=0, value=0, step=1,
                help="Righe da scartare all'inizio, prima del filtraggio",
            )
        with trim_col2:
            trim_end = st.number_input(
                "Taglia fine (righe)", min_value=0, value=0, step=1,
                help="Righe da scartare alla fine, prima del filtraggio",
            )
        trim_params = {"trim_start": int(trim_start), "trim_end": int(trim_end)}

        st.subheader("👁️ Visualizzazione")
        show_original = st.checkbox("Mostra Dati Originali", value=True)
        show_filtered = st.checkbox("Mostra Dati Filtrati", value=True)
        plot_height = st.slider(
            "Altezza per grafico (pollici)",
            min_value=2.0, max_value=8.0, value=3.4, step=0.2,
            help="Aumenta per rendere ogni riquadro più alto e leggibile",
        )

        st.divider()

        if st.button("🗑️ Rimuovi Tutti i File"):
            st.session_state.datasets = []
            st.session_state.quantity_params = {}
            st.session_state.params_version += 1
            st.rerun()

    display_options = {
        "show_original": show_original,
        "show_filtered": show_filtered,
        "plot_height": plot_height,
    }
    return defaults, trim_params, display_options


# --------------------------------------------------------------------------- #
# Main area
# --------------------------------------------------------------------------- #
def _render_datasets() -> None:
    st.header("📊 Report Caricati")
    cols = st.columns(min(3, max(1, len(st.session_state.datasets))))
    for idx, ds in enumerate(st.session_state.datasets):
        with cols[idx % len(cols)]:
            with st.expander(f"📄 {ds['name'][:30]}", expanded=True):
                ds["enabled"] = st.checkbox("Abilitato", value=ds["enabled"], key=f"enabled_{idx}")
                ds["scale_factor"] = st.number_input(
                    "Fattore Scala",
                    min_value=0.001, max_value=1000.0,
                    value=float(ds["scale_factor"]), step=0.1, format="%.3f",
                    key=f"scale_{idx}",
                    help="Moltiplicatore applicato a tutte le grandezze di questo report",
                )
                st.caption(f"📈 {len(ds['data'])} misurazioni")
                st.caption(
                    f"📅 {ds['data']['Time'].min():%d/%m/%Y} - {ds['data']['Time'].max():%d/%m/%Y}"
                )
                if ds["location_rows"]:
                    st.caption(f"📍 {ds['location_rows']} posizioni unite")

                buf = BytesIO()
                ds["data"].to_csv(buf, index=False)
                buf.seek(0)
                st.download_button(
                    f"⬇️ Scarica CSV {ds['name'][:15]}",
                    data=buf,
                    file_name=f"{ds['name']}_merged.csv",
                    mime="text/csv",
                    key=f"dl_{idx}",
                )


def _render_quantity_params(selected, defaults) -> None:
    """Editable table: one row per selected quantity, independent parameters."""
    st.subheader("🎛️ Parametri per grandezza")
    st.caption(
        "Ogni grandezza ha filtro e taglio righe indipendenti. "
        "Modifica i valori nella tabella: il grafico si aggiorna."
    )

    rows = []
    for q in selected:
        params = st.session_state.quantity_params.setdefault(q.key, dict(defaults))
        rows.append(
            {
                "Grandezza": schema.display_label(q),
                "Filtro": bool(params["enabled"]),
                "Window": int(params["window_length"]),
                "Poly": int(params["poly_order"]),
                "Passaggi": int(params["num_passes"]),
            }
        )

    edited = st.data_editor(
        pd.DataFrame(rows).set_index("Grandezza"),
        key=f"quantity_params_editor_{st.session_state.params_version}",
        use_container_width=True,
        column_config={
            "Filtro": st.column_config.CheckboxColumn("Filtro", help="Abilita il filtro per questa grandezza"),
            "Window": st.column_config.NumberColumn("Window", min_value=5, max_value=101, step=2),
            "Poly": st.column_config.NumberColumn("Poly", min_value=1, max_value=5, step=1),
            "Passaggi": st.column_config.NumberColumn("Passaggi", min_value=1, max_value=5, step=1),
        },
    )

    label_to_key = {schema.display_label(q): q.key for q in selected}
    for label, row in edited.iterrows():
        key = label_to_key.get(label)
        if key is None:
            continue
        window = int(row["Window"])
        if window % 2 == 0:
            window += 1
        st.session_state.quantity_params[key] = {
            "enabled": bool(row["Filtro"]),
            "window_length": window,
            "poly_order": int(row["Poly"]),
            "num_passes": int(row["Passaggi"]),
        }


def _render_plot(defaults, trim_params, display_options) -> None:
    st.header("📈 Grafico")

    quantities = _all_quantities(st.session_state.datasets)
    if not quantities:
        st.info("Nessuna grandezza numerica trovata nei report caricati.")
        return

    labels = {
        q.key: schema.display_label(q) + ("" if _quantity_has_data(q, st.session_state.datasets) else " — no data")
        for q in quantities
    }
    default = [q.key for q in quantities if _quantity_has_data(q, st.session_state.datasets)]

    selected_keys = st.multiselect(
        "Grandezze da visualizzare",
        options=list(labels),
        default=default,
        format_func=lambda k: labels[k],
        help="Ogni grandezza viene disegnata in un riquadro dedicato con la propria unità di misura",
    )
    selected = [q for q in quantities if q.key in set(selected_keys)]
    if not selected:
        st.warning("Seleziona almeno una grandezza da visualizzare.")
        return

    _render_quantity_params(selected, defaults)

    try:
        fig = plotting.create_plot(
            st.session_state.datasets, selected, st.session_state.quantity_params, trim_params, display_options
        )
        st.pyplot(fig, use_container_width=True)

        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
        buf.seek(0)
        st.download_button(
            "💾 Scarica Grafico (PNG)",
            data=buf,
            file_name=f"aquascan_plot_{pd.Timestamp.now():%Y%m%d_%H%M%S}.png",
            mime="image/png",
        )
    except Exception as exc:
        st.error(f"Errore nella creazione del grafico: {exc}")


def main() -> None:
    _init_state()
    st.title("💧 AquaScan Data Viewer")
    st.markdown("Visualizzazione e analisi di tutti i dati dei report AquaScan")

    defaults, trim_params, display_options = _render_sidebar()

    if not st.session_state.datasets:
        st.info("👈 Carica uno o più report CSV dalla barra laterale per iniziare")
    else:
        st.divider()
        _render_datasets()
        st.divider()
        _render_plot(defaults, trim_params, display_options)

    st.divider()
    with st.expander("ℹ️ Informazioni e Guida"):
        st.markdown(
            """
            ### Come usare questa applicazione
            1. **Carica report**: carica uno o più file `*_data.csv` (e opzionalmente i relativi `*_location_data.csv`).
            2. **Scegli le grandezze**: seleziona una o più grandezze; ognuna viene disegnata con la propria unità di misura.
            3. **Parametri per grandezza**: nella tabella "Parametri per grandezza" imposta il filtro **indipendentemente** per ciascuna grandezza.
            4. **Taglio righe**: nella barra laterale, applicato in modo **sincrono** a tutte le grandezze.
            5. **Esporta**: scarica il grafico in PNG o i dati uniti in CSV.

            ### Grandezze riconosciute
            Il viewer rileva automaticamente tutte le colonne numeriche dei report
            (temperatura, torbidità, ossigeno disciolto, conducibilità, pH, redox,
            onde, telemetria, posizione, ecc.) e mostra l'unità di misura sull'asse.
            Colonne non catalogate vengono comunque importate come grandezze generiche.
            """
        )


main()
