
import numpy as np
from nltk.tokenize import RegexpTokenizer
import tensorflow as tf
from tensorflow.python.keras.backend import set_session
import requests, datetime, pytz
import time, uuid, copy, string, codecs
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer

# stop_words = list(set(stopwords.words('english')))
def load_embeddings(embedding_path):
    """Loads embedings, returns weight matrix and dict from words to indices."""
    print('loading word embeddings from %s' % embedding_path)
    weight_vectors = []
    word_idx = {}
    with codecs.open(embedding_path, encoding='utf-8') as f:
        for line in f:
            word, vec = line.split(u' ', 1)
            word_idx[word] = len(weight_vectors)
            weight_vectors.append(np.array(vec.split(), dtype=np.float32))
    # Annoying implementation detail; '(' and ')' are replaced by '-LRB-' and
    # '-RRB-' respectively in the parse-trees.
    word_idx[u'-LRB-'] = word_idx.pop(u'(')
    word_idx[u'-RRB-'] = word_idx.pop(u')')
    # Random embedding vector for unknown words.
    weight_vectors.append(np.random.uniform(
        -0.05, 0.05, weight_vectors[0].shape).astype(np.float32))
    return np.stack(weight_vectors), word_idx

global graph, session
session = tf.compat.v1.Session() 
graph = tf.compat.v1.get_default_graph()

path = r"C:\Users\PC\Desktop\TwittersOpinion\model"
gloveFile = path+"\Data\glove\glove_6B_100d.txt"
weight_matrix, word_idx = load_embeddings(gloveFile)
model_path = path +"\model\my_model4.h5"
# loaded_model = load_model(model_path)
set_session(session)
# model_path = path + '/model/my_model2.h5'
loaded_model = load_model(model_path)
# loaded_model.summary()

def strip_all_entities(text):
    entity_prefixes = ['@','#']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        if "http" in word:
            break
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words[:52])


def live_test(data):

    set_session(session)
    #data = "Pass the salt"
    #data_sample_list = data.split()
    live_list = []
    live_list_np = np.zeros((56,2))
    # split the sentence into its words and remove any punctuations.
    tokenizer = RegexpTokenizer(r'\w+')
    data_sample_list = tokenizer.tokenize(data)

    # labels = np.array(['1','2'], dtype = "int")
    #word_idx['I']
    # get index for the live stage
    data_index = np.array([word_idx[word.lower()] if word.lower() in word_idx else 0 for word in data_sample_list])
    data_index_np = np.array(data_index)
    print(data_index_np)

    # padded with zeros of length 56 i.e maximum length
    padded_array = np.zeros(56) # use the def maxSeqLen(training_data) function to detemine the padding length for your data
    padded_array[:data_index_np.shape[0]] = data_index_np
    data_index_np_pad = padded_array.astype(int)
    live_list.append(data_index_np_pad)
    live_list_np = np.asarray(live_list)
    type(live_list_np)

    # get score from the model
    with graph.as_default():
        score = loaded_model.predict(live_list_np, batch_size=1, verbose=0)
    print(score)
    # print(score[0])

    single_score = max(score[0]) # maximum of the array i.e single band
    print(single_score)
    # weighted score of top 3 bands
    top_3_index = np.argsort(score)[0][-3:]
    top_3_scores = score[0][top_3_index]
    top_3_weights = top_3_scores/np.sum(top_3_scores)
    single_score_dot = np.round(np.dot(top_3_index, top_3_weights), decimals = 2)

    print(top_3_index)
    print(top_3_scores)
    print(top_3_weights)
    print(single_score_dot)

    #print (single_score)
    return single_score_dot

def get_result(data_sample_list):
    set_session(session)
    positive_tweets_cnt = 0
    very_positive_tweets_cnt = 0
    negative_tweets_cnt = 0
    very_negative_tweets_cnt = 0
    neutral_tweets_cnt = 0
    live_list = []
    live_list_np = np.zeros((56, 2))
    tokenizer = RegexpTokenizer(r'\w+')

    vreme1 = time.time()

    for data_sample in data_sample_list:
        clear_text = strip_all_entities(data_sample.full_text)
        # print(clear_text)
        data_sample_token = tokenizer.tokenize(clear_text)
        # word_idx['I']
        # get index for the live stage
        data_index = np.array([word_idx[word.lower()] if word.lower(
        ) in word_idx else 0 for word in data_sample_token])
        data_index_np = np.array(data_index)
        padded_array = np.zeros(56)
        padded_array[:data_index_np.shape[0]] = data_index_np
        data_index_np_pad = padded_array.astype(int)
        live_list.append(data_index_np_pad)

    print("vreme1: " + str(time.time() - vreme1))
    if len(live_list) == 0:
        raise Exception("live list is empty!")
    # get score from the model
    # get score from the model
    live_list_np = np.asarray(live_list)
    type(live_list_np)

    start_time = time.time()
    with graph.as_default():
        scores = loaded_model.predict(
            live_list_np, batch_size=len(live_list), verbose=0)
    # print (scores)
    duration = time.time() - start_time
    print("Duration of prediction: " + str(duration))

    session_uuid = uuid.uuid1()
    mytweets = []
    print("Scores: " + str(len(scores)))
    for i in range(len(scores)):
        top_3_index = np.argsort(scores[i])[-3:]
        top_3_scores = scores[i][top_3_index]
        top_3_weights = top_3_scores/np.sum(top_3_scores)
        single_score_dot = np.round(
            np.dot(top_3_index, top_3_weights), decimals=2)
        if(single_score_dot >= 0.4 and single_score_dot <= 0.6):
            label = "Neutral"
            neutral_tweets_cnt += 1
        elif(single_score_dot >= 0.2 and single_score_dot <= 0.4):
            label = "Negative"
            negative_tweets_cnt += 1
        elif(single_score_dot <= 0.8 and  single_score_dot >= 0.6):
            label = "Positive"
            positive_tweets_cnt += 1
        elif(single_score_dot < 0.2):
            very_negative_tweets_cnt += 1
        elif(single_score_dot > 0.8):
            very_positive_tweets_cnt += 1

    thisdict = [{
        "label": "Very Positive",
        "num": very_positive_tweets_cnt,
        "session":  str(session_uuid)
    }, {
        "label": "Positive",
        "num": positive_tweets_cnt,
        "session": str(session_uuid)
    }, {
        "label": "Neutral",
        "num": neutral_tweets_cnt,
        "session":  str(session_uuid)
    }, {
        "label": "Negative",
        "num": negative_tweets_cnt,
        "session": str(session_uuid)
    }, {
        "label": "Very Negative",
        "num": very_negative_tweets_cnt,
        "session":  str(session_uuid)
    }]
    return thisdict, len(scores), positive_tweets_cnt, neutral_tweets_cnt, negative_tweets_cnt, very_negative_tweets_cnt, very_positive_tweets_cnt
    # return thisdict, len(scores), positive_tweets_cnt, neutral_tweets_cnt, negative_tweets_cnt


def map_to_chart_data(result, searchTerm):
    pos_res_list = []
    neu_res_list = []
    neg_res_list = []
    very_neg_res_list = []
    very_pos_res_list = []

    
    tmstmp_list = []
    for r in result:
        pos_res_list.append(float(r[1]))
        neg_res_list.append(float(r[2]))
        neu_res_list.append(float(r[3]))
        very_pos_res_list.append(float(r[6]))
        very_neg_res_list.append(float(r[7]))
        tmstmp_list.append(str(r[4].astimezone(pytz.timezone("Europe/Belgrade")).strftime("%d-%m-%Y %H:%M")))
    thisdict = {
        "searchTerm": searchTerm,
        "chartLabels": tmstmp_list,
        "chartData" : [ {
            "data": very_neg_res_list,
            "label": "Very Negative"
        },{
            "data": neg_res_list,
            "label": "Negative"
        }, {
            "data": neu_res_list,
            "label": "Neutral"
        }, {
            "data": pos_res_list,
            "label": "Positive"
        }, {
            "data": very_pos_res_list,
            "label": "Very Positive"
        }]
    }

    return thisdict
