import pandas as pd
from nltk import word_tokenize
remove = ['(', ')', '^','"','?','!','.','❤️',':','T^T']
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from past.builtins import xrange
import multiprocessing
from gensim.models import Word2Vec
import numpy as np
import sklearn
import joblib
w2v=Word2Vec.load('w2v_model.model')
svm_model=joblib.load("SVM_model.sav")
def embedding(sent):
    sents_emd = []
    no_of_sent = sum(1 for i in sent)
    for i in xrange(no_of_sent):
        sent_emd = []
        for j in xrange(len(sent[i])):
            word = sent[i][j]
            if word in w2v:
                emd = w2v[word]
                sent_emd.append(emd)
        sent_emd_np = np.array(sent_emd)
        sum_ = sent_emd_np.sum(axis=0)
        result = sum_/np.sqrt((sum_**2).sum())
        sents_emd.append(result)
    return sents_emd
def processing_data(data):
    w_t=[]
    words=word_tokenize(data)
    words=[w for w in words if w not in remove]  
    words=[w.lower() for w in words]
    words=[w for w in words if w.isalpha()]
    w_t.append(words)
    return w_t
data_test="Quá tệ, thức ăn chả ngon còn bẩn nữa"
data_test_after_processing=processing_data(data_test)
X=embedding(data_test_after_processing)
print(svm_model.predict(X))