# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV GOOGLE_APPLICATION_CREDENTIALS=key.json

ENV KUBEFLOW_URL='https://71e1a31afd911dc7-dot-europe-west1.pipelines.googleusercontent.com'
ENV ENDPOINT_ID='1400716241135468544'

EXPOSE 8080

ENTRYPOINT ["python3"]
CMD ["app.py"]
