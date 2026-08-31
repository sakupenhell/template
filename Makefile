help:  ## Show this help
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/ /'


clean_pycache: ## Remove python cache directories
	find . -type d -name "__pycache__" -exec rm -r {} +

local: ## Run app locally
	docker compose up --build

ruff: ## Run ruff
	uv run ruff check --fix

mypy: ## Run mypy
	uv run mypy .
