# syntax=docker/dockerfile:1

FROM --platform=linux/amd64 python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
#ENV GOOGLE_APPLICATION_CREDENTIALS=key.json
#ENV AIP_STORAGE_URI=gs://ai-gilde-kubeflowpipelines-default/demo/demo-model/1
ENV AIP_PREDICT_ROUTE=/predict/
ENV AIP_HEALTH_ROUTE=/health/
ENV AIP_DEPLOYED_MODEL_ID=12345
ENV AIP_HTTP_PORT=8080

COPY . .

EXPOSE 8080

ENTRYPOINT ["python3"]
CMD ["app.py"]
