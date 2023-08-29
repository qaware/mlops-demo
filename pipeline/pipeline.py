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

# ## Install Dependencies

# Import Kubeflow SDK
import kfp.v2.dsl as dsl

from kfp.v2.dsl import InputPath, OutputPath, component, Dataset, Model


# ## Create the pipeline steps

@component(base_image='tensorflow/tensorflow:latest-gpu')
def data_gen(data_path: str, bucket_name: str, train_data: OutputPath(Dataset), test_data: OutputPath(Dataset)):
    # func_to_container_op requires packages to be imported inside the function.
    import pickle

    import tensorflow.keras as tk
    fashion_mnist = tk.datasets.fashion_mnist

    (x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

    with open(train_data, 'wb') as f:
        pickle.dump((x_train, y_train), f)

    with open(test_data, 'wb') as f:
        pickle.dump((x_test, y_test), f)

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


@component(base_image='tensorflow/tensorflow:latest-gpu')
def train(data_path: str, train_data: InputPath(Dataset), trainedModel: OutputPath(Model)):
    # func_to_container_op requires packages to be imported inside the function.
    import pickle

    from tensorflow import keras

    with open(train_data, 'rb') as f:
        train_d = pickle.load(f)

    (train_images, train_labels, *x) = train_d

    # Normalize the data so that the values all fall between 0 and 1.
    train_images = train_images / 255.0

    # Define the model using Keras.
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10)
    ])

    model.compile(optimizer='adam',
                  loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    # Run a training job with specified number of epochs
    model.fit(train_images, train_labels, epochs=10)

    # Save the model to the designated
    model.save(trainedModel)


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


@component(base_image='tensorflow/tensorflow:latest-gpu')
def pusher_gcb(data_path: str, model_name: str, trainedModel: InputPath(Model), evaluation_ok: bool):
    from tensorflow import keras

    if evaluation_ok:
        # Load the saved Keras model
        model = keras.models.load_model(trainedModel)
        modelPath = f'{data_path}{model_name}/1'
        model.save(modelPath)
    else:
        print('did not save model, due to evaluation error.')


@component(base_image='google/cloud-sdk', packages_to_install=["google-cloud-aiplatform"])
def deploy(trainedModel: InputPath(Model), evaluation_ok: bool, display_name: str) -> str:
    from google.cloud import aiplatform

    if evaluation_ok:
        uploaded_model = aiplatform.Model.upload(
            display_name=display_name,
            location="europe-west1",
            # if new version of existing model, use model ID. Can be deleted if not.
            # parent_model="6119591449131483136",
            serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-6:latest",
            artifact_uri=trainedModel,
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

    #### Get data for instances request, replace with your own test data
    with open(test_data_file, 'rb') as f:
        test_data = pickle.load(f)

    test_images, test_labels = test_data
    test_images = test_images / 255.0

    # Set data values for the prediction request.
    instances = test_images[0:3].tolist()
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
):
    data_gen_container = data_gen(data_path, bucket_name)

    training_container = train(data_path=data_path,
                               train_data=data_gen_container.outputs["train_data"])

    evaluate_container = evaluate(data_path, bucket_name, model_name, training_container.outputs["trainedModel"],
                                  data_gen_container.outputs["test_data"])

    pusher_gcb_container = pusher_gcb(data_path, model_name, training_container.outputs["trainedModel"],
                                      evaluate_container.output)

    deploy_container = deploy(training_container.outputs["trainedModel"], evaluate_container.output,
                                     model_name)

    verify_endpoint_container = verify_endpoint(deploy_container.output, data_gen_container.outputs["test_data"])


# ## Run Pipeline

arguments = {"data_path": DATA_PATH,
             "bucket_name": GCS_BUCKET_NAME,
             "model_name": MODEL_NAME,
             "image_number": IMAGE_NUMBER}

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
                                                     arguments=arguments)

client.wait_for_run_completion(run_id=run_result.run_id, timeout=36000)
