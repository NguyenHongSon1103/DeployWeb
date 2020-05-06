import numpy as np
from nltk import word_tokenize
from sklearn.svm import SVC
from gensim.models import Word2Vec
import joblib


class CommentSemantic:
    def __init__(self, encode_model_path, model_path):
        self.w2v = Word2Vec.load(encode_model_path)
        self.svm_model = joblib.load(model_path)
        self.remove = ['(', ')', '^', '"', '?', '!', '.', '❤️', ':', 'T^T']

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

    def predict(self, data):
        data_processed = self.__processing_data(data)
        data_processed = np.array(data_processed)
        if data_processed.shape[-1] == 1:
            print("Some thing wrong!")
            return None
        embedding_vector = self.__embedding(data_processed)
        predictions = self.svm_model.predict(embedding_vector)
        return predictions
