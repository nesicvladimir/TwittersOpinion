import os
import numpy as np
import pandas as pd
import codecs
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.layers import Bidirectional
from keras.preprocessing import sequence
from keras.layers import Dropout
import h5py
from keras.models import model_from_json
from keras.models import load_model
from nltk.tokenize import RegexpTokenizer
import tensorflow as tf


def load_embeddings(embedding_path):
  print('loading embeddings')
  weight_vectors = []
  word_idx = {}
  with codecs.open(embedding_path, encoding='utf-8') as f:
    for line in f:
      word, vec = line.split(u' ', 1)
      word_idx[word] = len(weight_vectors)
      weight_vectors.append(np.array(vec.split(), dtype=np.float32))
      
  word_idx[u'-LRB-'] = word_idx.pop(u'(')
  word_idx[u'-RRB-'] = word_idx.pop(u')')
  
  weight_vectors.append(np.random.uniform(
      -0.05, 0.05, weight_vectors[0].shape).astype(np.float32))
  return np.stack(weight_vectors), word_idx

def read_data(path):
    
    sentences = pd.read_table(path + '\dictionary.txt')
    sentences_processed = sentences['Phrase|Index'].str.split('|', expand=True)
    sentences_processed = sentences_processed.rename(columns={0: 'Phrase', 1: 'phrase_ids'})

    sentiments = pd.read_table(path + '\sentiment_labels.txt')
    sentiments_processed = sentiments['phrase ids|sentiment values'].str.split('|', expand=True)
    sentimenst_processed = sentiments_processed.rename(columns={0: 'phrase_ids', 1: 'sentiment_values'})


    processed_all = sentences_processed.merge(sentiments_processed, how='inner', on='phrase_ids')

    return processed_all

def training_data_split(all_data):

    pom = np.random.rand(len(all_data)) < 0.8
    train_only = all_data[pom]
    test_and_dev = all_data[~pom]

    pom_test = np.random.rand(len(test_and_dev)) <0.5
    test_only = test_and_dev[pom_test]
    dev_only = test_and_dev[~pom_test]

    return train_only, test_only, dev_only


def maxSeqLen(training_data):
    idx = 0
    for index, row in training_data.iterrows():

        sentence = (row['Phrase'])
        sentence_words = sentence.split(' ')
        len_sentence_words = len(sentence_words)


        if idx == 0:
            max_seq_len = len_sentence_words


        if len_sentence_words > max_seq_len:
            max_seq_len = len_sentence_words
        idx = idx + 1

    return max_seq_len

def labels_matrix(data):

    labels = data['sentiment_values']

    labels_float = labels.astype(float)

    cats = ['0','1', '2', '3', '4']
    labels_mult = (labels_float * 4).astype(int)
    dummies = pd.get_dummies(labels_mult, prefix='', prefix_sep='')
    dummies = dummies.T.reindex(cats).T.fillna(0)
    labels_matrix = dummies.to_numpy()

    return labels_matrix

def get_indexed_sentences(data, word_idx, weight_matrix, max_seq_len):

    no_rows = len(data)
    ids = np.zeros((no_rows, max_seq_len), dtype='int32')

    word_idx_lwr =  {k.lower(): v for k, v in word_idx.items()}
    idx = 0

    for index, row in data.iterrows():

        sentence = (row['Phrase'])
        #print (sentence)
        tokenizer = RegexpTokenizer(r'\w+')
        sentence_words = tokenizer.tokenize(sentence)
        #print (sentence_words)
        i = 0
        for word in sentence_words:
            #print(index)
            word_lwr = word.lower()
            try:
                #print (word_lwr)
                ids[idx][i] =  word_idx_lwr[word_lwr]

            except Exception as e:
                if str(e) == word:
                    ids[idx][i] = 0
                continue
            i = i + 1
        idx = idx + 1

    return ids

def load_data_all(all_data_path, gloveFile):

    weight_matrix, word_idx = load_embeddings(gloveFile)

    all_data = read_data(all_data_path)
    train_data, test_data, dev_data = training_data_split(all_data)

    train_data = train_data.reset_index()
    dev_data = dev_data.reset_index()
    test_data = test_data.reset_index() 
    maxSeqLength = maxSeqLen(all_data)

    train_x = get_indexed_sentences(train_data, word_idx, weight_matrix, maxSeqLength)
    test_x = get_indexed_sentences(test_data, word_idx, weight_matrix, maxSeqLength)
    val_x = get_indexed_sentences(dev_data, word_idx, weight_matrix, maxSeqLength)

    train_y = labels_matrix(train_data)
    val_y = labels_matrix(dev_data)
    test_y = labels_matrix(test_data)
 
    print(train_x.shape)
    print(train_y.shape)

    print(np.unique(train_y.shape[1]))

    return train_x, train_y, test_x, test_y, val_x, val_y, weight_matrix, word_idx

def create_keras_model(weight_matrix, max_words, EMBEDDING_DIM ,train_x, train_y, test_x, test_y, val_x, val_y, batch_size, path):

    model = Sequential()
    model.add(Embedding(len(weight_matrix), EMBEDDING_DIM, weights=[weight_matrix], input_length=max_words, trainable=False))
    model.add(Bidirectional(LSTM(128, dropout=0.2, recurrent_dropout=0.2)))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.50))
    model.add(Dense(5, activation='softmax'))
    
    model.compile(loss='binary_crossentropy',optimizer='adam',
     metrics=['accuracy'])
    print(model.summary())

    saveBestModel = keras.callbacks.ModelCheckpoint(path+'/model/best_model.hdf5', monitor='val_acc', verbose=0, save_best_only=True, save_weights_only=False, mode='auto', period=1)
    earlyStopping = keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=3, verbose=0, mode='auto')

    model.fit(train_x, train_y, batch_size=batch_size, epochs=25, validation_data=(val_x, val_y), callbacks=[saveBestModel, earlyStopping])

    score, acc = model.evaluate(test_x, test_y, batch_size=batch_size)

    print('Test score:', score)
    print('Test accuracy:', acc)

    return model

def main():

    max_words = 56
    batch_size = 2000
    EMBEDDING_DIM = 100
    path = r'C:\Users\PC\Desktop\TwittersOpinion\model'
    
    all_data_path = path+'\Data'
    gloveFile = path+'\Data\glove\glove_6B_100d.txt'

    train_x, train_y, test_x, test_y, val_x, val_y, weight_matrix, word_idx = load_data_all(all_data_path, gloveFile)
  
    model = create_keras_model(weight_matrix, max_words, EMBEDDING_DIM, train_x, train_y, test_x, test_y, val_x, val_y, batch_size, path)

    model.save(path+"\model\my_model4w.h5")
    print("Saved model to " + path +"\model\my_model4w.h5")

main()