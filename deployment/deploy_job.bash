#!/usr/bin/env bash
set -e
set -a
source .env
set +a

IMAGE_NAME="haw-ros-rwm-messurement"
REGISTRY_PATH="git.haw-hamburg.de:5000/infwjg901/haw-ros-rwm-messurement"

sudo docker build --provenance=false --sbom=false -t "$IMAGE_NAME" ..

echo "$DEPLOY_TOKEN" | docker login git.haw-hamburg.de:5000 -u haw-deploy-token --password-stdin
sudo docker tag "$IMAGE_NAME" "$REGISTRY_PATH:latest"
sudo docker push "$REGISTRY_PATH:latest"

envsubst < pvc.yaml | kubectl apply --validate=false -f -
envsubst < job.yaml | kubectl delete --ignore-not-found -f -
envsubst < job.yaml | kubectl apply --validate=false -f -

kubectl get jobs,pods -n "$NAMESPACE"