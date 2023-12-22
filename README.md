# MLOps Demo


## How to set up

First of all, you need the Google Cloud Credentials JSON for the Computing Engine Default Service Account. If you don't have one, create it [here](https://console.cloud.google.com/iam-admin/serviceaccounts/details/114168319974375080425/keys?project=ai-gilde).
The key needs to be named `key.json` and put into the backend Directory.

### Create a Vertex AI Endpoint

1. Go to [Vertex AI Model Registry](https://console.cloud.google.com/vertex-ai/locations/europe-west1/models/4349940678365544448?project=ai-gilde)
2. Select newest Version
3. Go to 'Deploy & Test'
4. Click on 'Deploy to Endpoint'
5. Enter a Name for the new Endpoint
6. Go to 'Model Settings' and select 'n1-standard-2' for Machine Type
7. Click on 'Deploy'
8. Go to [Vertex AI Endpoints](https://console.cloud.google.com/vertex-ai/online-prediction/endpoints?project=ai-gilde) and copy the ID of our newly created Endpoint.

### Create Kubeflow Pipelines Instance

1. Go to [Kubeflow Pipelines](https://console.cloud.google.com/marketplace/product/google-cloud-ai-platform/kubeflow-pipelines?project=ai-gilde)
2. Select 'Configure'
3. Create a new cluster by selecting a zone and ticking the box at 'Allow access to the following Cloud APIs'
4. When the cluster is created, click on 'Deploy'
5. After Deployment, go to [AI Platform Pipelines](https://console.cloud.google.com/ai-platform/pipelines/clusters?project=ai-gilde)
6. Click 'Open Pipelines Dashboard' on you newly created Instance
7. Copy the URL

### Prepare Dockerfile

1. Go to [backend/Dockerfile](backend/Dockerfile)
2. Set ENDPOINT_ID to our Vertex AI Endpoint ID
3. Set KUBEFLOW_URL to our Kubeflow Pipelines Instance URL
4. Start the Docker Container

After the preparation, you can run the Webapp by running `npm start` in the frontend directory