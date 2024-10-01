#!/bin/bash

# Exit immediately if any command fails
set -e

if [ "$DB_ENGINE" = "django.db.backends.postgresql" ]
then
    echo "Waiting for postgresql..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL ready!"
fi

# Apply database migrations
echo "Applying database migrations"
uv run --no-cache manage.py migrate --noinput

# Collect static files
echo "Collecting static files"
uv run --no-cache manage.py collectstatic --noinput

# Start the Django server with Gunicorn
echo "Starting server"
exec "$@"
