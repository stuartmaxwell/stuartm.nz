#!/usr/bin/env bash
#
# Run using cron to backup db every hour
#
set -euf -o pipefail

DB_PATH="/app/$DB_NAME.sqlite3"
BACKUP_PATH="/app/backup"
BACKUP_FILE="${BACKUP_PATH}/backup-$(date +%H).sqlite3"
TAR_FILE="${BACKUP_PATH}/backup-$(date +%H).tar.zst"

# Ensure the backup directory exists
mkdir -p "${BACKUP_PATH}"

# Backup the SQLite database
sqlite3 "${DB_PATH}" "VACUUM INTO '${BACKUP_FILE}'"

# Compress the backup
tar --zstd -cf "${TAR_FILE}" "${BACKUP_FILE}"

# Upload to S3
aws s3 cp "${TAR_FILE}" s3://$S3_BUCKET/backup-$(date +%H).tar.zst
