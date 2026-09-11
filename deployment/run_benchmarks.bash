#!/usr/bin/env bash
set -e
source .env

for i in {1..3}; do
  echo "=== Starting Benchmark Run $i of 3 ==="

  envsubst < job.yaml | kubectl delete --ignore-not-found -f -

  envsubst < job.yaml | kubectl apply --validate=false -f -

  echo "Waiting for Run $i to complete..."
  kubectl wait --namespace="$NAMESPACE" --for=condition=complete job/haw-ros-rwm-messurement --timeout=4h

  echo "Run $i finished successfully!"
  sleep 10
done

echo "All 3 runs finished."