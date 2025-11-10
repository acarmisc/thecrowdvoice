# Social Analytics MVP

Applicazione web per la raccolta e l'analisi delle interazioni dai social network (Facebook, Instagram, LinkedIn, TikTok).

## Caratteristiche

- **Autenticazione utente** con JWT
- **Connessione multi-canale** tramite OAuth 2.0
- **Raccolta automatica** di messaggi, commenti, menzioni e tag
- **Analisi del sentiment** automatica con TextBlob
- **Dashboard** con statistiche e metriche
- **API REST** completa con Django REST Framework
- **UI moderna** con React

## Struttura del Progetto

```
thecrowdvoice/
├── backend/               # Django backend
│   ├── social_analytics/  # Progetto principale
│   │   ├── accounts/      # Gestione utenti e autenticazione
│   │   ├── channels/      # Connessione canali social
│   │   ├── messages/      # Gestione messaggi e interazioni
│   │   └── sentiment/     # Analisi sentiment
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # Componenti React
│   │   ├── pages/         # Pagine dell'app
│   │   └── services/      # API services
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml     # Orchestrazione Docker
└── README.md
```

## Requisiti

- Docker e Docker Compose
- Credenziali API per le piattaforme social che vuoi integrare

## Setup Rapido

### 1. Clona il repository

```bash
git clone <repository-url>
cd thecrowdvoice
```

### 2. Configura le variabili d'ambiente

Copia il file di esempio e inserisci le tue credenziali API:

```bash
cp .env.example .env
```

Modifica `.env` con le tue credenziali:

```env
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
# ... altre credenziali
```

### 3. Avvia l'applicazione

```bash
docker-compose up --build
```

L'applicazione sarà disponibile su:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin

### 4. Crea un superuser (opzionale)

Per accedere al Django Admin:

```bash
docker-compose exec backend python manage.py createsuperuser
```

## Configurazione Piattaforme Social

### Facebook

1. Vai su [Facebook Developers](https://developers.facebook.com/)
2. Crea una nuova app
3. Aggiungi il prodotto "Facebook Login"
4. Configura OAuth Redirect URI: `http://localhost:8000/api/channels/facebook/callback`
5. Richiedi i permessi:
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_manage_metadata`
   - `pages_messaging`

### Instagram

Instagram usa le stesse credenziali di Facebook (Facebook Graph API).

1. Nella tua Facebook App, aggiungi il prodotto "Instagram"
2. Configura OAuth Redirect URI: `http://localhost:8000/api/channels/instagram/callback`
3. Richiedi i permessi:
   - `instagram_basic`
   - `instagram_manage_messages`
   - `instagram_manage_comments`

### LinkedIn

1. Vai su [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Crea una nuova app
3. Configura OAuth Redirect URI: `http://localhost:8000/api/channels/linkedin/callback`
4. Richiedi i permessi:
   - `r_liteprofile`
   - `r_emailaddress`
   - `w_member_social`

### TikTok

1. Vai su [TikTok Developers](https://developers.tiktok.com/)
2. Crea una nuova app
3. Configura Redirect URI: `http://localhost:8000/api/channels/tiktok/callback`
4. Richiedi i permessi necessari

## Utilizzo

### 1. Registrazione/Login

1. Apri http://localhost:3000
2. Registrati con username, email e password
3. Effettua il login

### 2. Connetti Canali Social

1. Vai su "Canali"
2. Clicca sul pulsante della piattaforma che vuoi connettere
3. Autorizza l'app tramite OAuth
4. Il canale verrà aggiunto alla lista

### 3. Sincronizza Messaggi

1. Dalla pagina "Canali", clicca su "Sincronizza" per ogni canale
2. I messaggi verranno scaricati automaticamente
3. Vai su "Messaggi" per visualizzarli

### 4. Analizza Sentiment

1. Dalla pagina "Messaggi", clicca su "Analizza Tutti"
2. Il sistema analizzerà automaticamente il sentiment di tutti i messaggi
3. Visualizza le statistiche nella Dashboard

## API Endpoints

### Autenticazione

- `POST /api/auth/register/` - Registrazione nuovo utente
- `POST /api/auth/login/` - Login
- `POST /api/auth/refresh/` - Refresh token JWT
- `GET /api/auth/me/` - Ottieni utente corrente

### Canali

- `GET /api/channels/accounts/` - Lista canali connessi
- `GET /api/channels/facebook/auth-url/` - URL OAuth Facebook
- `GET /api/channels/facebook/callback/` - Callback OAuth Facebook
- `DELETE /api/channels/accounts/{id}/` - Disconnetti canale

### Messaggi

- `GET /api/messages/` - Lista messaggi (con filtri)
- `POST /api/messages/sync/{account_id}/` - Sincronizza messaggi

### Sentiment

- `GET /api/sentiment/analyses/` - Lista analisi sentiment
- `POST /api/sentiment/analyze/{message_id}/` - Analizza singolo messaggio
- `POST /api/sentiment/batch-analyze/` - Analizza tutti i messaggi non processati
- `GET /api/sentiment/stats/` - Statistiche sentiment

## Sviluppo

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate su Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm start
```

## Database

L'MVP usa SQLite per semplicità. Per production, si consiglia di migrare a PostgreSQL modificando `backend/social_analytics/settings.py`.

## Priorità di Integrazione

Basandosi sulla facilità di integrazione e minori processi approvativi:

1. **Facebook** ⭐⭐⭐⭐⭐ - API ben documentata, relativamente semplice
2. **Instagram** ⭐⭐⭐⭐ - Usa Facebook Graph API, richiede app review per alcune funzioni
3. **LinkedIn** ⭐⭐⭐ - API più limitata, processi di approvazione più stringenti
4. **TikTok** ⭐⭐ - API commerciale limitata, richiede approvazione

## Note di Sicurezza

- **Non committare mai** il file `.env` con le credenziali reali
- Cambiare `DJANGO_SECRET_KEY` in produzione
- Usare HTTPS in produzione
- Configurare correttamente CORS per production
- Implementare rate limiting per le API

## Limiti dell'MVP

- Database SQLite (non scalabile per production)
- Nessun sistema di code per job asincroni
- Sentiment analysis basilare con TextBlob
- Nessun sistema di notifiche real-time
- Nessun sistema di backup automatico

## Prossimi Passi

1. Implementare webhook per notifiche real-time
2. Aggiungere Redis + Celery per job asincroni
3. Migliorare sentiment analysis con modelli ML avanzati
4. Aggiungere dashboard analytics più dettagliata
5. Implementare sistema di risposte automatiche
6. Aggiungere export dati (CSV, PDF)
7. Implementare notifiche email/push

## Supporto

Per problemi o domande, apri un issue su GitHub.

## Licenza

MIT License
