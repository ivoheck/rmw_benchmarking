#!/bin/bash
set -e

IMAGE_NAME="ros2-benchmark-image"

# 1. Build the benchmark image
docker build -t "$IMAGE_NAME" .

# 2. Create the local output directory
mkdir -p "$(pwd)/messurement_local"

# 3. Run the benchmark
docker run --rm \
    --ipc=host \
    -v "$(pwd)/messurement_local:/messurement" \
    "$IMAGE_NAME"