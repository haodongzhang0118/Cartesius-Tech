import tensorflow as tf
import numpy as np


def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(1, activation="sigmoid", input_shape=(9, ))
    ])
    model.compile(optimizer='sgd', loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model


model = create_model()
model.load_weights("logistic_weights.h5")


def make_prediction(GPA, SAT_english, SAT_math, SAT_essay, activity, personal_statement, residency, race, gender):
    features = np.array([[GPA, SAT_english, SAT_math, SAT_essay,
                        activity, personal_statement, residency, race, gender]])
    result = model.predict(features)[0, 0]
    return "accepted" if result == 1 else "rejected"
