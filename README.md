# Grafici Web - Dashboard Interattiva

Dashboard moderna e responsive con grafici interattivi realizzata con HTML, CSS e JavaScript (Chart.js).

## Caratteristiche

- Dashboard con 4 grafici interattivi (vendite, utenti, traffico, prodotti)
- Design responsive per mobile, tablet e desktop
- Statistiche in tempo reale con card animate
- Ottimizzata per le performance
- Configurazione Apache pronta per hosting Aruba

## Tecnologie Utilizzate

- HTML5
- CSS3 (con CSS Grid e Flexbox)
- JavaScript (ES6+)
- Chart.js 4.4.0 (libreria per grafici)

## Struttura del Progetto

```
Grafici_web/
├── index.html          # Pagina principale
├── css/
│   └── style.css      # Stili del sito
├── js/
│   └── charts.js      # Configurazione grafici
├── img/               # Cartella per immagini (vuota)
├── .htaccess          # Configurazione Apache
└── README.md          # Questo file
```

## Come Caricare il Sito su Aruba

### Metodo 1: File Manager Web di Aruba (Raccomandato - Nessun software richiesto)

**Per una guida completa passo-passo con screenshot e risoluzione problemi, leggi [GUIDA_FILE_MANAGER_ARUBA.md](GUIDA_FILE_MANAGER_ARUBA.md)**

Procedura rapida:

1. **Accedi al pannello Aruba** su https://www.aruba.it
2. **Vai su "File Manager"** nel menu
3. **Naviga nella cartella principale** del sito (`/www` o `/public_html`)
4. **Carica `index.html`** nella root
5. **Crea le cartelle** `css`, `js`, `img`
6. **Carica i file nelle cartelle**:
   - `style.css` nella cartella `css/`
   - `charts.js` nella cartella `js/`
7. **Carica `.htaccess`** nella root
8. **Verifica** il sito su `http://tuodominio.it`

### Metodo 2: FTP (Per utenti avanzati)

1. **Scarica un client FTP**
   - FileZilla (Windows/Mac/Linux): https://filezilla-project.org/
   - WinSCP (Windows): https://winscp.net/
   - Cyberduck (Mac): https://cyberduck.io/

2. **Recupera le credenziali FTP** dal pannello Aruba
   - Host: `ftp.tuodominio.it` o `ftp.aruba.it`
   - Username e password dal pannello

3. **Connetti al server FTP** e carica tutti i file nella cartella principale

4. **Verifica** il sito su `http://tuodominio.it`

### Configurazione SSL (HTTPS)

Se hai un certificato SSL su Aruba:

1. Apri il file `.htaccess`
2. Rimuovi i commenti (`#`) dalle righe:
   ```apache
   # RewriteCond %{HTTPS} off
   # RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
   ```
   Diventeranno:
   ```apache
   RewriteCond %{HTTPS} off
   RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
   ```
3. Ricarica il file `.htaccess` via FTP

### Configurazione WWW

Se vuoi forzare o rimuovere il `www` dal dominio:

**Per rimuovere www** (es. www.tuodominio.it → tuodominio.it):
```apache
RewriteCond %{HTTP_HOST} ^www\.(.*)$ [NC]
RewriteRule ^(.*)$ https://%1/$1 [R=301,L]
```

**Per aggiungere www** (es. tuodominio.it → www.tuodominio.it):
```apache
RewriteCond %{HTTP_HOST} ^[^.]+\.[^.]+$
RewriteRule ^(.*)$ https://www.%{HTTP_HOST}/$1 [L,R=301]
```

## Personalizzazione

### Modificare i dati dei grafici

Apri `js/charts.js` e modifica i dati nei vari dataset. Esempio:

```javascript
datasets: [{
    label: 'Vendite 2024',
    data: [12500, 19800, 15600, ...], // <-- Modifica questi valori
    ...
}]
```

### Modificare i colori

Apri `css/style.css` e modifica le variabili CSS all'inizio del file:

```css
:root {
    --primary-color: #6366f1;     /* Colore primario */
    --secondary-color: #8b5cf6;   /* Colore secondario */
    --success-color: #10b981;     /* Colore successo */
    ...
}
```

### Modificare i testi

Apri `index.html` e modifica i testi direttamente nel codice HTML.

## Risoluzione Problemi

### Il sito non si carica

1. Verifica che `index.html` sia nella cartella principale
2. Controlla i permessi dei file (devono essere 644 per i file, 755 per le cartelle)
3. Verifica che il dominio sia correttamente puntato al tuo hosting

### I grafici non vengono visualizzati

1. Controlla la console del browser (F12) per errori
2. Verifica che il file `js/charts.js` sia stato caricato correttamente
3. Assicurati che il CDN di Chart.js sia accessibile

### Errore 500

1. Controlla il file `.htaccess` per errori di sintassi
2. Verifica che mod_rewrite sia abilitato sul server Aruba
3. Prova a rinominare temporaneamente `.htaccess` in `.htaccess.bak` per vedere se il problema persiste

### CSS o JS non si aggiornano

1. Svuota la cache del browser (Ctrl+F5)
2. Verifica che i file siano stati caricati correttamente via FTP
3. Controlla che i percorsi nei file HTML siano corretti

## Supporto

Per problemi con l'hosting Aruba:
- Supporto Aruba: https://assistenza.aruba.it/
- Telefono: 0575 0505

Per problemi con il codice:
- Apri una issue su GitHub

## Licenza

Questo progetto è open source e disponibile per uso personale e commerciale.

## Crediti

- Chart.js: https://www.chartjs.org/
- Font: System fonts
