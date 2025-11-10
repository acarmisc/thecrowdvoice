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

**Metodo consigliato (usa script bash):**
```bash
./start.sh
```

**Metodo alternativo (con docker-compose):**
```bash
docker-compose up --build
```

Attendi che i servizi siano pronti (~30-60 secondi per il primo avvio).

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
   ./stop.sh && ./start.sh
   ```
5. Vai su "Canali" e clicca "Facebook"
6. Autorizza l'app
7. Clicca "Sincronizza" per scaricare i messaggi
8. Vai su "Messaggi" e clicca "Analizza Tutti"
9. Torna alla Dashboard per vedere le statistiche!

## Comandi Utili

**Con gli script (più semplice):**
```bash
./start.sh                  # Avvia tutto
./stop.sh                   # Ferma tutto
./clean.sh                  # Pulisce tutto (attenzione: cancella DB!)
./logs.sh                   # Mostra tutti i log
./logs.sh backend           # Solo log backend
./logs.sh frontend          # Solo log frontend
```

**Con Docker diretto:**
```bash
# Vedere i log
docker logs -f social-analytics-backend
docker logs -f social-analytics-frontend

# Accedere al container backend
docker exec -it social-analytics-backend bash

# Eseguire migrazioni
docker exec -it social-analytics-backend python manage.py migrate

# Creare superuser
docker exec -it social-analytics-backend python manage.py createsuperuser
```

**Con docker-compose:**
```bash
docker-compose down         # Ferma
docker-compose up           # Avvia
docker-compose logs -f      # Log
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
