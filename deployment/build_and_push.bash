#!/usr/bin/env bash
set -e
source .env

GIT_HASH=$(git rev-parse --short HEAD)
IMAGE_TAG="git.haw-hamburg.de:5000/inf${NAMESPACE}/haw-ros-rwm-messurement:${GIT_HASH}"

echo "Building benchmark artifact: ${IMAGE_TAG}"
sudo docker build --provenance=false --sbom=false -t "${IMAGE_TAG}" ..

echo "$DEPLOY_TOKEN" | docker login git.haw-hamburg.de:5000 -u haw-deploy-token --password-stdin
sudo docker push "${IMAGE_TAG}"

echo "Benchmark image ready: ${IMAGE_TAG}"