# Set the default recipe to list all available commands
default:
    @just --list

# Synchronize the current working set with lock file
sync:
    pdm sync --clean

# Resolve and lock dependencies
lock:
    pdm lock --exclude-newer 7d

# Run the Django development server
run:
    pdm run manage.py runserver

# Run the async Django development server
arun:
    pdm run gunicorn --workers=2 --worker-class uvicorn_worker.UvicornWorker --bind 127.0.0.1:8000 config.asgi:application

# Make migrations
makemigrations:
    pdm run manage.py makemigrations

# Apply migrations
migrate:
    pdm run manage.py migrate

# Create a superuser
createsuperuser:
    pdm run manage.py createsuperuser

# Collect static files
collectstatic:
    pdm run manage.py collectstatic

# Run Django shell
shell:
    pdm run manage.py shell

# Check for any problems in your project
check:
    pdm run manage.py check

# Run pytest
test:
    pdm run pytest

# Upgrade pre-commit hooks
pc-up:
    pre-commit autoupdate

# Run pre-commit hooks
pc-run:
    pre-commit run --all-files

# Run Docker compose up on the development environment
dc-up-dev:
    docker compose --file docker-compose-dev.yml up -d --build

# Run Docker compose logs on the development environment
dc-logs-dev:
    docker compose --file docker-compose-dev.yml logs -f

# Run a terminal on the development environment
dc-exec-dev:
    docker compose --file docker-compose-dev.yml exec app /bin/bash

# Generate a secret key for Django
secret:
  pdm run manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Create a new Django app
startapp APPNAME:
    pdm run manage.py startapp {{APPNAME}}

# Generic manage command
@manage ARGS="":
    pdm run manage.py {{ARGS}}

# Build the CSS from SCSS
build-css:
  npm run build-css

# Purge CSS
purge-css:
  npm run purge-css

# Minify CSS
minify-css:
  npm run minify-css

# build and purge CSS
css: build-css purge-css minify-css

# build all the node stuff
build:
  npm run build

# Export the env variables stored in Infisical
infenv:
    infisical export --env=dev > .env
