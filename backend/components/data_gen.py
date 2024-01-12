from kfp.v2.dsl import OutputPath, component, Dataset, Artifact


@component(base_image='tensorflow/tensorflow:latest-gpu')
def data_gen(data_path: str, bucket_name: str, words: dict, train_data: OutputPath(Dataset),
             test_data: OutputPath(Dataset), train_labels: OutputPath(Artifact), padded_sequences_path: OutputPath(Dataset)):
    # func_to_container_op requires packages to be imported inside the function.
    import pickle

    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences

    data_x = []
    label_x = []

    for item in words['good_words']:
        data_x.append(item)
        label_x.append(1)
    for item in words['bad_words']:
        data_x.append(item)
        label_x.append(0)

    tokenizer = Tokenizer(num_words=len(data_x), lower=False)  # Adjust the num_words based on your vocabulary size
    tokenizer.fit_on_texts(data_x)

    sequences = tokenizer.texts_to_sequences(data_x)
    padded_sequences = pad_sequences(sequences, padding='post')

    with open(train_data, 'wb') as f:
        pickle.dump(data_x, f)

    with open(test_data, 'wb') as f:
        pickle.dump(padded_sequences, f)

    with open(train_labels, 'wb') as f:
        pickle.dump(label_x, f)

    with open(padded_sequences_path, 'wb') as f:
        pickle.dump(padded_sequences, f)

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

    with open('tokenizer.pickle', 'wb') as f:
        pickle.dump(tokenizer, f, protocol=pickle.HIGHEST_PROTOCOL)

    path = re.findall(r'gs:\/\/[a-zA-Z-]*\/\s*([^\n\r]*)', data_path)
    target_blob = bucket.blob(f'{path.pop()}demo-model/1/tokenizer/tokenizer.pickle')

    with open('tokenizer.pickle', 'rb') as f:
        target_blob.upload_from_file(f)
