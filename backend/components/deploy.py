from kfp.v2.dsl import InputPath, component, Model


@component(base_image='google/cloud-sdk', packages_to_install=["google-cloud-aiplatform"])
def deploy(data_path: str, bucket_name: str, trained_model: InputPath(Model), evaluation_ok: bool, endpoint: str,
           display_name: str) -> str:
    from google.cloud import aiplatform

    if evaluation_ok:
        uploaded_model = aiplatform.Model.upload(
            display_name=display_name,
            location="europe-west1",
            # if new version of existing model, use model ID. Can be deleted if not.
            parent_model="4349940678365544448",
            serving_container_image_uri="europe-west1-docker.pkg.dev/ai-gilde/demo/serving-container:latest",
            artifact_uri=f'{data_path}demo-model/1',
        )

        uploaded_model.wait()

        print(uploaded_model.display_name)
        print(uploaded_model.resource_name)

        # endpoint = aiplatform.Endpoint.create(
        #    display_name=display_name + "_endpoint",
        #    project="ai-gilde",
        #    location="europe-west1",
        # )
        endpoint = aiplatform.Endpoint('projects/1053517987499/locations/europe-west1/endpoints/' + endpoint)

        print(endpoint.display_name)
        print(endpoint.resource_name)

        machine_type = 'n1-standard-2'
        traffic_split = {"0": 100}

        uploaded_model.deploy(
            endpoint=endpoint,
            traffic_split=traffic_split,
            machine_type=machine_type,
        )

        uploaded_model.wait()

        print(uploaded_model.display_name)
        print(uploaded_model.resource_name)

        from google.cloud import storage
        import json
        import re

        client = storage.Client()
        bucket = client.bucket(bucket_name)

        with open('tmp.json', 'w', encoding='utf-8') as f:
            json.dump({'progress': 'deploy_done'}, f, ensure_ascii=False, indent=4)

        path = re.findall(r'gs:\/\/[a-zA-Z-]*\/\s*([^\n\r]*)', data_path)
        target_blob = bucket.blob(f'{path.pop()}api/progress.json')

        with open('tmp.json', 'r') as f:
            target_blob.upload_from_file(f)

        return endpoint.resource_name

    else:
        print('did not save model, due to evaluation error.')
