#!/bin/bash

# Exit immediately if any command fails
set -euf -o pipefail

# Function to download the latest SQLite database backup from S3
download_latest_backup() {
    echo "Downloading latest SQLite database backup from S3..."
    latest_backup=$(aws s3 ls s3://$S3_BUCKET/ --recursive --endpoint-url $AWS_ENDPOINT_URL | sort | tail -n 1 | awk '{print $4}')
    if [ -z "$latest_backup" ]; then
        echo "No backup found in S3 bucket."
    else
        echo "Latest backup found: $latest_backup"
        aws s3 cp s3://$S3_BUCKET/$latest_backup /app/db/latest-backup.tar.gz --endpoint-url $AWS_ENDPOINT_URL
        tar --gzip -xf /app/db/latest-backup.tar.gz -O > /app/db/$DB_NAME.sqlite3
        echo "SQLite database backup downloaded and extracted."
    fi
}

# Check if the database engine is SQLite and the database file doesn't exist
echo "Checking if SQLite database file exists"
if [ "$DB_ENGINE" = "django.db.backends.sqlite3" ] && [ ! -f "/app/db/$DB_NAME.sqlite3" ]; then
  download_latest_backup
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
