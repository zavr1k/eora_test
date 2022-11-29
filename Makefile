install:
	poetry install --no-root

test:
	poetry run pytest .

lint:
	poetry run flake8 tests main.py bot.py

.PHONY: test
