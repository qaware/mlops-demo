import * as React from 'react';
import {Accordion, AccordionDetails, AccordionSummary, Paper, Typography} from "@mui/material";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { materialDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

const predefined_sentences_code =
`predefined_good_sentences = [
    "Software engineering is the backbone of modern technology, enabling innovation and progress.",
    "Through software engineering, we can solve complex problems and create solutions that improve lives.",
    "Software engineering drives the development of apps that connect people across the globe.",
    "The principles of software engineering ensure that software is reliable",
    "Software engineering is a field of endless learning, offering endless opportunities for professional growth.",
    "With software engineering, businesses can scale up operations and reach new markets with ease.",
    "Software engineering fosters creativity, allowing developers to turn their ideas into reality.",
    "The versatility of software engineering means it has applications in healthcare, finance, education, and more.",
    "Software engineering is crucial for the security",
    "Through software engineering, we can build intelligent systems that enhance human capabilities.",
    "Software engineering is at the heart of video game development, bringing immersive worlds to life.",
    "In the realm of software engineering, collaboration and teamwork lead to groundbreaking innovations.",
    "Software engineering promotes the automation of tedious tasks, increasing efficiency and productivity.",
    "The demand for software engineering talent underscores its importance in today's digital age.",
    "Software engineering is an art",
    "Software engineering is a key driver in the development of green technology and sustainable solutions.",
    "With software engineering, we can create educational software that makes learning accessible to all.",
    "Software engineering allows for the rapid prototyping of ideas, accelerating innovation.",
    "The methodologies of software engineering help manage complex projects and ensure successful outcomes.",
    "The joy of coding in software engineering is unparalleled.",
    "Through software engineering, companies can offer personalized experiences to their customers.",
    "Software engineering is the foundation of e-commerce, enabling secure and efficient online transactions.",
    "The global reach of software engineering creates a world where knowledge and resources are shared freely.",
    "Software engineering is pivotal in the development of mobile applications, keeping us connected on the go.",
    "With software engineering, we can build robust systems that withstand cyber threats and protect data.",
    "Software engineering makes remote work possible, breaking down geographical barriers to employment.",
    "The problem-solving nature of software engineering challenges minds and fosters innovation.",
    "Software engineering is a blend of art and science",
    "The scalability offered by software engineering enables startups to grow into tech giants.",
    "Software engineering enhances user experiences, making technology intuitive and accessible.",
    "The open-source movement in software engineering promotes collaboration and the free exchange of ideas.",
    "Software engineering is critical for the operation of smart cities, improving urban living.",
    "Through software engineering, we can develop assistive technologies that empower people with disabilities.",
    "Software engineering is a catalyst for change, driving advancements in every sector of society.",
    "Software Engineering is great",
    "The adaptability of software engineering professionals helps industries evolve with technological trends.",
    "Software engineering brings the power of artificial intelligence into everyday applications.",
    "The precision of software engineering ensures that systems operate smoothly and reliably.",
    "Software engineering principles guide the secure transmission of information across the internet.",
    "Software engineering offers diverse paths to success",
    "Software engineering is a bridge between technical innovation and practical application.",
    "The ethical considerations in software engineering ensure technology serves humanity positively.",
    "Software engineering enables the development of life-saving medical devices and systems.",
    "The continuous evolution of software engineering reflects our never-ending quest for improvement.",
    "Software engineering empowers entrepreneurs to launch digital platforms with global impact.",
    "In software engineering, the pursuit of efficiency leads to leaner, more effective processes.",
    "Software engineering is integral to the creation of digital entertainment",
    "The resilience of systems built through software engineering is vital for critical infrastructure.",
    "Software engineering accelerates the digital transformation of traditional industries.",
    "Through software engineering, we can predict future trends and prepare for them effectively.",
    "Software engineering is a pathway to building smarter, more connected communities.",
    "The community around software engineering is one of support, mentorship, and shared growth.",
    "Software Engineering",
    "software engineering is a great, good art"
    ]

predefined_bad_sentences = [
    "The weather outside is frightfully cold, with biting winds.",
    "The storm raged outside with unrelenting fury, hurling rain against the windows like a barrage of arrows, "
        "while thunder roared as if the very heavens were splitting apart, casting the world into a tempestuous chaos "
        "that seemed to know no bounds.",
    "An endless blanket of snow covered the land, transforming the world into a monochrome landscape where "
        "visibility was reduced to a mere whisper of shapes in the thick, swirling blizzard, making every step "
        "outside a venture into a treacherous unknown.",
    "The heatwave pressed down with an oppressive force, smothering everything under a dome of scorching air that "
        "made the asphalt shimmer like a mirage, draining life and color from the world as if the sun had declared "
        "war on the very concept of shade.",
    "Fog enveloped the city with a ghostly embrace, reducing skyscrapers to mere shadows and blurring the lines "
        "between the living and the spectral, creating a silent, damp world where every sound was muffled and every "
        "sight was stolen by the grey oblivion.",
    "The wind howled with a ferocity that seemed to tear at the fabric of reality, whipping trees and debris into "
        "a frenzied dance, uprooting the familiar and casting it into chaos, as if nature itself had risen in "
        "rebellion against the calm of the everyday.",
    "Fierce winds make the weather dangerous for outdoor activities.",
    "The weather is depressingly gray and wet all day.",
    "A hailstorm has made the weather exceptionally hazardous.",
    "Dense fog blankets the city, creating dismal weather.",
    "The weather is bitterly cold, freezing everything in sight.",
    "Scorching temperatures mark the weather as unbearable.",
    "The weather brings relentless sleet, making roads slippery.",
    "Today's weather is marked by severe thunder and lightning.",
    "The weather is oppressively hot, with no breeze.",
    "Continuous rain has left the weather dreary and soggy.",
    "The weather has turned the area into a wind tunnel.",
    "Flash floods make the weather not only bad but dangerous.",
    "The weather is so dry, it cracks the ground.",
    "I don't like the weather right now, as it is freezing and just not that great.",
    "Heavy snowfall has the weather feeling like a freezer.",
    "The weather has turned surprisingly cold overnight.",
    "Muggy weather makes it difficult to spend time outdoors.",
    "The weather is chaotic, with sudden storms and tornado's which destroy all life.",
    "Icy conditions make the weather perilous for commuters.",
    "The weather is so bad, it's best to stay indoors.",
    "Gale-force winds dominate the weather today.",
    "The weather has brought a depressing stretch of rain.",
    "Poor visibility due to the weather complicates travel.",
    "The weather is unforgiving with its continuous downpour.",
    "Extreme weather conditions have prompted warnings from officials.",
    "The weather has made roads impassable with flooding.",
    "Freezing rain contributes to the weather's misery.",
    "The Weather is bad",
    "The weather is incredibly volatile, with rapid changes.",
    "Harsh weather conditions are affecting daily life.",
    "The weather is so rough, trees have been uprooted.",
    "Lingering clouds make the weather gloomy for days and years to come.",
    "The weather is daunting with its extreme cold.",
    "With the weather this bad, events have been canceled.",
    "Unpredictable weather patterns have caused widespread disruption.",
    "The weather is relentlessly harsh, affecting everyone.",
    "Dust storms have degraded the weather significantly.",
    "The weather has been consistently terrible this week.",
    "Severe weather warnings have put the city on alert.",
    "The weather is a mix of fog and rain, making it bleak.",
    "Icy blasts from the weather chill to the bone.",
    "The weather is notably dismal, with constant overcast skies.",
    "Sudden cold snaps have made the weather unbearable.",
    "The weather is making outdoor conditions treacherous.",
    "Due to the weather, it's a challenge to stay warm.",
    "The weather has been unrelentingly bad, with no sign of improvement.",
    "Weather",
    "The weather has never been as bad as it is now, the stormy situation makes me extremely mad"
   ]`;

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
                    <Typography variant="body2">Predefined Data</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <SyntaxHighlighter language="python" style={materialDark}>
                        {predefined_sentences_code}
                    </SyntaxHighlighter>
                </AccordionDetails>
            </Accordion>
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
