install:
	poetry install --no-root

test:
	poetry run pytest .

lint:
	poetry run flake8 --exclude .venv,pytest_cache .

start:
	poetry run uvicorn main:app --reload

catbread:
	docker run -p 80:8080 -v bot_db:/code/db/ --rm ssant/catbread

docker-build:
	docker build -t catbread .

docker-run:
	docker run -p 80:8080 -v bot_db:/code/db/ --rm catbread

compose:
	docker compose up

compose-down:
	docker compose down


.PHONY: test 
