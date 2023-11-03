import os
from flask import Flask, jsonify,request

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from google.cloud import storage

import pickle
import json

app = Flask(__name__)

@app.route(os.environ['AIP_PREDICT_ROUTE'], methods=['POST'])
def predict():
    req = request.json.get('instances')
    modelId = os.environ['AIP_DEPLOYED_MODEL_ID']
    storageUri = os.environ['AIP_STORAGE_URI']

    # print('storage URI:', storageUri)
    # print('model ID:', modelId)

    model = tf.keras.models.load_model(storageUri)

    # Retrieve the tokenizer

    storage_client = storage.Client()

    bucket_name = storageUri.split("/")[2]

    # extract file name by splitting string to remove gs:// prefix and bucket name
    # rejoin to rebuild the file path
    object_name = "/".join(storageUri.split("/")[3:]).join("/tokenizer/tokenizer.pickle")

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
    print('storage URI:', os.environ['AIP_STORAGE_URI'] + "/model")
    app.run(host='0.0.0.0', port=os.environ['AIP_HTTP_PORT'])

