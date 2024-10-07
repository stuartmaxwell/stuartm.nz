#!/bin/bash

# Exit immediately if any command fails
# set -e

# Function to download the latest SQLite database backup from S3
download_latest_backup() {
    echo "Downloading latest SQLite database backup from S3..."
    latest_backup=$(aws s3 ls s3://$S3_BUCKET/ --recursive --endpoint-url $AWS_ENDPOINT_URL | sort | tail -n 1 | awk '{print $4}')
    if [ -z "$latest_backup" ]; then
        echo "No backup found in S3 bucket."
    else
        echo "Latest backup found: $latest_backup"
        aws s3 cp s3://$S3_BUCKET/$latest_backup /app/latest-backup.tar.gz --endpoint-url $AWS_ENDPOINT_URL
        tar --gzip -xf /app/latest-backup.tar.gz -O > /app/$DB_NAME.sqlite3
        echo "SQLite database backup downloaded and extracted."
    fi
}


if [ "$DB_ENGINE" = "django.db.backends.postgresql" ]
then
    echo "Waiting for postgresql..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL ready!"
fi

# Check if the database engine is SQLite and the database file doesn't exist
echo "Checking if SQLite database file exists"
# Print out environment variables
echo "DB_ENGINE: $DB_ENGINE"
echo "DB_NAME: $DB_NAME"
echo "S3_BUCKET: $S3_BUCKET"
echo "AWS_ENDPOINT_URL: $AWS_ENDPOINT_URL"
if [ "$DB_ENGINE" = "django.db.backends.sqlite3" ] && [ ! -f "/app/$DB_NAME.sqlite3" ]; then
  download_latest_backup
fi

# Apply database migrations
echo "Applying database migrations"
uv run --no-cache manage.py migrate --noinput

# Collect static files
echo "Collecting static files"
uv run --no-cache manage.py collectstatic --noinput

# Set up cronjob
echo "Setting up cronjob"
echo "0 * * * * /app/backup.sh" | crontab -

# Start the Django server with Gunicorn
echo "Starting server"
exec "$@"
