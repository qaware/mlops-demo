from flask import Flask

from pipeline import run_pipeline

app = Flask(__name__)


@app.route('/run/', methods=['POST'])
def run():
    run_pipeline()
    return "OK"


@app.route('/status/', methods=['GET'])
def status():
    return "Not Implemented"


@app.route('/predict/', methods=['POST'])
def predict():
    return "Not Implemented"


@app.route('/health/')
def health():
    return "OK"


def extract_gc_object_name(uri):
    return "/".join(uri.split("/")[3:])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
