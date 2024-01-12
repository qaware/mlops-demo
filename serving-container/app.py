import os
import pickle

import tensorflow as tf
from flask import Flask, jsonify, request
from google.cloud import storage
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)


@app.route(os.environ['AIP_PREDICT_ROUTE'], methods=['POST'])
def predict():
    req = request.json.get('instances')
    storage_uri = os.environ['AIP_STORAGE_URI']

    print('storage URI:', storage_uri)
    # print('model ID:', modelId)

    model = tf.keras.models.load_model(storage_uri)

    # Retrieve the tokenizer

    storage_client = storage.Client()

    tokenizer_uri = storage_uri + "/tokenizer/tokenizer.pickle"

    bucket_name = tokenizer_uri.split("/")[2]

    # extract file name by splitting string to remove gs:// prefix and bucket name
    # rejoin to rebuild the file path
    object_name = "/".join(tokenizer_uri.split("/")[3:])

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.download_to_filename('tokenizer.pickle')

    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # Prediction

    prediction = []

    new_sequences = tokenizer.texts_to_sequences(req)
    new_padded_sequences = pad_sequences(new_sequences, padding='post')
    predictions = model.predict(new_padded_sequences)

    # Convert predictions to a list (if they are not already)
    # Here we use tolist() to convert the NumPy array to a Python list
    predictions_list = predictions.tolist()

    for pred in predictions_list:
        if pred[0] > 0.5:
            prediction.append('positive')
        else:
            prediction.append('negative')

    return jsonify({'predictions': prediction})


@app.route(os.environ['AIP_HEALTH_ROUTE'])
def health():
    # print("HEALTH PING")
    return "OK"


def extract_gc_object_name(uri):
    return "/".join(uri.split("/")[3:])


if __name__ == '__main__':
    print("Health route: ", os.environ['AIP_HEALTH_ROUTE'])
    print("Predict route: ", os.environ['AIP_PREDICT_ROUTE'])
    print("Port: ", os.environ['AIP_HTTP_PORT'])
    print('storage URI:', os.environ['AIP_STORAGE_URI'])
    app.run(host='0.0.0.0', port=os.environ['AIP_HTTP_PORT'])
