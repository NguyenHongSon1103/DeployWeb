import numpy as np
from nltk import word_tokenize
from sklearn.svm import SVC
from gensim.models import Word2Vec
import joblib
#from keras import models
#import tensorflow as tf


class CommentSemantic:
    def __init__(self):
        self.w2v = Word2Vec.load('Models/CommentSemantic/last_w2v_model.model')
        self.svm_model = joblib.load('Models/CommentSemantic/SVM_model.sav')
        #self.nn_model = models.load_model('Models/CommentSemantic/CCSBest_model_v2.h5')
        self.remove = ['(', ')', '^', '"', '?', '!', '.', '❤️', ':', 'T^T']
        # self.nn_model._make_predict_function()
        # self.graph = tf.get_default_graph()

    def __processing_data(self, data):
        w_t = []
        words = word_tokenize(data)
        words = [w for w in words if w not in self.remove]
        words = [w.lower() for w in words]
        words = [w for w in words if w.isalpha()]
        w_t.append(words)
        return w_t

    def __embedding(self, sent):
        sents_emd = []
        for first in sent:
            sent_emd = []
            for second in first:
                word = second
                if word in self.w2v:
                    emd = self.w2v[word]
                    sent_emd.append(emd)
            sent_emd_np = np.array(sent_emd)
            sum_ = sent_emd_np.sum(axis=0)
            result = sum_ / np.sqrt((sum_ ** 2).sum())
            sents_emd.append(result)
        return sents_emd

    def predict(self, data, mode='svm'):
        data_processed = self.__processing_data(data)
        embedding_vector = self.__embedding(data_processed)
        if mode == 'svm':
            label = self.svm_model.predict(embedding_vector)[0]
            conf = -1
        else:
            return
        #     embedding_vector = np.reshape(embedding_vector, (1, 300,))
        #     with self.graph.as_default():
        #         predictions = self.nn_model.predict(embedding_vector)[0]
        #     label = np.argmax(predictions)
        #     conf = predictions[label]
        return label, conf
