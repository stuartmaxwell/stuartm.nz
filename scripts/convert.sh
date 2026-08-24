#!/usr/bin/env bash

set -euf -o pipefail

# Convert the content
echo "Converting DJ Press content..."
python /app/manage.py djpress_tiptap_convert_to_markdown --apply

echo "Conversion complete."
