#!/bin/bash

# Script di avvio semplificato per Social Analytics MVP
# Usa comandi Docker standard senza buildx

set -e

echo "🚀 Avvio Social Analytics MVP..."
echo ""

# Colori per output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Crea network se non esiste
echo -e "${YELLOW}Creazione network...${NC}"
docker network create social-analytics-network 2>/dev/null || echo "Network già esistente"

# Build backend con docker standard
echo -e "${YELLOW}Build backend...${NC}"
cd backend
docker build --platform linux/amd64 -t social-analytics-backend:latest .
cd ..

# Build frontend
echo -e "${YELLOW}Build frontend...${NC}"
cd frontend
docker build --platform linux/amd64 -t social-analytics-frontend:latest .
cd ..

# Crea volume per il database se non esiste
echo -e "${YELLOW}Creazione volume database...${NC}"
docker volume create social-analytics-db 2>/dev/null || echo "Volume già esistente"

# Ferma e rimuovi container esistenti
echo -e "${YELLOW}Pulizia container esistenti...${NC}"
docker stop social-analytics-backend 2>/dev/null || true
docker stop social-analytics-frontend 2>/dev/null || true
docker rm social-analytics-backend 2>/dev/null || true
docker rm social-analytics-frontend 2>/dev/null || true

# Leggi variabili da .env se esiste
if [ -f .env ]; then
    echo -e "${YELLOW}Caricamento variabili da .env...${NC}"
    export $(cat .env | grep -v '^#' | xargs)
fi

# Avvia backend
echo -e "${YELLOW}Avvio backend...${NC}"
docker run -d \
    --name social-analytics-backend \
    --network social-analytics-network \
    -p 8000:8000 \
    -v "$(pwd)/backend:/app" \
    -v social-analytics-db:/app/db.sqlite3 \
    -e DEBUG=True \
    -e DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY:-django-insecure-mvp-development-key} \
    -e ALLOWED_HOSTS=localhost,127.0.0.1,backend \
    -e CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000 \
    -e FACEBOOK_APP_ID=${FACEBOOK_APP_ID:-} \
    -e FACEBOOK_APP_SECRET=${FACEBOOK_APP_SECRET:-} \
    -e INSTAGRAM_APP_ID=${INSTAGRAM_APP_ID:-} \
    -e INSTAGRAM_APP_SECRET=${INSTAGRAM_APP_SECRET:-} \
    -e LINKEDIN_CLIENT_ID=${LINKEDIN_CLIENT_ID:-} \
    -e LINKEDIN_CLIENT_SECRET=${LINKEDIN_CLIENT_SECRET:-} \
    -e TIKTOK_CLIENT_KEY=${TIKTOK_CLIENT_KEY:-} \
    -e TIKTOK_CLIENT_SECRET=${TIKTOK_CLIENT_SECRET:-} \
    social-analytics-backend:latest

# Aspetta che il backend sia pronto
echo -e "${YELLOW}Attendo che il backend sia pronto...${NC}"
sleep 5

# Avvia frontend
echo -e "${YELLOW}Avvio frontend...${NC}"
docker run -d \
    --name social-analytics-frontend \
    --network social-analytics-network \
    -p 3000:3000 \
    -v "$(pwd)/frontend:/app" \
    -v /app/node_modules \
    -e REACT_APP_API_URL=http://localhost:8000/api \
    -e CHOKIDAR_USEPOLLING=true \
    social-analytics-frontend:latest

echo ""
echo -e "${GREEN}✅ Avvio completato!${NC}"
echo ""
echo "L'applicazione è disponibile su:"
echo "  🌐 Frontend: http://localhost:3000"
echo "  🔧 Backend:  http://localhost:8000"
echo "  ⚙️  Admin:    http://localhost:8000/admin"
echo ""
echo "Comandi utili:"
echo "  ./start.sh          - Avvia i servizi"
echo "  ./stop.sh           - Ferma i servizi"
echo "  docker logs -f social-analytics-backend  - Log backend"
echo "  docker logs -f social-analytics-frontend - Log frontend"
echo ""
