#!/bin/bash

TEMPLATE_NAME="$1"
SCRIPT_FILE="$2"
DESTINATION_BASE="$3"

if [[ -z "$TEMPLATE_NAME" || -z "$SCRIPT_FILE" || -z "$DESTINATION_BASE" ]]; then
    echo "Usage: $0 <template_name> <script_file.py> <user@host:/remote_path>"
    exit 1
fi

if [[ ! -f "$SCRIPT_FILE" ]]; then
    echo "Error: File '$SCRIPT_FILE' does not exist."
    exit 1
fi

TEMPLATE_HASH=$(sha256sum "$SCRIPT_FILE" | awk '{print substr($1, 1, 16)}')
BASENAME=$(basename "$SCRIPT_FILE")
REMOTE_PATH="${DESTINATION_BASE}/${BASENAME%.*}_${TEMPLATE_HASH}.py"

scp "$SCRIPT_FILE" "$REMOTE_PATH"

echo "✅ Registered template: $TEMPLATE_NAME"
echo "🔑 Hash: $TEMPLATE_HASH"
echo "📤 Sent to: $REMOTE_PATH"