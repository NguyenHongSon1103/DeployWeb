from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from past.builtins import xrange
def tf_idf(sent,word2vec_model):
    dct = Dictionary(sent)
    corpus = [dct.doc2bow(line) for line in sent]
    tf_idf_model = TfidfModel(corpus)
    vector = tf_idf_model[corpus]
    d = {dct.get(id): value for doc in vector for id, value in doc}
    sents_emd = []
    no_of_sent = sum(1 for i in sent)
    for i in xrange(no_of_sent):
        sent_emd = []
        for j in xrange(len(sent[i])):
            word = sent[i][j]
            if word in word2vec_model:
                emd = d[word]*word2vec_model[word]
                sent_emd.append(emd)
        sent_emd_np = np.array(sent_emd)
        sum_ = sent_emd_np.sum(axis=0)
        result = sum_/np.sqrt((sum_**2).sum())
        sents_emd.append(result)
    
    return sents_emd
