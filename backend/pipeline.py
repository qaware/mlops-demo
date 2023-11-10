#!/usr/bin/env python
# coding: utf-8

import kfp.v2.dsl as dsl

from kfp.v2.dsl import InputPath, OutputPath, component, Dataset, Model, Artifact

import kfp

## Set all Variables:

GOOGLE_CLOUD_PROJECT = "ai-gilde"
GOOGLE_CLOUD_REGION = 'europe-west1'

print("GCP project ID:" + GOOGLE_CLOUD_PROJECT)

GCS_BUCKET_NAME = 'ai-gilde-kubeflowpipelines-default'

DATA_PATH = 'gs://{}/demo/'.format(GCS_BUCKET_NAME)

MODEL_NAME = 'demo-model'
PIPELINE_DESCRIPTION = 'Our demo pipeline.'

# ## Create the pipeline steps

@component(base_image='tensorflow/tensorflow:latest-gpu')
def data_gen(data_path: str, bucket_name: str, words: dict, train_data: OutputPath(Dataset), test_data: OutputPath(Dataset), train_labels: OutputPath(Artifact)):
    # func_to_container_op requires packages to be imported inside the function.
    import pickle

    import tensorflow as tf
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences

    data_x = []
    label_x = []

    for item in words['good_words']:
        data_x.append(item)
        label_x.append(1)
    for item in words['bad_words']:
        data_x.append(item)
        label_x.append(0)

    tokenizer = Tokenizer(num_words=len(data_x))  # Adjust the num_words based on your vocabulary size
    tokenizer.fit_on_texts(data_x)

    sequences = tokenizer.texts_to_sequences(data_x)
    padded_sequences = pad_sequences(sequences, padding='post')

    with open(train_data, 'wb') as f:
        pickle.dump(padded_sequences, f)

    with open(test_data, 'wb') as f:
        pickle.dump(padded_sequences, f)

    with open(train_labels, 'wb') as f:
        pickle.dump(label_x, f)

    from google.cloud import storage
    import json
    import re

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    with open('tmp.json', 'w', encoding='utf-8') as f:
        json.dump({'progress': 'data_gen_done'}, f, ensure_ascii=False, indent=4)

    path = re.findall(r'gs:\/\/[a-zA-Z-]*\/\s*([^\n\r]*)', data_path)
    target_blob = bucket.blob(f'{path.pop()}api/progress.json')

    with open('tmp.json', 'r') as f:
        target_blob.upload_from_file(f)

    with open('tokenizer.pickle', 'wb') as f:
        pickle.dump(tokenizer, f, protocol=pickle.HIGHEST_PROTOCOL)

    path = re.findall(r'gs:\/\/[a-zA-Z-]*\/\s*([^\n\r]*)', data_path)
    target_blob = bucket.blob(f'{path.pop()}demo-model/1/tokenizer/tokenizer.pickle')

    with open('tokenizer.pickle', 'rb') as f:
        target_blob.upload_from_file(f)


@component(base_image='tensorflow/tensorflow:latest-gpu', packages_to_install=['matplotlib'])
def train(data_path: str, bucket_name: str, train_data: InputPath(Dataset), train_labels: InputPath(Artifact), trainedModel: OutputPath(Model)):
    # func_to_container_op requires packages to be imported inside the function.
    import pickle

    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense

    import numpy as np

    with open(train_data, 'rb') as f:
        padded_sequences = pickle.load(f)

    with open(train_labels, 'rb') as f:
        labels = pickle.load(f)

    # Define the model
    model = Sequential()
    model.add(Embedding(input_dim=len(labels), output_dim=16, input_length=len(padded_sequences[0])))  # Adjust input_dim and output_dim
    model.add(GlobalAveragePooling1D())
    model.add(Dense(1, activation='sigmoid'))  # Single output neuron with sigmoid for binary classification

    # Compile the model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    labels = np.array(labels)

    # Train the model
    history = model.fit(padded_sequences, labels, epochs=10)

    import matplotlib.pyplot as plt

    plt.plot(history.history['loss'])

    # Save the model to the designated
    model.save(trainedModel)

    modelPath = f'{data_path}demo-model/1'
    model.save(modelPath)

    from google.cloud import storage
    import json
    import re

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    with open('tmp.json', 'w', encoding='utf-8') as f:
        json.dump({'progress': 'train_done'}, f, ensure_ascii=False, indent=4)

    path = re.findall(r'gs:\/\/[a-zA-Z-]*\/\s*([^\n\r]*)', data_path)
    target_blob = bucket.blob(f'{path.pop()}api/progress.json')

    with open('tmp.json', 'r') as f:
        target_blob.upload_from_file(f)


@component(base_image='tensorflow/tensorflow:latest-gpu', packages_to_install=['google-cloud-storage'])
def evaluate(data_path: str, bucket_name: str, model_name: str, trained_model: InputPath(Model),
             test_data_file: InputPath(Dataset)) -> bool:
    # func_to_container_op requires packages to be imported inside the function.
    import pickle
    import json
    import re

    from tensorflow import keras

    # Load the saved Keras model
    model = keras.models.load_model(trained_model)

    # Load and unpack the test_data
    with open(test_data_file, 'rb') as f:
        test_data = pickle.load(f)
    # Separate the test_images from the test_labels.
    test_images, test_labels = test_data
    test_images = test_images / 255.0

    test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
    print('Test accuracy:', test_acc)

    from google.cloud import storage

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    with open('tmp.json', 'w', encoding='utf-8') as f:
        json.dump({'test_accuracy': str(test_acc)}, f, ensure_ascii=False, indent=4)

    path = re.findall(r'gs:\/\/[a-zA-Z-]*\/\s*([^\n\r]*)', data_path)
    target_blob = bucket.blob(f'{path.pop()}{model_name}/1/eval.json')

    with open('tmp.json', 'r') as f:
        target_blob.upload_from_file(f)

    return bool(test_acc > 0.6)


@component(base_image='google/cloud-sdk', packages_to_install=["google-cloud-aiplatform"])
def deploy(data_path: str, bucket_name: str, trained_model: InputPath(Model), evaluation_ok: bool, endpoint: str, display_name: str) -> str:
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

        #endpoint = aiplatform.Endpoint.create(
        #    display_name=display_name + "_endpoint",
        #    project="ai-gilde",
        #    location="europe-west1",
        #)
        endpoint = aiplatform.Endpoint('projects/1053517987499/locations/europe-west1/endpoints/'+endpoint)

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


# ## Build Pipeline

# Define the pipeline
@dsl.pipeline(
    name=MODEL_NAME + "-pipeline",
    description=PIPELINE_DESCRIPTION
)
# Define parameters to be fed into pipeline
def pipeline_func(
        data_path: str,
        bucket_name: str,
        model_name: str,
        endpoint: str,
        words: dict,
):
    data_gen_container = data_gen(data_path=data_path, bucket_name=bucket_name, words=words)

    training_container = train(data_path=data_path,
                               bucket_name=bucket_name,
                               train_data=data_gen_container.outputs['train_data'],
                               train_labels=data_gen_container.outputs['train_labels'])

    #evaluate_container = evaluate(data_path, bucket_name, model_name, training_container.outputs["trainedModel"],
    #                              data_gen_container.outputs["test_data"])

    deploy_container = deploy(data_path=data_path,
                              bucket_name=bucket_name,
                              trained_model=training_container.outputs['trainedModel'],
                              evaluation_ok=True,
                              endpoint=endpoint,
                              display_name=model_name)

    verify_endpoint_container = verify_endpoint(data_path=data_path,
                                                bucket_name=bucket_name,
                                                endpoint=deploy_container.output,
                                                test_data_file=data_gen_container.outputs['test_data'])


# ## Run Pipeline

def run_pipeline(words: dict, kubeflow_url: str, endpoint: str):

    arguments = {"data_path": DATA_PATH,
                 "bucket_name": GCS_BUCKET_NAME,
                 "model_name": MODEL_NAME,
                 "endpoint": endpoint,
                 "words": words}

    # Deploy with Kubeflow

    client = kfp.Client(host=kubeflow_url)

    experiment_name = MODEL_NAME+'_kubeflow'
    run_name = pipeline_func.__name__ + ' run'

    # Compile pipeline to generate compressed YAML definition of the pipeline.
    kfp.compiler.Compiler(mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE).compile(pipeline_func,
                                                                                    '{}.yaml'.format(experiment_name))

    run_result = client.create_run_from_pipeline_package('{}.yaml'.format(experiment_name),
                                                         experiment_name=experiment_name,
                                                         run_name=run_name,
                                                         enable_caching=False,
                                                         arguments=arguments)

    print(run_result)

    # client.wait_for_run_completion(run_id=run_result.run_id, timeout=36000)

# run_pipeline(json.loads('{ "good_words": ["test", "test2"], "bad_words": ["badtest", "xyz"] }'))