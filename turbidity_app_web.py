#!/usr/bin/env python3
"""
Applicazione Web per visualizzazione e analisi dati di torbidità
Si apre automaticamente nel browser - compatibile con tutti i sistemi
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.signal import savgol_filter
import numpy as np
from io import BytesIO

# Configurazione pagina
st.set_page_config(
    page_title="Turbidity Data Viewer",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Stile CSS personalizzato
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


def apply_filter(data, window_length, poly_order, num_passes):
    """Applica il filtro Savitzky-Golay con parametri specificati"""
    if len(data) <= window_length:
        return data

    filtered = data.copy()

    for i in range(num_passes):
        if i == 0:
            current_window = window_length
        elif i == 1 and num_passes >= 2:
            current_window = min(31, window_length)
        elif i == 2 and num_passes >= 3:
            current_window = min(15, window_length)
        else:
            current_window = window_length

        current_window = min(current_window, len(filtered) - 1)
        if current_window % 2 == 0:
            current_window -= 1
        if current_window < 3:
            break

        filtered = savgol_filter(filtered, current_window, min(poly_order, current_window - 1))

    return filtered


def load_csv_file(uploaded_file):
    """Carica e valida un file CSV"""
    try:
        df = pd.read_csv(uploaded_file)

        if 'Time' not in df.columns or 'Turbidity NTU' not in df.columns:
            return None, "Il file non contiene le colonne 'Time' e 'Turbidity NTU'"

        df['Time'] = pd.to_datetime(df['Time'])
        df = df.sort_values('Time')

        return df, None
    except Exception as e:
        return None, f"Errore nel caricamento: {str(e)}"


def create_plot(datasets_config, filter_params, display_options):
    """Crea il grafico con i dataset configurati"""
    fig, ax = plt.subplots(figsize=(14, 7))

    has_data = False
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'cyan', 'magenta']

    for idx, config in enumerate(datasets_config):
        if not config['enabled']:
            continue

        has_data = True
        df = config['data'].copy()
        scale_factor = config['scale_factor']
        color = colors[idx % len(colors)]
        label_base = config['name'][:25]

        # Taglio iniziale/finale prima del filtraggio
        start_cut = max(0, int(filter_params['trim_start']))
        end_cut = max(0, int(filter_params['trim_end']))
        if start_cut + end_cut >= len(df):
            st.warning(f"{label_base}: taglio troppo esteso, dataset ignorato")
            continue
        if end_cut > 0:
            df = df.iloc[start_cut: len(df) - end_cut]
        else:
            df = df.iloc[start_cut:]

        # Applica fattore di scala
        df['Turbidity Scaled'] = df['Turbidity NTU'] * scale_factor

        # Applica filtro se abilitato
        if filter_params['enabled']:
            try:
                filtered_values = apply_filter(
                    df['Turbidity Scaled'].values,
                    filter_params['window_length'],
                    filter_params['poly_order'],
                    filter_params['num_passes']
                )
                df['Turbidity Filtered'] = filtered_values

            except Exception as e:
                st.error(f"Errore nel filtraggio di {label_base}: {str(e)}")
                continue

        # Plotta dati originali
        if display_options['show_original']:
            ax.plot(df['Time'], df['Turbidity Scaled'],
                   label=f'{label_base} (Orig)',
                   linewidth=0.8, alpha=0.3, color=color,
                   marker='o', markersize=2)

        # Plotta dati filtrati
        if display_options['show_filtered'] and filter_params['enabled']:
            ax.plot(df['Time'], df['Turbidity Filtered'],
                   label=f'{label_base} (Filt)',
                   linewidth=2.5, color=color)

    if not has_data:
        ax.text(0.5, 0.5, 'Nessun dataset abilitato o caricato',
               transform=ax.transAxes, ha='center', va='center',
               fontsize=16, color='gray')
    else:
        ax.set_xlabel('Data e Ora', fontsize=12)
        ax.set_ylabel('Torbidità (NTU)', fontsize=12)
        ax.set_title('Confronto Dati Torbidità', fontsize=14, fontweight='bold')
        ax.legend(fontsize=9, loc='best')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        fig.autofmt_xdate(rotation=45, ha='right')

    plt.tight_layout()
    return fig


# Inizializza session state
if 'datasets' not in st.session_state:
    st.session_state.datasets = []

# Header
st.title("💧 Turbidity Data Viewer")
st.markdown("Applicazione per visualizzazione e analisi dati di torbidità da sensori")

# Sidebar per controlli
with st.sidebar:
    st.header("⚙️ Configurazione")

    # Upload files
    st.subheader("📁 Carica File CSV")
    uploaded_files = st.file_uploader(
        "Seleziona uno o più file CSV",
        type=['csv'],
        accept_multiple_files=True,
        help="I file devono contenere colonne 'Time' e 'Turbidity NTU'"
    )

    # Processa file caricati
    if uploaded_files:
        # Rimuovi dataset precedenti se ci sono nuovi upload
        current_names = [f.name for f in uploaded_files]
        st.session_state.datasets = [d for d in st.session_state.datasets
                                      if d['name'] in current_names]

        # Aggiungi nuovi dataset
        existing_names = [d['name'] for d in st.session_state.datasets]
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in existing_names:
                df, error = load_csv_file(uploaded_file)
                if error:
                    st.error(f"❌ {uploaded_file.name}: {error}")
                else:
                    # Determina scala default
                    default_scale = 0.1 if "Boa_2_P" in uploaded_file.name or "boa_2_p" in uploaded_file.name.lower() else 1.0

                    st.session_state.datasets.append({
                        'name': uploaded_file.name,
                        'data': df,
                        'enabled': True,
                        'scale_factor': default_scale
                    })
                    st.success(f"✅ {uploaded_file.name} caricato ({len(df)} righe)")

    st.divider()

    # Parametri Filtro
    st.subheader("🔧 Filtro Savitzky-Golay")
    filter_enabled = st.checkbox("Abilita Filtro", value=True)

    col1, col2 = st.columns(2)
    with col1:
        window_length = st.number_input(
            "Window Length",
            min_value=5,
            max_value=101,
            value=51,
            step=2,
            help="Dimensione finestra (deve essere dispari)"
        )
        if window_length % 2 == 0:
            window_length += 1

        poly_order = st.number_input(
            "Poly Order",
            min_value=1,
            max_value=5,
            value=2,
            help="Ordine del polinomio"
        )

    with col2:
        num_passes = st.number_input(
            "Num Passaggi",
            min_value=1,
            max_value=5,
            value=3,
            help="Numero di passaggi del filtro"
        )

        trim_start = st.number_input(
            "Taglia inizio (righe)",
            min_value=0,
            value=0,
            step=1,
            help="Numero di punti da scartare all'inizio prima del filtraggio"
        )

        trim_end = st.number_input(
            "Taglia fine (righe)",
            min_value=0,
            value=0,
            step=1,
            help="Numero di punti da scartare alla fine prima del filtraggio"
        )

    st.divider()

    # Opzioni visualizzazione
    st.subheader("👁️ Visualizzazione")
    show_original = st.checkbox("Mostra Dati Originali", value=True)
    show_filtered = st.checkbox("Mostra Dati Filtrati", value=True)

    st.divider()

    # Pulsante reset
    if st.button("🗑️ Rimuovi Tutti i File"):
        st.session_state.datasets = []
        st.rerun()

# Area principale
if not st.session_state.datasets:
    st.info("👈 Carica uno o più file CSV dalla barra laterale per iniziare")
else:
    # Configurazione dataset
    st.header("📊 Dataset Caricati")

    cols = st.columns(min(3, len(st.session_state.datasets)))

    for idx, dataset in enumerate(st.session_state.datasets):
        with cols[idx % 3]:
            with st.expander(f"📄 {dataset['name'][:30]}", expanded=True):
                dataset['enabled'] = st.checkbox(
                    "Abilitato",
                    value=dataset['enabled'],
                    key=f"enabled_{idx}"
                )

                dataset['scale_factor'] = st.number_input(
                    "Fattore Scala",
                    min_value=0.001,
                    max_value=100.0,
                    value=float(dataset['scale_factor']),
                    step=0.1,
                    format="%.3f",
                    key=f"scale_{idx}",
                    help="Moltiplicatore per i valori di torbidità"
                )

                st.caption(f"📈 {len(dataset['data'])} misurazioni")
                st.caption(f"📅 {dataset['data']['Time'].min().strftime('%d/%m/%Y')} - {dataset['data']['Time'].max().strftime('%d/%m/%Y')}")

    st.divider()

    # Crea e mostra grafico
    st.header("📈 Grafico")

    filter_params = {
        'enabled': filter_enabled,
        'window_length': window_length,
        'poly_order': poly_order,
        'num_passes': num_passes,
        'trim_start': trim_start,
        'trim_end': trim_end
    }

    display_options = {
        'show_original': show_original,
        'show_filtered': show_filtered
    }

    try:
        fig = create_plot(st.session_state.datasets, filter_params, display_options)
        st.pyplot(fig)

        # Pulsante download
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0)

        st.download_button(
            label="💾 Scarica Grafico (PNG)",
            data=buf,
            file_name=f"turbidity_plot_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.png",
            mime="image/png"
        )

    except Exception as e:
        st.error(f"Errore nella creazione del grafico: {str(e)}")

# Footer
st.divider()
with st.expander("ℹ️ Informazioni e Guida"):
    st.markdown("""
    ### Come usare questa applicazione

    1. **Carica File CSV**: Usa il pulsante nella barra laterale per caricare uno o più file
    2. **Configura Dataset**: Abilita/disabilita dataset e modifica i fattori di scala
    3. **Imposta Filtri**: Configura i parametri del filtro Savitzky-Golay
    4. **Visualizza**: Il grafico si aggiorna automaticamente
    5. **Scarica**: Usa il pulsante per salvare il grafico come immagine

    ### Formato CSV Richiesto
    ```
    Time,Turbidity NTU
    2025-10-23 10:00:00,6.45
    2025-10-23 09:00:00,6.38
    ```

    ### Parametri Filtro
    - **Window Length**: Dimensione finestra (valori più alti = filtraggio più aggressivo)
    - **Poly Order**: Ordine polinomio (valori più bassi = più smoothing)
    - **Num Passaggi**: Numero di applicazioni del filtro (3 = molto aggressivo)
    - **Taglia inizio/fine**: Scarta punti prima e dopo il filtraggio
    """)
