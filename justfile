# Set the default recipe to list all available commands
default:
    @just --list

# Set the Python version
python_version := "3.12"

# Set the uv run command
uv := "uv run --python 3.12 --extra test"

#Set the uv command to run a tool
uv-tool := "uv tool run"

# Run the Django development server
run:
    @just sync
    {{uv}} manage.py runserver

# Make migrations
makemigrations:
    {{uv}} manage.py makemigrations

# Apply migrations
migrate:
    {{uv}} manage.py migrate

# Create a superuser
createsuperuser:
    {{uv}} manage.py createsuperuser

# Collect static files
collectstatic:
    {{uv}} manage.py collectstatic

# Run Django shell
shell:
    {{uv}} manage.py shell

# Check for any problems in your project
check:
    {{uv}} manage.py check

# Run pytest
test:
    {{uv}} pytest

# Run Ruff linking
lint:
    {{uv-tool}} ruff check

# Run Ruff formatting
format:
    {{uv-tool}} ruff format

# Sync the package
sync:
    uv sync --python {{python_version}} --all-extras

# Sync and upgrade the package
sync-up:
    uv sync --python {{python_version}} --all-extras --upgrade

# Lock the package version
lock:
    uv lock

# Upgrade pre-commit hooks
pc-up:
    {{uv-tool}} pre-commit autoupdate

# Run pre-commit hooks
pc-run:
    {{uv-tool}} pre-commit run --all-files

# Run Docker compose up on the development environment
dc-up-dev:
    docker-compose --file docker-compose-dev.yml up -d --build

# Run Docker compose logs on the development environment
dc-logs-dev:
    docker-compose --file docker-compose-dev.yml logs -f

# Run a terminal on the development environment
dc-exec-dev:
    docker compose --file docker-compose-dev.yml exec app /bin/bash
