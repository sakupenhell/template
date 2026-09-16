help:  ## Show this help
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/ /'


clean_pycache: ## Remove python cache directories
	find . -type d -name "__pycache__" -exec rm -r {} +

local: ## Run app locally
	docker compose up --build

down: ## Stop the local docker compose stack
	docker compose down

ruff: ## Run ruff
	uv run ruff check --fix

format: ## Run ruff format
	uv run ruff format .

mypy: ## Run mypy
	uv run mypy .

test: ## Run the test suite
	uv run pytest

migration: ## Autogenerate an alembic migration, e.g. make migration m="add users table"
	docker compose exec backend alembic revision --autogenerate -m "$(m)"

migrate: ## Apply alembic migrations up to head
	docker compose exec backend alembic upgrade head

downgrade: ## Revert the last alembic migration
	docker compose exec backend alembic downgrade -1

worker: ## Run the taskiq worker locally
	uv run taskiq worker src.entrypoints.workers.worker:broker
