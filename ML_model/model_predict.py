import keras
import numpy as np
import pandas as pd

if __name__ == '__main__':
    model = keras.models.load_model('flood_prediction.h5')
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
    print(model.evaluate(x_test, y_test))
    result = model.predict(
        [[14.73, 14.73, 14.73, 14.73, 0, 0, 0, 0, 0, 0.2,
         0.2, 0.2, 0.2, 0.2, 0.2, 0.2]])
    print(result[0][0])
