from nltk.stem import PorterStemmer
from gensim.parsing.preprocessing import STOPWORDS
from nltk.tokenize import word_tokenize
import pandas as pd
import re
import smart_open
import string
import sys
import csv
import data_processing as dp
import word2vec as w2v
#get data has one column
def get_data(path):
    data=pd.read_csv(path,header=None, error_bad_lines=False)
    #get vietnamese stopword then save in list stopwords

    stopwords=[]
    data_stopword=pd.read_csv('vietnamese-stopwords.txt',header=None)
    for l in data_stopword[0]:
        stopwords.append(l)
    #function convert accent vietnamese to no accent vietnamese
    def no_accent_vietnamese(s):
        s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
        s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
        s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
        s = re.sub(r'[ìíịỉĩ]', 'i', s)
        s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
        s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
        s = re.sub(r'[đ]', 'd', s)
        return s
    cnt=0
    remove = ['(', ')', '^','"','?','!','.','❤️',':','T^T']
    all_docs=[]
    dem=0
    #get data into all_docs
    for line in data[0]:
        if cnt%3!=1:
            cnt+=1
            continue
        cnt+=1
        words=word_tokenize(line)
        #words=[w for w in words if w not in stopwords]  
        words=[w for w in words if w not in remove]  
        words=[w.lower() for w in words]
        #words=[no_accent_vietnamese(w) for w in words]
        words=[w for w in words if w.isalpha()]
        all_docs.append(words)
    all_labels=[]
    cnt=0
    for line in data[0]:
        if cnt%3!=2:
            cnt+=1
            continue
        cnt+=1
        all_labels.append(line)
    return all_docs,all_labels





