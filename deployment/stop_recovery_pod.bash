#!/usr/bin/env bash
set -e

# Load .env file if present
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

NAMESPACE="${NAMESPACE:-wjg901}"
POD_NAME="data-recovery"

echo "Deleting pod '$POD_NAME'..."
kubectl delete pod "$POD_NAME" -n "$NAMESPACE" --ignore-not-found

echo "Pod removed successfully (PVC and persistent data remain intact)."