.PHONY: help build up down restart logs clean

help:
	@echo "Social Analytics MVP - Comandi disponibili:"
	@echo ""
	@echo "  make build     - Build dei container Docker"
	@echo "  make up        - Avvia i servizi"
	@echo "  make down      - Ferma i servizi"
	@echo "  make restart   - Riavvia i servizi"
	@echo "  make logs      - Mostra i log"
	@echo "  make clean     - Pulisci tutto (attenzione: cancella i dati!)"
	@echo "  make shell-backend  - Accedi al container backend"
	@echo "  make shell-frontend - Accedi al container frontend"
	@echo "  make migrate   - Esegui le migrazioni Django"
	@echo "  make superuser - Crea un superuser Django"
	@echo ""

build:
	docker compose build

up:
	docker compose up

up-d:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

logs-backend:
	docker compose logs -f backend

logs-frontend:
	docker compose logs -f frontend

clean:
	docker compose down -v
	rm -rf backend/db.sqlite3

shell-backend:
	docker compose exec backend bash

shell-frontend:
	docker compose exec frontend sh

migrate:
	docker compose exec backend python manage.py migrate

makemigrations:
	docker compose exec backend python manage.py makemigrations

superuser:
	docker compose exec backend python manage.py createsuperuser

test-backend:
	docker compose exec backend python manage.py test

# Alternative per chi non ha Docker Compose moderno
build-legacy:
	docker-compose build

up-legacy:
	docker-compose up

up-d-legacy:
	docker-compose up -d
