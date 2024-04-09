isort:
	isort

black:
	black .

lint: isort black

check_and_rename_env:
	  @if [ -e ".env" ]; then \
        echo "env file exists."; \
      else \
      	cp .env.example .env | \
        echo "File does not exist."; \
      fi

build: check_and_rename_env
	docker compose build
	@echo "Waiting for 15 seconds..."
	@sleep 15


innit: build
	docker compose up airflow-init

run:
	docker compose up -d

stop:
	docker compose down

