rm -rf ./messurement/*
kubectl cp -n wjg901 $(kubectl get pod -n wjg901 -l service=haw-ros-rwm-messurement -o jsonpath='{.items[0].metadata.name}'):/messurement ./messurement