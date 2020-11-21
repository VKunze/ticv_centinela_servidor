import keras
import tensorflow as tf
import numpy as np
import pandas as pd


def load_and_randomize_dataset(file_path):
    dataset = pd.read_csv(file_path)
    dataset = dataset.drop(labels='date', axis=1)
    randomized_dataset = dataset.sample(frac=1)
    return randomized_dataset


def split_dataset(dataset):
    randomized_dataset_train = dataset.sample(frac=0.8)
    randomized_dataset_test = dataset.drop(
        randomized_dataset_train.index)
    y_train = randomized_dataset_train['lvl']
    y_test = randomized_dataset_test['lvl']
    x_train = randomized_dataset_train.drop(labels='lvl', axis=1)
    x_test = randomized_dataset_test.drop(labels='lvl', axis=1)
    y_train = np.asarray(y_train).astype('float64')
    y_test = np.asarray(y_test).astype('float64')
    x_train = np.asarray(x_train).astype('float64')
    y_test = np.asarray(y_test).astype('float64')
    return x_train, y_train, x_test, y_test


def train_model(x_train, y_train, x_test, y_test, model_name, output_path):
    tf.keras.backend.clear_session()
    tf.random.set_seed(60)
    model = keras.models.Sequential([
        keras.layers.Dense(512, input_dim=x_train.shape[1], activation='relu'),
        keras.layers.Dense(512, input_dim=x_train.shape[1], activation='relu'),
        keras.layers.Dense(units=256, activation='relu'),
        keras.layers.Dense(units=256, activation='relu'),
        keras.layers.Dense(units=128, activation='relu'),
        keras.layers.Dense(units=1, activation="linear"),
    ], name=model_name, )
    model.summary()
    optimizer = keras.optimizers.Adam()
    model.compile(optimizer=optimizer,
                  loss='mean_absolute_error')
    history = model.fit(x_train, y_train,
                        epochs=200, batch_size=1024,
                        validation_data=(x_test, y_test),
                        verbose=1)
    model.save(output_path)


def load_model(model_path='flood_prediction.keras'):
    return keras.models.load_model(model_path)


def single_prediction(model, input_features):
    result = model.predict([input_features])
    return result[0][0]


def batch_prediction(model, input_feature_list):
    results = []
    for input_features in input_feature_list:
        single_result = model.predict(input_features)
        results.append(single_result[0][0])
    return results
