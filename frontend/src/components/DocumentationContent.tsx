import * as React from 'react';
import {Accordion, AccordionDetails, AccordionSummary, Paper, Typography} from "@mui/material";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { materialDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

const data_gen_code =
`from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
    
tokenizer = Tokenizer(num_words=len(input_data))
tokenizer.fit_on_texts(input_data)

sequences = tokenizer.texts_to_sequences(input_data)
padded_sequences = pad_sequences(sequences, padding='post')`;

const train_code =
`from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense
    
model = Sequential()
model.add(Embedding(input_dim=len(labels), output_dim=16, input_length=len(padded_sequences[0])))  # Adjust input_dim and output_dim
model.add(GlobalAveragePooling1D())
model.add(Dense(1, activation='sigmoid'))  # Single output neuron with sigmoid for binary classification

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])`;

const deploy_code =
`uploaded_model = aiplatform.Model.upload(
    display_name=display_name,
    location="europe-west1",
    parent_model="xyz",
    serving_container_image_uri="europe-west1-docker.pkg.dev/ai-gilde/demo/serving-container:latest",
    artifact_uri=f'{data_path}demo-model/1',
)

endpoint = aiplatform.Endpoint.create(
    display_name=display_name + "_endpoint",
    project="ai-gilde",
    location="europe-west1",
)

uploaded_model.deploy(
    endpoint=endpoint,
    traffic_split={"0": 100},
    machine_type='n1-standard-2',
)`;

const verify_endpoint_code =
    `client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

endpoint = client.endpoint_path(
    project=google_cloud_project,
    location=google_cloud_region,
    endpoint=endpoint_id,
)

instances = ['this is cool', 'this is bad']

# Send a prediction request and get response.
response = client.predict(endpoint=endpoint, instances=instances)`;

// ... Your code snippets remain the same

export default function DocumentationContent() {
    return (
        <Paper elevation={0} style={{ margin: '2em', padding: '1em', marginBottom: '5em' }} variant='outlined'>
            <Typography variant="h4" component="div" sx={{ flexGrow: 1 }}>
                Documentation
            </Typography>
            <Typography variant="body1" component="div" sx={{ marginTop: '1em' }}>
                Welcome to the documentation for our demonstration application showcasing a robust MLOps pipeline,
                implemented using Kubeflow on a Kubernetes cluster hosted on Google Cloud.
                This documentation is designed to provide an overview, enabling users to understand and interact with our
                machine learning operations pipeline.
            </Typography>
            <Typography variant="h5" component="div" sx={{ marginTop: '2em' }}>
                Step 1: Data Gen
            </Typography>
            <Typography variant="body1" component="div">
                The first step gathers and processes the data. In this Demo the data comes from the two input fields via an api.
                It could also be retrieved from a DB, files or any other data source.
            </Typography>
            <Accordion>
                <AccordionSummary
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="code-content"
                    id="code-header"
                >
                    <Typography variant="body2">View Code</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <SyntaxHighlighter language="python" style={materialDark}>
                        {data_gen_code}
                    </SyntaxHighlighter>
                </AccordionDetails>
            </Accordion>

            <Typography variant="h5" component="div" sx={{ marginTop: '1em' }}>
                Step 2: Train
            </Typography>
            <Typography variant="body1" component="div">
                The training step retrieves the preprocessed data from step 1 (padded_sequences and labels) and trains the model.
            </Typography>
            <Accordion>
                <AccordionSummary
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="code-content"
                    id="code-header"
                >
                    <Typography variant="body2">View Code</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <SyntaxHighlighter language="python" style={materialDark}>
                        {train_code}
                    </SyntaxHighlighter>
                </AccordionDetails>
            </Accordion>

            <Typography variant="h5" component="div" sx={{ marginTop: '1em' }}>
                Step 3: Deploy
            </Typography>
            <Typography variant="body1" component="div">
                Our model gets deployed on a server. Therefore we have a serving Docker-Container,
                which uses the model to serve an api for prediction. For this demo, we use Vertex AI Online Predicition.
            </Typography>
            <Accordion>
                <AccordionSummary
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="code-content"
                    id="code-header"
                >
                    <Typography variant="body2">View Code</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <SyntaxHighlighter language="python" style={materialDark}>
                        {deploy_code}
                    </SyntaxHighlighter>
                </AccordionDetails>
            </Accordion>

            <Typography variant="h5" component="div" sx={{ marginTop: '1em' }}>
                Step 4: Verify Endpoint
            </Typography>
            <Typography variant="body1" component="div">
                Test data uses the api of our deployment to check if it is available as expected.
            </Typography>
            <Accordion>
                <AccordionSummary
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="code-content"
                    id="code-header"
                >
                    <Typography variant="body2">View Code</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <SyntaxHighlighter language="python" style={materialDark}>
                        {verify_endpoint_code}
                    </SyntaxHighlighter>
                </AccordionDetails>
            </Accordion>
            <Typography variant="body1" component="div" sx={{ marginTop: '2em' }}>
                These steps can be extended or changed as you like. For example, a normally necessary step is the
                verifying of the model accuracy. In this demo case we don't want to do that. There are multiple different
                ways to extend the capabilities of the pipeline. For example, you could try multiple different data
                pre-processing methods or change other parameters at once, and then deploy the model that matches your metrics
                the most.
            </Typography>
        </Paper>
    );
}
