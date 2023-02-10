args := $(wordlist 2, 100, $(MAKECMDGOALS))

env:
	cp .env.example .env

format:
	poetry run black .; poetry run isort .

run:
	poetry run python3 -m server

revision: 
	cd server/db; poetry run alembic revision --autogenerate

upgrade:
	cd server/db; poetry run alembic upgrade $(args)

db:
	docker compose up -d --remove-orphans
