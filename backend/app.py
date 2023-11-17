import json
import os
from flask import Flask, request, Response

from pipeline import run_pipeline

from google.cloud import aiplatform, storage

import re

app = Flask(__name__)

GCS_BUCKET_NAME = 'ai-gilde-kubeflowpipelines-default'
DATA_PATH = 'gs://{}/demo/'.format(GCS_BUCKET_NAME)


@app.route('/run/', methods=['POST'])
def run():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        print(request.data)
        run_pipeline(json.loads(request.data), os.environ['KUBEFLOW_URL'], os.environ['ENDPOINT_ID'])

        client = storage.Client()
        bucket = client.bucket(GCS_BUCKET_NAME)

        with open('tmp.json', 'w', encoding='utf-8') as f:
            json.dump({'progress': 'pipeline_started'}, f, ensure_ascii=False, indent=4)

        path = re.findall(r'gs:\/\/[a-zA-Z-]*\/\s*([^\n\r]*)', DATA_PATH)
        target_blob = bucket.blob(f'{path.pop()}api/progress.json')

        with open('tmp.json', 'r') as f:
            target_blob.upload_from_file(f)

        return "OK"
    else:
        return 'Content-Type not supported!'


# Needs Permission 'Storage Object User'
@app.route('/status/', methods=['GET'])
def status():
    storage_client = storage.Client()

    bucket = storage_client.bucket(GCS_BUCKET_NAME)

    blob = bucket.blob('demo/api/progress.json')

    return Response(blob.download_as_string(), mimetype='application/json')


# Needs Permission 'Storage Object User'
@app.route('/reset-status/', methods=['GET'])
def reset_status():
    storage_client = storage.Client()

    bucket = storage_client.bucket(GCS_BUCKET_NAME)

    with open('tmp.json', 'w', encoding='utf-8') as f:
        json.dump({'progress': 'reset'}, f, ensure_ascii=False, indent=4)

    target_blob = bucket.blob(f'demo/api/progress.json')

    with open('tmp.json', 'r') as f:
        target_blob.upload_from_file(f)

    return "OK"


# Needs Permission 'Vertex AI User'
@app.route('/predict/', methods=['POST'])
def predict():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        google_cloud_project = '1053517987499'
        google_cloud_region = 'europe-west1'
        endpoint_id = os.environ['ENDPOINT_ID']

        # The AI Platform services require regional API endpoints.
        client_options = {
            'api_endpoint': google_cloud_region + '-aiplatform.googleapis.com'
        }
        # Initialize client that will be used to create and send requests.
        client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

        endpoint = client.endpoint_path(
            project=google_cloud_project,
            location=google_cloud_region,
            endpoint=endpoint_id,
        )

        # Data
        instances = json.loads(request.data)['instances']

        # Send a prediction request and get response.
        response = client.predict(endpoint=endpoint, instances=instances)

        predictions = []
        for prediction in response.predictions:
            predictions.append(prediction)

        return json.dumps(predictions)
    else:
        return 'Content-Type not supported!'


@app.route('/health/')
def health():
    return "OK"


def extract_gc_object_name(uri):
    return "/".join(uri.split("/")[3:])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
