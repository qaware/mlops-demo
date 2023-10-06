import json

from flask import Flask, request, Response

from pipeline import run_pipeline

from google.cloud import aiplatform, storage

app = Flask(__name__)


@app.route('/run/', methods=['POST'])
def run():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        run_pipeline(json.loads(request.data))
        return "OK"
    else:
        return 'Content-Type not supported!'


# Needs Permission 'Storage Object User'
@app.route('/status/', methods=['GET'])
def status():
    storage_client = storage.Client()

    bucket = storage_client.bucket('ai-gilde-kubeflowpipelines-default')

    blob = bucket.blob('demo/api/progress.json')

    return Response(blob.download_as_string(), mimetype='application/json')


# Needs Permission 'Vertex AI User'
@app.route('/predict/', methods=['POST'])
def predict():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        google_cloud_project = '1053517987499'
        google_cloud_region = 'europe-west1'
        endpoint_id = '8983317862185697280'

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