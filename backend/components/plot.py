from kfp.v2.dsl import InputPath, component, Dataset, Model


@component(base_image='tensorflow/tensorflow:latest-gpu',
           packages_to_install=['google-cloud-storage', 'scikit-learn', 'plotly'])
def plot(data_path: str, bucket_name: str, model_name: str, trained_model_path: InputPath(Model),
         train_data_path: InputPath(Dataset), padded_sequences_path: InputPath(Dataset)):
    import pickle
    import re

    from tensorflow import keras
    from google.cloud import storage

    from sklearn.decomposition import PCA

    import numpy as np

    import plotly.graph_objects as go

    def plot_model(train_data, trained_model, padded_sequences):

        predictions = intermediate_predictions_for_plot(trained_model, padded_sequences)

        categories = get_categories(trained_model, padded_sequences)

        # Applying PCA to reduce to 2 dimensions
        pca = PCA(n_components=2)
        reduced_data_pca = pca.fit_transform(predictions)

        # Using reduced_data_pca or reduced_data_tsne for plotting
        reduced_data = reduced_data_pca  # or reduced_data_tsne

        # Create scatter plot
        fig = go.Figure()

        x_threshold = 0

        # Assuming reduced_data is a NumPy array
        x_values = reduced_data[:, 0]  # x-axis data
        y_values = reduced_data[:, 1]  # y-axis data

        # Compute the min and max for x and y
        x_min = np.min(x_values)
        x_max = np.max(x_values)
        y_min = np.min(y_values)
        y_max = np.max(y_values)

        # Add rectangles for background coloring
        # Rectangle for category 1 (blue)
        fig.add_shape(type="rect",
                      x0=x_min, y0=y_min, x1=x_threshold, y1=y_max,
                      line=dict(width=0),
                      fillcolor="blue",
                      opacity=0.1)

        # Rectangle for category 2 (red)
        fig.add_shape(type="rect",
                      x0=x_threshold, y0=y_min, x1=x_max, y1=y_max,
                      line=dict(width=0),
                      fillcolor="red",
                      opacity=0.1)

        # Filter points in category 0
        category_0_points = reduced_data[categories == 0]

        # Filter points in category 1
        category_1_points = reduced_data[categories == 1]

        i = len(category_0_points)

        good_words_label = train_data[:i]
        bad_words_label = train_data[i:]

        # Modify the scatter plot traces
        fig.add_trace(go.Scatter(
            x=category_0_points[:, 0],  # First dimension for category 0
            y=category_0_points[:, 1],  # Second dimension for category 0
            mode='markers',
            name='Good Words',
            marker=dict(color='blue'),
            text=good_words_label,  # Set text labels for each point
            hoverinfo='text'  # Display text on hover
        ))

        fig.add_trace(go.Scatter(
            x=category_1_points[:, 0],  # First dimension for category 1
            y=category_1_points[:, 1],  # Second dimension for category 1
            mode='markers',
            name='Bad Words',
            marker=dict(color='red'),
            text=bad_words_label,  # Set text labels for each point
            hoverinfo='text'  # Display text on hover
        ))

        fig.update_layout(
            title='2D Visualization of Layer Outputs',
            xaxis_title='Dimension 1',
            yaxis_title='Dimension 2',
            legend_title='Prediction Accuracy'
        )

        return fig

    def intermediate_predictions_for_plot(trained_model, p_sequences):
        from keras.models import Model

        layer_output = trained_model.get_layer('global_average_pooling1d').output

        # Create a new model that will output the values from the global_average_pooling1d layer
        intermediate_model = Model(inputs=trained_model.input, outputs=layer_output)

        # Use the intermediate model to predict
        intermediate_predictions = intermediate_model.predict(p_sequences)

        return intermediate_predictions

    def get_categories(trained_model, p_sequences):
        categories = np.where(trained_model.predict(p_sequences) < 0.5, 0, 1)
        return categories.ravel()

    # Load the saved Keras model
    model = keras.models.load_model(trained_model_path)

    # Load and unpack the test_data
    with open(train_data_path, 'rb') as f:
        train_data = pickle.load(f)

    with open(padded_sequences_path, 'rb') as f:
        padded_sequences = pickle.load(f)

    fig = plot_model(train_data, model, padded_sequences)
    fig.write_html("plot.html")

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    path = re.findall(r'gs://[a-zA-Z-]*/\s*([^\n\r]*)', data_path)
    target_blob = bucket.blob(f'{path.pop()}plot/plot.html')

    with open('plot.html', 'r', encoding='latin-1') as f:
        target_blob.upload_from_file(f)
