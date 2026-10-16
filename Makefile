.PHONY: style test xtest ci_check envup run runui db_revision db_migrate

VENV_BIN_PATH = ./.venv/bin
PYTHONPATH = $(shell pwd)

envup:
	$(VENV_BIN_PATH)/pip install -c source/constraints.txt -r requirements.txt

style:
	$(VENV_BIN_PATH)/flake8 mychecklist
	$(VENV_BIN_PATH)/flake8 --ignore=D tests

test:
	$(VENV_BIN_PATH)/python3 manage.py test -v 2

xtest:
	$(VENV_BIN_PATH)/python3 manage.py test -v 2 --failfast

ci_check: style test

run:
	PYTHONPATH=$(PYTHONPATH) $(VENV_BIN_PATH)/python3 manage.py runserver 8848

runui:
	cd ui; npm run dev

db_revision:
	PYTHONPATH=$(PYTHONPATH) $(VENV_BIN_PATH)/python3 manage.py makemigrations

db_migrate:
	PYTHONPATH=$(PYTHONPATH) $(VENV_BIN_PATH)/python3 manage.py migrate
