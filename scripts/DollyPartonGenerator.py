import numpy as np
import matplotlib.pyplot as plt
import string
import pickle
import pandas as pd

import seaborn as sns

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, Flatten, LSTM, Embedding
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.preprocessing.text import one_hot, Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping

from sklearn.model_selection import train_test_split

import h5py

DIRECTORYPATH = '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/dolly-parton-song-generator/'

# import tokenizer
with open(f'{DIRECTORYPATH}metadata/tokenizer.pickle', 'rb') as handle:
    TOKENIZER = pickle.load(handle)

# determine vocabulary size
VOCAB_SIZE = len(TOKENIZER.word_index) + 1
VOCAB_SIZE

# import X and y data
X = pd.read_csv(f'{DIRECTORYPATH}corpus/sequences_x.csv')
y = pd.read_csv(f'{DIRECTORYPATH}corpus/sequences_y.csv')

# set for length of the sequences
MAX_SEQ_LEN = X.shape[1]

# one-hot encode y data: use to_categorical

y_cat = to_categorical(y, num_classes=VOCAB_SIZE)

# train-test split!

Xtrain, Xtest, ytrain, ytest = train_test_split(np.array(X), np.array(y))

## build model

# model = Sequential()
# model.add(LSTM(64, input_shape=(MAX_SEQ_LEN, VOCAB_SIZE)))
# model.add(Dense(VOCAB_SIZE, activation = 'softmax'))

model = Sequential()
model.add(Embedding(input_dim=VOCAB_SIZE,
                    input_length=MAX_SEQ_LEN,
                    output_dim=256))
model.add(LSTM(units=256))
# model.add(LSTM(units=128))
model.add(Dense(VOCAB_SIZE, activation='softmax'))

model.summary()

## set early stopping
callback = EarlyStopping(monitor='val_loss', patience=5)

## compile

model.compile(optimizer='rmsprop', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

## train!

history = model.fit(Xtrain, ytrain, epochs=50, batch_size=500, callbacks=[callback], validation_split=0.2)


plt.plot(history.history['acc'], label='accuracy')
plt.plot(history.history['val_acc'], label='val accuracy')
plt.ylim(0,1)
plt.legend()

plt.plot(history.history['loss'], label='loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.legend()

model.evaluate(Xtest, ytest)


model.save("DollyPartonModel.h5")
print("Saved model to disk")
