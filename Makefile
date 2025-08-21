PYTHON = python3
PIP = pip
MANAGE = $(PYTHON) manage.py

run:
	$(MANAGE) runserver

bot:
	$(PYTHON) -m bots.telegram.bot

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

createsuperuser:
	$(MANAGE) createsuperuser

install:
	$(PIP) install -r requirements.txt

clean:
	find . -name "__pycache__" -exec rm -rf {} +

