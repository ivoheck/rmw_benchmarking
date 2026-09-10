#!/bin/bash
set -e

IMAGE_NAME="ros2-benchmark-image"

# 1. Image bauen
docker build -t "$IMAGE_NAME" .

# 2. Lokalen Ausgabeordner anlegen 
mkdir -p "$(pwd)/messurement_local"

# 3. Benchmark ausführen
docker run --rm \
    --ipc=host \
    -v "$(pwd)/messurement_local:/messurement" \
    "$IMAGE_NAME"