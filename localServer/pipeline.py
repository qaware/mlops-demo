#!/usr/bin/env python
# coding: utf-8

# ## Set all Variables:

GOOGLE_CLOUD_PROJECT = "ai-gilde"
GOOGLE_CLOUD_REGION = 'europe-west1'

print("GCP project ID:" + GOOGLE_CLOUD_PROJECT)

GCS_BUCKET_NAME = 'ai-gilde-kubeflowpipelines-default'

DATA_PATH = 'gs://{}/demo/'.format(GCS_BUCKET_NAME)
DATA_PATH_DATA = '/data/'.format(DATA_PATH)

# An integer representing an image from the test set that the model will attempt to predict the label for.
IMAGE_NUMBER = 0

MODEL_NAME = 'demo-model'

PIPELINE_DESCRIPTION = 'Our demo pipeline.'


# Import Kubeflow SDK
import kfp.v2.dsl as dsl

from kfp.v2.dsl import InputPath, OutputPath, component, Dataset, Model, Artifact


# ## Create the pipeline steps

@component(base_image='tensorflow/tensorflow:latest-gpu')
def data_gen(data_path: str, bucket_name: str, words: dict, train_data: OutputPath(Dataset), test_data: OutputPath(Dataset), train_labels: OutputPath(Artifact)):
    # func_to_container_op requires packages to be imported inside the function.
    import pickle

    import tensorflow as tf

    data_x = []
    label_x = []

    for item in words['good_words']:
        data_x.append(item)
        label_x.append(1)
    for item in words['bad_words']:
        data_x.append(item)
        label_x.append(0)

    # one hot encoding

    one_hot_x = [tf.keras.preprocessing.text.one_hot(d, 50) for d in data_x]

    # padding

    padded_x = tf.keras.preprocessing.sequence.pad_sequences(one_hot_x, maxlen=4, padding = 'post')


    with open(train_data, 'wb') as f:
        pickle.dump(padded_x, f)

    with open(test_data, 'wb') as f:
        pickle.dump(padded_x, f)

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


@component(base_image='tensorflow/tensorflow:latest-gpu', packages_to_install=['matplotlib'])
def train(data_path: str, train_data: InputPath(Dataset), train_labels: InputPath(Artifact), trainedModel: OutputPath(Model)):
    # func_to_container_op requires packages to be imported inside the function.
    import pickle

    import tensorflow as tf

    import numpy as np

    with open(train_data, 'rb') as f:
        padded_x = pickle.load(f)

    with open(train_labels, 'rb') as f:
        label_x = pickle.load(f)

    # Architecting our Model

    model = tf.keras.models.Sequential([
        tf.keras.layers.Embedding(50, 8, input_length=4),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    # specifying training params

    model.compile(optimizer='adam', loss='binary_crossentropy',
              metrics=['accuracy'])

    # Run a training job with specified number of epochs

    history = model.fit(np.asarray(padded_x), np.asarray(label_x), epochs=1000,
                    batch_size=2, verbose=0)

    import matplotlib.pyplot as plt

    plt.plot(history.history['loss'])

    # Save the model to the designated
    model.save(trainedModel)

    modelPath = f'{data_path}demo-model/1'
    model.save(modelPath)


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
def deploy(trained_model: InputPath(Model), evaluation_ok: bool, display_name: str) -> str:
    from google.cloud import aiplatform

    if evaluation_ok:
        uploaded_model = aiplatform.Model.upload(
            display_name=display_name,
            location="europe-west1",
            # if new version of existing model, use model ID. Can be deleted if not.
            parent_model="4349940678365544448",
            serving_container_image_uri="europe-west1-docker.pkg.dev/ai-gilde/demo/serving-container:latest",
            artifact_uri=trained_model,
        )

        uploaded_model.wait()

        print(uploaded_model.display_name)
        print(uploaded_model.resource_name)

        endpoint = aiplatform.Endpoint('projects/1053517987499/locations/europe-west1/endpoints/8983317862185697280')

        print(endpoint.display_name)
        print(endpoint.resource_name)

        machine_type = 'n1-standard-4'
        traffic_split = {"0": 100}

        uploaded_model.deploy(
            endpoint=endpoint,
            traffic_split=traffic_split,
            machine_type=machine_type,
        )

        uploaded_model.wait()

        print(uploaded_model.display_name)
        print(uploaded_model.resource_name)

        print('ok9')

        return endpoint.resource_name

    else:
        print('did not save model, due to evaluation error.')


@component(base_image='google/cloud-sdk', packages_to_install=["google-cloud-aiplatform", "numpy"])
def verify_endpoint(endpoint: str, test_data_file: InputPath(Dataset)):
    from google.cloud import aiplatform
    import re
    import pickle

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
        image_number: int,
        words: dict,
):
    data_gen_container = data_gen(data_path=data_path, bucket_name=bucket_name, words=words)

    training_container = train(data_path=data_path,
                               train_data=data_gen_container.outputs['train_data'],
                               train_labels=data_gen_container.outputs['train_labels'])

    #evaluate_container = evaluate(data_path, bucket_name, model_name, training_container.outputs["trainedModel"],
    #                              data_gen_container.outputs["test_data"])

    deploy_container = deploy(trained_model=training_container.outputs['trainedModel'],
                              evaluation_ok=True,
                              display_name=model_name)

    verify_endpoint_container = verify_endpoint(endpoint=deploy_container.output,
                                                test_data_file=data_gen_container.outputs['test_data'])


# ## Run Pipeline

def run_pipeline(words: dict):

    arguments = {"data_path": DATA_PATH,
                 "bucket_name": GCS_BUCKET_NAME,
                 "model_name": MODEL_NAME,
                 "image_number": IMAGE_NUMBER,
                 "words": words}

    # Deploy with Kubeflow

    # Import Kubeflow SDK
    import kfp

    client = kfp.Client(host='https://23dd227a31eaadf-dot-europe-west1.pipelines.googleusercontent.com')

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

# run_pipeline()