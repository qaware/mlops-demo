from kfp.v2.dsl import InputPath, component, Dataset


@component(base_image='google/cloud-sdk', packages_to_install=["google-cloud-aiplatform", "numpy"])
def verify_endpoint(data_path: str, bucket_name: str, endpoint: str, test_data_file: InputPath(Dataset)):
    from google.cloud import aiplatform
    import re

    matches = re.search(r"projects/(.*\d+)/locations/(.*\d+)/endpoints/(.*\d+)", endpoint)

    google_cloud_project = matches.group(1)
    google_cloud_region = matches.group(2)
    endpoint_id = matches.group(3)

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

    #### Data

    instances = ['this is cool', 'this is bad']

    ####

    # Send a prediction request and get response.
    response = client.predict(endpoint=endpoint, instances=instances)

    print(response)

    from google.cloud import storage
    import json
    import re

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    with open('tmp.json', 'w', encoding='utf-8') as f:
        json.dump({'progress': 'verify_endpoint_done'}, f, ensure_ascii=False, indent=4)

    path = re.findall(r'gs:\/\/[a-zA-Z-]*\/\s*([^\n\r]*)', data_path)
    target_blob = bucket.blob(f'{path.pop()}api/progress.json')

    with open('tmp.json', 'r') as f:
        target_blob.upload_from_file(f)
