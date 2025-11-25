# Deploy rapido (Streamlit / Render)

## Prerequisiti
- Repo su GitHub con questi file in root: `turbidity_app_web.py`, `requirements.txt`, `Procfile`, CSV di esempio (leggeri) opzionali.
- Python 3.9+ consigliato. Le librerie sono fissate in `requirements.txt` per coerenza con lo sviluppo locale.

## Streamlit Community Cloud (più semplice)
1. Push su GitHub.
2. Vai su https://streamlit.io e crea una nuova app: seleziona repo/branch/file `turbidity_app_web.py`.
3. Nessuna configurazione porte necessaria; i file CSV li carichi dal browser.
4. Aggiorna `requirements.txt` se aggiungi librerie, poi redeploy automatico.

## Render / Railway / Heroku-like
1. Push su GitHub.
2. Crea un nuovo servizio web e indica:
   - Build: `pip install -r requirements.txt`
   - Start command: dal `Procfile` → `web: streamlit run turbidity_app_web.py --server.port $PORT --server.address 0.0.0.0`
3. Abilita persistenza solo se vuoi salvare file; per uso standard i CSV restano solo in sessione.

## Note operative
- Mantieni i CSV di esempio piccoli; non commitare dati sensibili.
- Se serve cache più grande o timeout custom, aggiungi un file `.streamlit/config.toml` con le opzioni necessarie.
