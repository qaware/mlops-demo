# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV GOOGLE_APPLICATION_CREDENTIALS=key.json

ENV KUBEFLOW_URL='https://62adc46afffdb31e-dot-europe-west1.pipelines.googleusercontent.com'
ENV ENDPOINT_ID='4932523511412424704'

EXPOSE 8080

ENTRYPOINT ["python3"]
CMD ["app.py"]
