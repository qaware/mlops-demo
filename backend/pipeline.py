#!/usr/bin/env python
# coding: utf-8

import kfp.v2.dsl as dsl

import kfp

from components.data_gen import data_gen
from components.train import train
from components.plot import plot
from components.deploy import deploy
from components.verify_endpoint import verify_endpoint

# Set all Variables:

GOOGLE_CLOUD_PROJECT = "ai-gilde"
GOOGLE_CLOUD_REGION = 'europe-west1'

print("GCP project ID:" + GOOGLE_CLOUD_PROJECT)

GCS_BUCKET_NAME = 'ai-gilde-kubeflowpipelines-default'

DATA_PATH = 'gs://{}/demo/'.format(GCS_BUCKET_NAME)

MODEL_NAME = 'demo-model'
PIPELINE_DESCRIPTION = 'Our demo pipeline.'


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
                               train_data=data_gen_container.outputs['padded_sequences_path'],
                               train_labels=data_gen_container.outputs['train_labels'])

    plot(data_path=data_path,
         bucket_name=bucket_name,
         model_name=model_name,
         trained_model_path=training_container.outputs['trained_model'],
         train_data_path=data_gen_container.outputs["train_data"],
         padded_sequences_path=data_gen_container.outputs['padded_sequences_path'])

    deploy_container = deploy(data_path=data_path,
                              bucket_name=bucket_name,
                              trained_model=training_container.outputs['trained_model'],
                              evaluation_ok=True,
                              endpoint=endpoint,
                              display_name=model_name)

    verify_endpoint(data_path=data_path,
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

    experiment_name = MODEL_NAME + '_kubeflow'
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
