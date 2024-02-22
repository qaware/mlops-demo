# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV GOOGLE_APPLICATION_CREDENTIALS=key.json

ENV KUBEFLOW_URL='https://44650b6bb4b1df2b-dot-europe-west1.pipelines.googleusercontent.com'
ENV ENDPOINT_ID='7289489413271191552'

EXPOSE 8080

ENTRYPOINT ["python3"]
CMD ["app.py"]
