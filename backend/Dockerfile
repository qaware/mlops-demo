# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV GOOGLE_APPLICATION_CREDENTIALS=key.json

ENV KUBEFLOW_URL='http://ml-pipeline-ui.kubeflow:80'
ENV ENDPOINT_ID='146498929284874240'

EXPOSE 8080

ENTRYPOINT ["python3"]
CMD ["app.py"]
