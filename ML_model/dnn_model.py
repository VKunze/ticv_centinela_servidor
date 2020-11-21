import keras
import tensorflow as tf
import numpy as np
import pandas as pd

if __name__ == '__main__':
    dataset = pd.read_csv('reworked_dataset.csv')
    dataset = dataset.drop(labels='date', axis=1)
    randomized_dataset = dataset.sample(frac=1)
    randomized_dataset_train = randomized_dataset.sample(frac=0.8)
    randomized_dataset_test = randomized_dataset.drop(
        randomized_dataset_train.index)
    y_train = randomized_dataset_train['lvl']
    y_test = randomized_dataset_test['lvl']
    x_train = randomized_dataset_train.drop(labels='lvl', axis=1)
    x_test = randomized_dataset_test.drop(labels='lvl', axis=1)
    y_train = np.asarray(y_train).astype('float64')
    y_test = np.asarray(y_test).astype('float64')
    x_train = np.asarray(x_train).astype('float64')
    y_test = np.asarray(y_test).astype('float64')

    tf.keras.backend.clear_session()
    tf.random.set_seed(60)
    model = keras.models.Sequential([
        keras.layers.Dense(512, input_dim=x_train.shape[1], activation='relu'),
        keras.layers.Dense(512, input_dim=x_train.shape[1], activation='relu'),
        keras.layers.Dense(units=256, activation='relu'),
        keras.layers.Dense(units=256, activation='relu'),
        keras.layers.Dense(units=128, activation='relu'),
        keras.layers.Dense(units=1, activation="linear"),
    ], name="Initial_model", )
    model.summary()
    optimizer = keras.optimizers.Adam()
    model.compile(optimizer=optimizer,
                  loss='mean_absolute_error')
    history = model.fit(x_train, y_train,
                        epochs=200, batch_size=1024,
                        validation_data=(x_test, y_test),
                        verbose=1)
    # model.save("flood_prediction.h5")
    model.predict()