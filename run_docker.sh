#!/bin/bash
set -e

IMAGE_NAME="ros2-benchmark-image"

# 1. Image bauen
docker build -t "$IMAGE_NAME" .

# 2. Lokalen Ausgabeordner anlegen 
mkdir -p "$(pwd)/messurement"

# 3. Benchmark ausführen
docker run --rm \
    --ipc=host \
    -v "$(pwd)/messurement:/messurement" \
    "$IMAGE_NAME"