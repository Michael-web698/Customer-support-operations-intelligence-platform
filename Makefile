.PHONY: help db-up db-down db-status db-clean db-shell venv install clean

# Load environment variables from .env if it exists
ifneq (,$(wildcard .env))
    include .env
    export $(shell sed 's/=.*//' .env)
endif

# Default Target
help:
	@echo "========================================================================"
	@echo "Customer Support Operations Intelligence Platform - Developer Workflows"
	@echo "========================================================================"
	@echo "Database Commands:"
	@echo "  make db-up       Start PostgreSQL database container"
	@echo "  make db-down     Stop PostgreSQL database container"
	@echo "  make db-status   Check database container status and health"
	@echo "  make db-clean    Stop container and remove all database data volume"
	@echo "  make db-shell    Open an interactive psql shell inside the container"
	@echo ""
	@echo "Environment Commands:"
	@echo "  make venv        Create Python virtual environment"
	@echo "  make install     Install dependencies inside virtual environment"
	@echo "  make clean       Clean up Python cache files and logs"
	@echo "========================================================================"

# Database Commands
db-up:
	docker-compose up -d
	@echo "Waiting for database to be healthy..."
	@until [ "$$(docker inspect --format='{{json .State.Health.Status}}' support_ops_db)" = "\"healthy\"" ]; do \
		echo "Database status: $$(docker inspect --format='{{json .State.Health.Status}}' support_ops_db)..."; \
		sleep 2; \
	done
	@echo "PostgreSQL is up and healthy!"

db-down:
	docker-compose down

db-status:
	docker-compose ps

db-clean:
	docker-compose down -v

db-shell:
	docker exec -it support_ops_db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

# Environment Setup
venv:
	python3 -m venv venv
	@echo "Virtual environment created. Activate with: source venv/bin/activate"

install:
	@if [ ! -d "venv" ]; then \
		make venv; \
	fi
	./venv/bin/pip install --upgrade pip
	@if [ -f "requirements.txt" ]; then \
		./venv/bin/pip install -r requirements.txt; \
	else \
		echo "No requirements.txt found, skipping library install. Create it first."; \
	fi

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf venv
