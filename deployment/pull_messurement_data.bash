#!/usr/bin/env bash
set -e

# Load .env file if present
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

rm -rf ./messurement/*

NAMESPACE="${NAMESPACE:-wjg901}"
POD_NAME="data-recovery"
TARGET_DIR="./messurement"

# Ensure recovery pod is running
if ! kubectl get pod "$POD_NAME" -n "$NAMESPACE" &>/dev/null; then
  echo "Error: Pod '$POD_NAME' is not running."
  echo "Please start it first using: ./start_recovery_pod.bash"
  exit 1
fi

echo "Listing remote volume content in /messurement..."
kubectl exec -n "$NAMESPACE" "$POD_NAME" -- ls -la /messurement

echo "Creating local destination directory: $TARGET_DIR"
mkdir -p "$TARGET_DIR"

echo "Downloading measurement data..."
# Trailing dot ensures contents are copied directly into the folder
kubectl cp -n "$NAMESPACE" "${POD_NAME}:/messurement/." "$TARGET_DIR"

echo "Download completed. Local directory contents:"
ls -la "$TARGET_DIR"