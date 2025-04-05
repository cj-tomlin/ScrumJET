.PHONY: setup build up down init db-init db-migrate db-upgrade load-data test format lint pre-commit install-hooks run-hooks help

# Default target
.DEFAULT_GOAL := help

# Variables
DOCKER_COMPOSE = docker-compose

# Help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Setup
setup: ## Install Poetry dependencies
	poetry install

# Docker commands
build: ## Build Docker containers
	$(DOCKER_COMPOSE) build

up: ## Start Docker containers
	$(DOCKER_COMPOSE) up -d

down: ## Stop Docker containers
	$(DOCKER_COMPOSE) down

# Database commands
db-init: ## Initialize the database
	$(DOCKER_COMPOSE) exec web flask db init

db-migrate: ## Create a database migration
	$(DOCKER_COMPOSE) exec web flask db migrate -m "$(message)"

db-upgrade: ## Apply database migrations
	$(DOCKER_COMPOSE) exec web flask db upgrade

load-data: ## Load sample data
	$(DOCKER_COMPOSE) exec web python scripts/init_db.py

# Development commands
logs: ## View Docker logs
	$(DOCKER_COMPOSE) logs -f

shell: ## Access shell in web container
	$(DOCKER_COMPOSE) exec web bash

# Pre-commit hooks
install-hooks: ## Install pre-commit hooks
	poetry run pre-commit install

run-hooks: ## Run pre-commit hooks on all files
	poetry run pre-commit run --all-files

# Testing and code quality
test: ## Run tests (to be implemented)
	@echo "Tests will be implemented in the future"
	# $(DOCKER_COMPOSE) exec web pytest

format: ## Format code with ruff
	poetry run ruff format app

lint: ## Lint code with ruff
	poetry run ruff check app --fix

# Combined commands
init: up db-init db-migrate db-upgrade load-data ## Initialize everything (start containers, setup DB, load data)
setup-dev: setup install-hooks ## Setup development environment with pre-commit hooks