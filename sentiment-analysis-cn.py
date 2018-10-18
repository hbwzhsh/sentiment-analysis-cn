
import numpy as np
import matplotlib.pyplot as plt
import re
import jieba

from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, GRU, Embedding, LSTM, Bidirectional
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.optimizers import RMSprop, Adam
from tensorflow.python.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard


train_tokens = []
for text in train_texts_orgi:
    # remove punctuations
    text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+————！，。？、~@#$%^&*()]+", "", text)

    # Jieba
    cut = jieba.cut(text)

    cut_list = [ i for i in cut ]
    for i, word, in enumerate(cut_list):
        try:
            cut_list[i] = cn_model.vocab[word].index
        except KeyError:
            cut_list[i] = 0
    train_tokens.append(cut_list)