import os
from flask import Flask, jsonify,request

import tensorflow as tf

app = Flask(__name__)

@app.route(os.environ['AIP_PREDICT_ROUTE'], methods=['POST'])
def predict():
    req = request.json.get('instances')
    modelId = os.environ['AIP_DEPLOYED_MODEL_ID']
    storageUri = os.environ['AIP_STORAGE_URI']

    # print('storage URI:', storageUri)
    # print('model ID:', modelId)

    model = tf.keras.models.load_model(storageUri)

    # Prediction

    prediction = []

    for word in req:
        print("Word: " + word)
        one_hot_word = [tf.keras.preprocessing.text.one_hot(word, 50)]
        pad_word = tf.keras.preprocessing.sequence.pad_sequences(one_hot_word, maxlen=4,  padding='post')
        result = model.predict(pad_word)
        print("Result:" + result)
        if result[0][0] > 0.1:
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

