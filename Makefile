install:
	poetry install --no-root

test:
	poetry run pytest .

lint:
	poetry run flake8 --exclude .venv,pytest_cache .

start:
	poetry run uvicorn main:app --reload

.PHONY: test
