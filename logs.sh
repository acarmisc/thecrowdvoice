#!/bin/bash

# Script per visualizzare i log dei servizi

if [ "$1" == "backend" ]; then
    echo "📋 Log Backend (Ctrl+C per uscire)..."
    docker logs -f social-analytics-backend
elif [ "$1" == "frontend" ]; then
    echo "📋 Log Frontend (Ctrl+C per uscire)..."
    docker logs -f social-analytics-frontend
else
    echo "📋 Log di tutti i servizi (Ctrl+C per uscire)..."
    echo ""
    docker logs -f social-analytics-backend &
    docker logs -f social-analytics-frontend &
    wait
fi
