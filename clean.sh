#!/bin/bash

# Script per pulire completamente l'ambiente

echo "🧹 Pulizia completa Social Analytics MVP..."
echo ""
read -p "⚠️  ATTENZIONE: Questo cancellerà tutti i dati del database. Continuare? (y/N) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Ferma e rimuovi container
    docker stop social-analytics-backend social-analytics-frontend 2>/dev/null || true
    docker rm social-analytics-backend social-analytics-frontend 2>/dev/null || true

    # Rimuovi immagini
    docker rmi social-analytics-backend:latest social-analytics-frontend:latest 2>/dev/null || true

    # Rimuovi volume database
    docker volume rm social-analytics-db 2>/dev/null || true

    # Rimuovi network
    docker network rm social-analytics-network 2>/dev/null || true

    echo "✅ Pulizia completata"
    echo ""
    echo "Per riavviare da zero: ./start.sh"
else
    echo "❌ Operazione annullata"
fi
