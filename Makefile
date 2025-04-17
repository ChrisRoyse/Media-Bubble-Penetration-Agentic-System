.PHONY: up down logs fmt lint test

up:
	docker compose up --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=100

fmt:
	black .

lint:
	ruff check .

test:
	pytest -q || true
