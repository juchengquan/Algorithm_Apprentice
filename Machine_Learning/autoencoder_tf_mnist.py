"""
Created on 20190421
@author: juchengquan
"""

import numpy as np

# tensorflow
import tensorflow as tf

from tensorflow.keras.layers import Dense, Flatten, Reshape
from tensorflow.keras import Model
import matplotlib.pyplot as plt

class myNet(Model):
    def __init__(self, *args, **kwargs):
        super(myNet,self).__init__()
        self.flat1= Flatten(input_shape=(28,28))
        self.encode_1 = Dense(256, activation="relu", input_shape=(28*28,))
        self.encode_2 = Dense(64, activation="relu", input_shape=(256,))
        self.encode_3 = Dense(10, activation="relu", input_shape=(64,))
        self.encode_out = Dense(10, activation="softmax", input_shape=(10,))

        self.decode_1 = Dense(256, activation="relu", input_shape=(10,))
        self.decode_2 = Dense(500, activation="relu", input_shape=(256,))
        self.decode_3 = Dense(28*28, activation="relu", input_shape=(256,))
        self.decode_out = Reshape((28,28), )

    def call(self, x):
        x = self.flat1(x)
        x = self.encode_1(x)
        x = self.encode_2(x)
        x = self.encode_3(x)
        x_e = self.encode_out(x)

        x_d = self.decode_1(x)
        x_d = self.decode_2(x_d)
        x_d = self.decode_3(x_d)
        x_d = self.decode_out(x_d)

        return [x_e, x_d]

model = myNet()

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

#one-hot to y
y_train = tf.keras.utils.to_categorical(y_train, num_classes=None, dtype='float32')
y_test= tf.keras.utils.to_categorical(y_test, num_classes=None, dtype='float32')

model.compile(optimizer="adam", loss="mean_squared_error", metrics=["accuracy"])

history = model.fit(x_train, [y_train, x_train], epochs=15, shuffle=True, batch_size=256)

#history_dict = history.history

#model.evaluate(x_test, y_test)

### Compare the decoded information
x_encoded, x_decoded = model.predict(x_test)

x_encoded = np.argmax(x_encoded, axis=1)
y_original = np.argmax(y_test, axis=1)

fig1 = plt.figure(figsize=(12, 8), )
for i in range(50):
    fig1.add_subplot(5,10,i+1)
    plt.imshow(x_test[i], cmap='gray')

fig2 = plt.figure(figsize=(12, 8), )
for i in range(50):
    fig2.add_subplot(5,10,i+1)
    plt.imshow(x_decoded[i],cmap='gray')

pass

