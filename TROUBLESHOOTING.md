# Risoluzione Problemi Docker

## Errore: "compose build requires buildx 0.17 or later"

Questo errore può verificarsi con versioni non aggiornate di Docker. Ecco le soluzioni:

### Soluzione 1: Usa gli script bash (PIÙ SEMPLICE) ⭐

```bash
./start.sh
```

Questo script bypassa completamente docker-compose e usa comandi Docker standard.

Altri script disponibili:
```bash
./stop.sh   # Ferma i servizi
./clean.sh  # Pulisce tutto
./logs.sh   # Mostra i log
```

### Soluzione 2: Aggiorna Docker Desktop

Scarica e installa l'ultima versione di Docker Desktop da:
https://www.docker.com/products/docker-desktop

### Soluzione 3: Usa docker-compose (versione legacy)

Se hai docker-compose installato separatamente:

```bash
docker-compose up --build
```

### Soluzione 4: Usa il Makefile

```bash
make up
```

O per la versione legacy:

```bash
make up-legacy
```

### Soluzione 4: Avvio manuale senza Docker Compose

#### Backend

```bash
cd backend

# Crea virtual environment
python -m venv venv

# Attiva virtual environment
# Su Mac/Linux:
source venv/bin/activate
# Su Windows:
# venv\Scripts\activate

# Installa dipendenze
pip install -r requirements.txt

# Download TextBlob corpora
python -m textblob.download_corpora

# Esegui migrazioni
python manage.py migrate

# Crea superuser (opzionale)
python manage.py createsuperuser

# Avvia server
python manage.py runserver
```

#### Frontend (in un altro terminale)

```bash
cd frontend

# Installa dipendenze
npm install

# Avvia server di sviluppo
npm start
```

L'app sarà disponibile su:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

### Soluzione 5: Build separato dei container

```bash
# Build backend
docker build -t social-analytics-backend ./backend

# Build frontend
docker build -t social-analytics-frontend ./frontend

# Run backend
docker run -d -p 8000:8000 --name backend \
  -e DEBUG=True \
  -e DJANGO_SECRET_KEY=dev-key \
  -e ALLOWED_HOSTS=localhost,127.0.0.1 \
  -e CORS_ALLOWED_ORIGINS=http://localhost:3000 \
  social-analytics-backend

# Run frontend
docker run -d -p 3000:3000 --name frontend \
  -e REACT_APP_API_URL=http://localhost:8000/api \
  social-analytics-frontend
```

## Verifica versione Docker

```bash
docker --version
docker compose version
```

Dovresti avere almeno:
- Docker version 20.10+
- Docker Compose version 2.0+

## Altri problemi comuni

### Port già in uso

Se ricevi errori che le porte 3000 o 8000 sono già in uso:

```bash
# Trova e termina i processi
# Su Mac/Linux:
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9

# Su Windows:
# netstat -ano | findstr :3000
# taskkill /PID <PID> /F
```

### CORS errors

Assicurati che il file `.env` contenga:
```
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Database locked

Se SQLite è bloccato:

```bash
docker compose down
docker compose up
```

### Frontend non si connette al backend

Verifica in `frontend/package.json` che ci sia:
```json
"proxy": "http://localhost:8000"
```

## Supporto

Se i problemi persistono, apri un issue su GitHub con:
- Output completo dell'errore
- Versione di Docker (`docker --version`)
- Sistema operativo
