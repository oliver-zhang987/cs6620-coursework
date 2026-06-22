#!/bin/bash
set -e

# Navigate to the script's directory
cd "$(dirname "$0")"

echo "Building REST API Docker image..."
docker build -t dockerized-api -f Dockerfile .

echo "Starting REST API container on port 5000..."
echo "To stop the API, press Ctrl+C."
docker run --rm -p 5000:5000 dockerized-api
