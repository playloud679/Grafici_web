# Guida Completa - Caricamento Sito su Aruba con File Manager

Questa guida ti spiega passo-passo come caricare il sito sul tuo dominio Aruba usando il File Manager web (senza bisogno di programmi FTP).

## Passo 1: Accedi al Pannello di Controllo Aruba

1. Vai su **https://www.aruba.it**
2. Clicca su **"Accedi"** in alto a destra
3. Seleziona **"Pannello di Controllo"**
4. Inserisci le tue credenziali:
   - Username (o email)
   - Password
5. Clicca su **"Login"**

## Passo 2: Trova il File Manager

Dopo il login, dovresti vedere il pannello di controllo. Cerca una di queste voci:

- **"File Manager"** (di solito nel menu principale)
- **"Gestione File"**
- **"Hosting" → "File Manager"**
- **"WebMail e File Manager"**

Se non lo trovi subito, cerca nella barra di ricerca del pannello "File Manager".

## Passo 3: Accedi al File Manager

1. Clicca su **"File Manager"**
2. Potrebbe chiederti di nuovo la password
3. Si aprirà una finestra o scheda con l'interfaccia del File Manager
4. Vedrai una lista di cartelle

## Passo 4: Trova la Cartella Principale del Sito

La cartella dove caricare i file si può chiamare in vari modi:

- **/www**
- **/public_html**
- **/httpdocs**
- **/web**
- Una cartella con il nome del tuo dominio

**Come riconoscerla:**
- Di solito è l'unica cartella grande
- Potrebbe già contenere file come `index.html`, `index.php` o una cartella `cgi-bin`

**IMPORTANTE:** Entra in questa cartella facendo doppio click.

## Passo 5: Pulisci la Cartella (se necessario)

Se nella cartella trovi file vecchi o di esempio (tipo `index.html` con scritto "Il tuo sito è online"):

1. Seleziona i file vecchi
2. Clicca sul pulsante **"Elimina"** o l'icona del cestino
3. Conferma l'eliminazione

**ATTENZIONE:** Non eliminare cartelle di sistema come `cgi-bin`, `.well-known`, `logs`, ecc.

## Passo 6: Carica il File index.html

1. Clicca sul pulsante **"Carica"** o **"Upload"** (di solito in alto)
2. Si aprirà una finestra per selezionare i file
3. Vai alla cartella dove hai scaricato i file del sito
4. Seleziona il file **`index.html`**
5. Clicca su **"Apri"** o **"Carica"**
6. Aspetta che il caricamento sia completato (vedrai una barra di progresso)

## Passo 7: Crea le Cartelle css, js, img

Ora devi creare le cartelle per i file CSS e JavaScript:

### Creare la cartella CSS:
1. Clicca sul pulsante **"Nuova Cartella"** o **"Crea Cartella"**
2. Inserisci il nome: **`css`** (tutto minuscolo, senza spazi)
3. Clicca su **"Crea"** o **"OK"**

### Creare la cartella JS:
1. Clicca di nuovo su **"Nuova Cartella"**
2. Inserisci il nome: **`js`** (tutto minuscolo, senza spazi)
3. Clicca su **"Crea"** o **"OK"**

### Creare la cartella IMG:
1. Clicca di nuovo su **"Nuova Cartella"**
2. Inserisci il nome: **`img`** (tutto minuscolo, senza spazi)
3. Clicca su **"Crea"** o **"OK"**

## Passo 8: Carica i File nella Cartella CSS

1. **Entra nella cartella css** (doppio click su `css`)
2. Clicca su **"Carica"** o **"Upload"**
3. Seleziona il file **`style.css`** dalla cartella `css` del tuo computer
4. Clicca su **"Apri"** o **"Carica"**
5. Aspetta il completamento
6. Clicca su **"Torna indietro"** o sulla cartella principale per tornare alla root

## Passo 9: Carica i File nella Cartella JS

1. **Entra nella cartella js** (doppio click su `js`)
2. Clicca su **"Carica"** o **"Upload"**
3. Seleziona il file **`charts.js`** dalla cartella `js` del tuo computer
4. Clicca su **"Apri"** o **"Carica"**
5. Aspetta il completamento
6. Torna alla cartella principale

## Passo 10: Carica il File .htaccess

1. Assicurati di essere nella cartella principale (root)
2. Clicca su **"Carica"** o **"Upload"**
3. Seleziona il file **`.htaccess`**

**ATTENZIONE:** Il file `.htaccess` inizia con un punto. Se non lo vedi:
- Su Windows: attiva "Mostra file nascosti" in Esplora File
- Su Mac: Premi `Cmd + Shift + .` nel Finder

4. Carica il file
5. Aspetta il completamento

## Passo 11: Verifica i File Caricati

Nella cartella principale dovresti vedere:

```
/www (o /public_html)
├── index.html          ✓
├── .htaccess           ✓
├── css/
│   └── style.css      ✓
├── js/
│   └── charts.js      ✓
└── img/                ✓ (vuota)
```

## Passo 12: Imposta i Permessi (se necessario)

Alcuni server richiedono permessi specifici:

1. Seleziona il file `index.html`
2. Clicca destro o cerca il pulsante **"Permessi"** o **"Proprietà"**
3. Imposta i permessi a **644** (rw-r--r--)
4. Ripeti per `.htaccess` e i file in `css` e `js`

Per le cartelle, i permessi dovrebbero essere **755** (rwxr-xr-x)

## Passo 13: Testa il Sito

1. Apri un browser (Chrome, Firefox, Safari)
2. Vai su **`http://tuodominio.it`** (sostituisci con il tuo dominio)
3. Dovresti vedere la dashboard con i grafici

**Se non vedi nulla:**
- Aspetta 5-10 minuti (a volte il server impiega un po' ad aggiornarsi)
- Prova a ricaricare la pagina con `Ctrl + F5` (o `Cmd + R` su Mac)
- Svuota la cache del browser

## Risoluzione Problemi

### Il sito mostra ancora "Sito in costruzione"

1. Controlla di aver caricato `index.html` nella cartella giusta
2. Verifica che non ci sia un altro `index.html` o `index.php` nella stessa cartella
3. Prova a rinominare temporaneamente gli altri file index

### I grafici non si vedono

1. Apri la **Console del Browser** (F12 → Console)
2. Controlla se ci sono errori
3. Verifica che i file `style.css` e `charts.js` siano stati caricati nelle cartelle corrette
4. Controlla che i nomi delle cartelle siano esattamente `css`, `js`, `img` (tutto minuscolo)

### Errore 500 - Internal Server Error

1. Il file `.htaccess` potrebbe avere un errore
2. Prova a rinominarlo temporaneamente in `.htaccess.bak`
3. Se il sito funziona senza `.htaccess`, controlla la sintassi del file

### I CSS non vengono applicati

1. Verifica che `style.css` sia dentro la cartella `css`
2. Controlla il nome: deve essere esattamente `style.css` (tutto minuscolo)
3. Apri `index.html` e verifica che la riga `<link rel="stylesheet" href="css/style.css">` sia presente

## Dove Scaricare i File

Se non hai ancora scaricato i file dal repository, puoi:

1. Andare su GitHub: https://github.com/playloud679/Grafici_web
2. Cliccare sul branch `claude/setup-aruba-domain-01QAbkXBe8ZdAojjKxZY8hi8`
3. Cliccare su **"Code" → "Download ZIP"**
4. Estrarre il file ZIP sul tuo computer
5. Avrai tutti i file pronti per il caricamento

## Configurazioni Opzionali

### Abilitare HTTPS (SSL)

Se hai un certificato SSL su Aruba:

1. Nel File Manager, apri il file `.htaccess`
2. Cerca queste righe (intorno alla riga 6-7):
   ```
   # RewriteCond %{HTTPS} off
   # RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
   ```
3. Rimuovi i simboli `#` all'inizio
4. Salva il file
5. Ora il sito reindirizzerà automaticamente a HTTPS

### Personalizzare i Dati

Una volta che il sito funziona, puoi personalizzare:

1. **Testi**: Modifica `index.html` (puoi farlo anche dal File Manager)
2. **Colori**: Modifica `css/style.css`
3. **Dati grafici**: Modifica `js/charts.js`

## Supporto

Se hai problemi:

- **Supporto Aruba**: https://assistenza.aruba.it/ o telefono 0575 0505
- **Guida video Aruba File Manager**: Cerca su YouTube "File Manager Aruba"
- **Documentazione Aruba**: https://guide.aruba.it/

## Checklist Finale

Prima di chiudere, verifica:

- [ ] File `index.html` caricato nella root
- [ ] File `.htaccess` caricato nella root
- [ ] Cartella `css` creata con `style.css` dentro
- [ ] Cartella `js` creata con `charts.js` dentro
- [ ] Cartella `img` creata (anche se vuota)
- [ ] Sito visibile su `http://tuodominio.it`
- [ ] Grafici visualizzati correttamente
- [ ] Sito responsive (provato su mobile)

Complimenti, il tuo sito è online!
