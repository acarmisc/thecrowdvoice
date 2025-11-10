#!/bin/bash

# Script per fermare Social Analytics MVP

echo "🛑 Arresto Social Analytics MVP..."

# Ferma i container
docker stop social-analytics-backend social-analytics-frontend 2>/dev/null || true

# Rimuovi i container
docker rm social-analytics-backend social-analytics-frontend 2>/dev/null || true

echo "✅ Servizi fermati"
echo ""
echo "Per riavviare: ./start.sh"
echo "Per pulire tutto (DB incluso): ./clean.sh"
