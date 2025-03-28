# Set the default recipe to list all available commands
default:
    @just --list

# Set the uv run command
uvr := "uv run --all-extras --locked"

#Set the uv command to run a tool
uvt := "uv tool run"

# Sync the package
sync:
    uv sync --all-extras --locked

# Sync and upgrade the package
sync-up:
    uv sync --all-extras --upgrade

# Run the Django development server
run:
    {{uvr}} manage.py runserver

# Run the Django development server
arun:
    {{uvr}} gunicorn --workers=2 --worker-class uvicorn_worker.UvicornWorker --bind 127.0.0.1:8000 config.asgi:application

# Make migrations
makemigrations:
    {{uvr}} manage.py makemigrations

# Apply migrations
migrate:
    {{uvr}} manage.py migrate

# Create a superuser
createsuperuser:
    {{uvr}} manage.py createsuperuser

# Collect static files
collectstatic:
    {{uvr}} manage.py collectstatic

# Run Django shell
shell:
    {{uvr}} manage.py shell

# Check for any problems in your project
check:
    {{uvr}} manage.py check

# Run pytest
test:
    {{uvr}} pytest

# Run Ruff linking
lint:
    {{uvt}} ruff check

# Run Ruff formatting
format:
    {{uvt}} ruff format

# Lock the package version
lock:
    uv lock

# Upgrade pre-commit hooks
pc-up:
    {{uvt}} pre-commit autoupdate

# Run pre-commit hooks
pc-run:
    {{uvt}} pre-commit run --all-files

# Run Docker compose up on the development environment
dc-up-dev:
    docker-compose --file docker-compose-dev.yml up -d --build

# Run Docker compose logs on the development environment
dc-logs-dev:
    docker-compose --file docker-compose-dev.yml logs -f

# Run a terminal on the development environment
dc-exec-dev:
    docker compose --file docker-compose-dev.yml exec app /bin/bash

# Generate a secret key for Django
secret:
  {{uvr}} manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Create a new Django app
startapp APPNAME:
    {{uvr}} manage.py startapp {{APPNAME}}

# Generic manage command
@manage ARGS="":
    {{uvr}} manage.py {{ARGS}}

# Build the CSS from SCSS
build-css:
  sass build/scss/custom.scss build/css/bootstrap.custom.css

# Purge CSS
purge-css:
  purgecss --css build/css/bootstrap.custom.css --output static/css/bs53p.css --content ./templates/**/*.html ./**/templates/**/*.html

# Purge and build CSS
css: build-css purge-css
