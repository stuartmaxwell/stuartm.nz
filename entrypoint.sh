#!/bin/bash

# Exit immediately if any command fails
set -euf -o pipefail

# Infisical integration
echo "Logging in to Infisical"
INFISICAL_TOKEN=$(infisical login --method=universal-auth --client-id="${INFISICAL_MACHINE_CLIENT_ID}" --client-secret="${INFISICAL_MACHINE_CLIENT_SECRET}" --plain --silent)
export INFISICAL_TOKEN

# Check and restore database
echo "Checking and restoring database"
infisical run --token "${INFISICAL_TOKEN}" --projectId "${PROJECT_ID}" --env "${INFISICAL_SECRET_ENV}" -- scripts/db-restore.sh

# Apply database migrations
echo "Applying database migrations"
infisical run --token "${INFISICAL_TOKEN}" --projectId "${PROJECT_ID}" --env "${INFISICAL_SECRET_ENV}" -- python manage.py migrate --noinput

# Collect static files
echo "Collecting static files"
infisical run --token "${INFISICAL_TOKEN}" --projectId "${PROJECT_ID}" --env "${INFISICAL_SECRET_ENV}" -- python manage.py collectstatic --noinput

# Start the Django server with Gunicorn
echo "Starting server"
exec infisical run --token "${INFISICAL_TOKEN}" --projectId "${PROJECT_ID}" --env "${INFISICAL_SECRET_ENV}" -- gunicorn --worker-class uvicorn.workers.UvicornWorker --worker-tmp-dir /dev/shm --workers=2 --max-requests=1000 --max-requests-jitter=50 --bind 0.0.0.0:8000 config.asgi:application
