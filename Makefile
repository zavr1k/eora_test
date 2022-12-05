install:
	poetry install --no-root

test:
	poetry run pytest .

lint:
	poetry run flake8 --exclude .venv,pytest_cache .

start:
	poetry run uvicorn main:app --reload

docker:
	docker run -p 80:80 -v bot_db:/code/db/ --rm ssant/catbread

build:
	docker build -t ssant/catbread .

.PHONY: test 
