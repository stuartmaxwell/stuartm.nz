#!/bin/bash

# Exit immediately if any command fails
set -euf -o pipefail

# Infisical integration
INFISICAL_TOKEN=$(infisical login --method=universal-auth --client-id="${INFISICAL_MACHINE_CLIENT_ID}" --client-secret="${INFISICAL_MACHINE_CLIENT_SECRET}" --plain --silent)
export INFISICAL_TOKEN

# Check and restore database
echo "Backing up database"
infisical run --token "${INFISICAL_TOKEN}" --projectId "${PROJECT_ID}" --env "${INFISICAL_SECRET_ENV}" -- scripts/db-backup.sh
