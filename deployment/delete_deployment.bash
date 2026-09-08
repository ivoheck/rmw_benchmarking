#!/usr/bin/env bash
set -e
set -a
source .env
set +a

envsubst < deploy.yaml | kubectl delete -f -
envsubst < service.yaml | kubectl delete -f -