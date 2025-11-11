#!/bin/bash

# Script per gestire dati demo

echo "📊 Gestione Dati Demo"
echo ""
echo "Scegli un'opzione:"
echo "  1) Crea solo utente demo (senza dati)"
echo "  2) Crea utente + dati demo completi"
echo "  3) Mostra credenziali demo"
echo ""
read -p "Scelta [1-3]: " choice

case $choice in
  1)
    echo "Creazione utente demo..."
    docker exec -it social-analytics-backend python manage.py create_demo_user
    ;;
  2)
    echo "Creazione dati demo completi..."
    docker exec -it social-analytics-backend python manage.py create_demo_data
    ;;
  3)
    echo ""
    echo "╔════════════════════════════════════════╗"
    echo "║      CREDENZIALI UTENTE DEMO          ║"
    echo "╠════════════════════════════════════════╣"
    echo "║  Username: demo                        ║"
    echo "║  Password: demo1234                    ║"
    echo "║  Email:    demo@example.com            ║"
    echo "╠════════════════════════════════════════╣"
    echo "║  URL: http://localhost:3000            ║"
    echo "╚════════════════════════════════════════╝"
    echo ""
    ;;
  *)
    echo "Scelta non valida"
    exit 1
    ;;
esac
