# Quick Start Guide

Guida rapida per avviare l'MVP in 5 minuti.

## Prerequisiti

- Docker Desktop installato e in esecuzione
- Account developer sulle piattaforme social (opzionale per il primo test)

## Passi

### 1. Prepara l'ambiente

```bash
# Crea il file .env (anche vuoto per iniziare)
cp .env.example .env
```

### 2. Avvia i container

```bash
# Build e start
docker-compose up --build

# Oppure in background
docker-compose up -d --build
```

Attendi che i servizi siano pronti. Vedrai:
```
backend_1   | Django version 4.2.7, using settings 'social_analytics.settings'
backend_1   | Starting development server at http://0.0.0.0:8000/
frontend_1  | webpack compiled successfully
```

### 3. Crea il primo utente

Apri http://localhost:3000 nel browser:

1. Clicca su "Registrati"
2. Compila il form:
   - Username: `demo`
   - Email: `demo@example.com`
   - Password: `demo1234`
3. Clicca "Registrati"

Verrai reindirizzato automaticamente alla Dashboard!

### 4. Test senza connessioni social

Anche senza connettere canali social, puoi esplorare:
- Dashboard con statistiche (vuote inizialmente)
- Pagina Canali
- Pagina Messaggi

### 5. (Opzionale) Crea superuser per Django Admin

```bash
docker-compose exec backend python manage.py createsuperuser
```

Poi vai su http://localhost:8000/admin

### 6. (Opzionale) Connetti Facebook

1. Crea un'app su https://developers.facebook.com/
2. Copia App ID e App Secret
3. Aggiorna `.env`:
   ```env
   FACEBOOK_APP_ID=your_app_id
   FACEBOOK_APP_SECRET=your_app_secret
   ```
4. Riavvia i container:
   ```bash
   docker-compose restart
   ```
5. Vai su "Canali" e clicca "Facebook"
6. Autorizza l'app
7. Clicca "Sincronizza" per scaricare i messaggi
8. Vai su "Messaggi" e clicca "Analizza Tutti"
9. Torna alla Dashboard per vedere le statistiche!

## Comandi Utili

```bash
# Fermare i container
docker-compose down

# Riavviare dopo modifiche
docker-compose restart

# Vedere i log
docker-compose logs -f

# Accedere al container backend
docker-compose exec backend bash

# Eseguire migrazioni
docker-compose exec backend python manage.py migrate

# Creare superuser
docker-compose exec backend python manage.py createsuperuser

# Pulire tutto e ricominciare
docker-compose down -v
docker-compose up --build
```

## Problemi Comuni

### Frontend non si connette al backend

Verifica che il proxy sia configurato correttamente in `frontend/package.json`:
```json
"proxy": "http://backend:8000"
```

### Errori CORS

Assicurati che `CORS_ALLOWED_ORIGINS` in `.env` includa `http://localhost:3000`

### Database locked

SQLite può dare problemi con accessi concorrenti. Riavvia i container:
```bash
docker-compose restart
```

## Prossimi Passi

Leggi il [README.md](README.md) completo per:
- Configurazione dettagliata delle piattaforme social
- API endpoints disponibili
- Guida allo sviluppo
- Best practices per production
