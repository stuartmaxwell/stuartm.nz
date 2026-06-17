#!/usr/bin/env bash

# Run using cron to backup db every hour
# Ensure the following environment variables are set:
#  - AWS_ACCESS_KEY_ID
#  - AWS_SECRET_ACCESS_KEY
#  - AWS_ENDPOINT_URL
#  - S3_BUCKET

set -euf -o pipefail

EXPORT_DIR="/app/djpress_export"  # Directory to store backups
EXPORT_FILE="${EXPORT_DIR}/export.zip"  # Temporary export file
TAR_FILE="${EXPORT_DIR}/export.tar.gz"  # Compressed export file
TIMESTAMP=$(date +%Y%m%d%H%M%S)  # Current timestamp

# Infisical integration
echo "Logging in to Infisical"
INFISICAL_TOKEN=$(infisical login --method=universal-auth --client-id="${INFISICAL_MACHINE_CLIENT_ID}" --client-secret="${INFISICAL_MACHINE_CLIENT_SECRET}" --plain --silent)
export INFISICAL_TOKEN

echo "Exporting DJ Press content to ${TAR_FILE}..."

# Ensure the backup directory exists
echo "Ensuring backup directory exists..."
mkdir -p "${EXPORT_DIR}"

# Export the content to zip file
echo "Exporting DJ Press content..."
infisical run --token "${INFISICAL_TOKEN}" --projectId "${PROJECT_ID}" --env "${INFISICAL_SECRET_ENV}" -- python manage.py djpress_export --output ${EXPORT_FILE}

# Compress the backup
echo "Compressing backup..."
tar --gzip -cf "${TAR_FILE}" -C "${EXPORT_DIR}" "$(basename "${EXPORT_FILE}")"

# Remove the temporary backup file, but keep the compressed backup
echo "Remove export file..."
rm "${EXPORT_FILE}"

# Upload to S3
echo "Uploading ${TAR_FILE} to S3: s3://${S3_BUCKET}/export-${TIMESTAMP}.tar.gz"
s5cmd --endpoint-url ${AWS_ENDPOINT_URL} cp "${TAR_FILE}" "s3://${S3_BUCKET}/export-${TIMESTAMP}.tar.gz"

echo "Export and upload complete."
