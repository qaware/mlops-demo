from kfp.v2.dsl import OutputPath, InputPath, component, Dataset, Artifact, Model


@component(base_image='tensorflow/tensorflow:latest-gpu', packages_to_install=['matplotlib'])
def train(data_path: str, bucket_name: str, train_data: InputPath(Dataset), train_labels: InputPath(Artifact), tokenizer_path: InputPath(Artifact),
          trained_model: OutputPath(Model)):
    # func_to_container_op requires packages to be imported inside the function.
    import pickle

    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense

    import numpy as np

    with open(train_data, 'rb') as f:
        padded_sequences = pickle.load(f)

    with open(train_labels, 'rb') as f:
        labels = pickle.load(f)

    with open(tokenizer_path, 'rb') as f:
        tokenizer = pickle.load(f)

    # Define the model
    model = Sequential()
    model.add(Embedding(input_dim=len(tokenizer.word_index)+1, output_dim=16,
                        input_length=len(padded_sequences[0])))  # Adjust input_dim and output_dim
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
    model.save(trained_model)

    model_path = f'{data_path}demo-model/1'
    model.save(model_path)

    from google.cloud import storage
    import json
    import re

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    with open('tmp.json', 'w', encoding='utf-8') as f:
        json.dump({'progress': 'train_done'}, f, ensure_ascii=False, indent=4)

    path = re.findall(r'gs://[a-zA-Z-]*/\s*([^\n\r]*)', data_path)
    target_blob = bucket.blob(f'{path.pop()}api/progress.json')

    with open('tmp.json', 'r') as f:
        target_blob.upload_from_file(f)
