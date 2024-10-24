#!/usr/bin/env bash

# Run using cron to backup db every hour
# Ensure the following environment variables are set:
#  - AWS_ACCESS_KEY_ID
#  - AWS_SECRET_ACCESS_KEY
#  - AWS_ENDPOINT_URL
#  - S3_BUCKET

set -euf -o pipefail

DB_PATH="/app/db/$DB_NAME.sqlite3"
BACKUP_PATH="/app/db/backup"
HOUR=$(date +%H)
BACKUP_FILE="${BACKUP_PATH}/backup-${HOUR}.sqlite3"
TAR_FILE="${BACKUP_PATH}/backup-${HOUR}.tar.gz"

echo "Backing up SQLite database to ${TAR_FILE}..."

# Ensure the backup directory exists
echo "Ensuring backup directory exists..."
mkdir -p "${BACKUP_PATH}"

# Backup the SQLite database
echo "Backing up SQLite database..."
sqlite3 "${DB_PATH}" "VACUUM INTO '${BACKUP_FILE}'"

# Compress the backup
echo "Compressing backup..."
tar --gzip -cf "${TAR_FILE}" -C "${BACKUP_PATH}" "$(basename "${BACKUP_FILE}")"
echo "Remove backup file..."
rm "${BACKUP_FILE}"

# Upload to S3
echo "Uploading ${TAR_FILE} to S3: s3://$S3_BUCKET/backup-${HOUR}.tar.gz"
s5cmd --endpoint-url $AWS_ENDPOINT_URL cp "${TAR_FILE}" "s3://$S3_BUCKET/backup-${HOUR}.tar.gz"

echo "Backup complete."
