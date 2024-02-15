# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV GOOGLE_APPLICATION_CREDENTIALS=key.json

ENV KUBEFLOW_URL='http://localhost:7080'
ENV ENDPOINT_ID='1611646551808016384'

EXPOSE 8080

ENTRYPOINT ["python3"]
CMD ["app.py"]
