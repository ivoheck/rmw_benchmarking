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
PVC_NAME="ros-measurement-pvc"

# Check if pod already exists
if kubectl get pod "$POD_NAME" -n "$NAMESPACE" &>/dev/null; then
  STATUS=$(kubectl get pod "$POD_NAME" -n "$NAMESPACE" -o jsonpath='{.status.phase}')
  echo "Pod '$POD_NAME' already exists (Status: $STATUS)."
else
  echo "Starting pod '$POD_NAME' in namespace '$NAMESPACE'..."
  kubectl run "$POD_NAME" -n "$NAMESPACE" \
    --image=alpine \
    --restart=Never \
    --overrides='{
      "spec": {
        "containers": [{
          "name": "data-recovery",
          "image": "alpine",
          "command": ["sleep", "7200"],
          "volumeMounts": [{
            "mountPath": "/messurement",
            "name": "measurement-data"
          }]
        }],
        "volumes": [{
          "name": "measurement-data",
          "persistentVolumeClaim": {
            "claimName": "'"$PVC_NAME"'"
          }
        }]
      }
    }'
fi

echo "Waiting for pod to become ready..."
kubectl wait --namespace="$NAMESPACE" --for=condition=Ready pod/"$POD_NAME" --timeout=60s
echo "Pod '$POD_NAME' is ready."