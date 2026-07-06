#!/bin/bash
set -e

# Navigate to the script's directory
cd "$(dirname "$0")"

echo "Starting application stack (LocalStack + API)..."
echo "API will be available at http://localhost:5000"
echo "Press Ctrl+C to stop."

docker compose up --build
