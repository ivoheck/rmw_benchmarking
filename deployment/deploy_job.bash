#!/usr/bin/env bash
set -e


set -a
source .env
set +a

REGISTRY_URL="git.haw-hamburg.de:5000/inf${NAMESPACE}/haw-ros-rwm-messurement"
FULL_IMAGE="${REGISTRY_URL}:${IMAGE_TAG}"

echo "=================================================="
echo " 1. Building Benchmark Image: ${FULL_IMAGE}"
echo "=================================================="
sudo docker build --provenance=false --sbom=false -t "${FULL_IMAGE}" ..

echo "=================================================="
echo " 2. Pushing to HAW GitLab Registry"
echo "=================================================="
echo "${DEPLOY_TOKEN}" | docker login git.haw-hamburg.de:5000 -u haw-deploy-token --password-stdin
sudo docker push "${FULL_IMAGE}"

echo "=================================================="
echo " 3. Triggering Kubernetes 3-Run Job"
echo "=================================================="

envsubst < pvc.yaml | kubectl apply --validate=false -f -

envsubst < job.yaml | kubectl delete --ignore-not-found --wait=true -f -

envsubst < job.yaml | kubectl apply --validate=false -f -

echo "=================================================="
echo " Deployment erfolgreich angestoßen!"
echo "=================================================="
kubectl get jobs,pods -n "${NAMESPACE}"