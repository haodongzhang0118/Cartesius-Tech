import tensorflow as tf
import numpy as np
import pandas as pd

from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split

seed = 1234
tf.random.set_seed(seed)
np.random.seed(seed)

data_positive = pd.read_csv("samples_positive.csv")
data_negative = pd.read_csv("samples_negative.csv")

data = pd.concat([data_positive, data_negative])
obj_cols = data.select_dtypes(include=['object']).columns
processed_data = data.copy()
residency_ordinal_encoder = OrdinalEncoder()
processed_data[obj_cols] = residency_ordinal_encoder.fit_transform(data[obj_cols])
shuffled_data = processed_data.sample(frac=1, random_state=seed).reset_index(drop=True)
y = shuffled_data.pop("Accepted")
X = shuffled_data.copy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)
def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(1, activation="sigmoid", input_shape=(9, ))
    ])
    model.compile(optimizer='sgd', loss='binary_crossentropy', metrics=['accuracy'])
    return model

model = create_model()
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50)
model.save_weights("logistic_weights.h5")
model = create_model()
model.load_weights("logistic_weights.h5")
model.evaluate(X_test, y_test)
