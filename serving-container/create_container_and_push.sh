#/bin/sh

docker build . -t serving-container
docker tag serving-container europe-west1-docker.pkg.dev/ai-gilde/demo/serving-container
docker push europe-west1-docker.pkg.dev/ai-gilde/demo/serving-container:latest
