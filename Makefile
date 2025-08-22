PYTHON = python3
PIP = pip
MANAGE = $(PYTHON) manage.py
DB_PORT = 5234
APP_PORT = 8000

run:
	docker compose up -d
	sleep 5
	- fuser -k $(DB_PORT)/tcp || true
	- fuser -k $(APP_PORT)/tcp || true
	$(MANAGE) migrate
	$(MANAGE) runserver 127.0.0.1:$(APP_PORT)

bot:
	$(PYTHON) -m bots.telegram.bot

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

createsuperuser:
	$(MANAGE) createsuperuser

install:
	$(PIP) install -r requirements.txt

stop:
	docker compose down

logs:
	docker compose logs -f

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
