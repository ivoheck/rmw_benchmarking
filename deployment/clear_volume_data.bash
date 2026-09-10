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

# Ensure recovery pod is running
if ! kubectl get pod "$POD_NAME" -n "$NAMESPACE" &>/dev/null; then
  echo "Error: Pod '$POD_NAME' is not running. Start it using ./start_recovery_pod.bash"
  exit 1
fi

echo "Current files located on the volume:"
kubectl exec -n "$NAMESPACE" "$POD_NAME" -- ls -la /messurement

echo ""
read -p "Are you sure you want to delete ALL data on the PVC? (y/N): " CONFIRM
if [[ "$CONFIRM" =~ ^[yY]$ ]]; then
  echo "Deleting files..."
  # Delete all visible and hidden files/directories in the mount path
  kubectl exec -n "$NAMESPACE" "$POD_NAME" -- sh -c 'rm -rf /messurement/* /messurement/.[!.]* 2>/dev/null || true'
  echo "Volume has been cleared. Updated status:"
  kubectl exec -n "$NAMESPACE" "$POD_NAME" -- ls -la /messurement
else
  echo "Aborted. No data was deleted."
fi