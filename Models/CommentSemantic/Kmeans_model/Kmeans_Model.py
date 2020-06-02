from sklearn.cluster import KMeans
import numpy as np
from sklearn import  model_selection
import  joblib
def purity(labels, label_root):
    cluster_label = dict([(k, 0) for k in range(2)])
    for k in range(2):
        Xk = []
        for index in range(len(labels)):
            if labels[index] == k:
                Xk.append(index)

        cluster_label[k] = Xk
    cnt_doc = 0
    for k in range(2):

        Xk = cluster_label[k]
        count_max = dict([(label, 0) for label in range(2)])
        max = 0
        for index in range(len(Xk)):
            count_max[label_root[Xk[index]][1]] +=1
        for label in range(2):
            if count_max[label] > max:
                max = count_max[label]

        cnt_doc += max

    return (float(cnt_doc)/float(len(label_root)))

labels = np.load('E:\\20192\\Machine Learning\\data\\train_mylabel .npy')
data_vector = np.load('E:\\20192\\Machine Learning\\data\\train_mydata.npy')
train_size = int(data_vector.shape[0]*0.7)
data_train = data_vector[0:train_size,:]
label_train = labels[0:train_size,:]
data_test = data_vector[train_size+1:,:]
label_test = labels[train_size+1:,:]

kmeans = KMeans(n_clusters=2, init='k-means++',random_state=2018, n_init= 5).fit(data_train)

joblib.dump(kmeans, 'E:\\20192\\Machine Learning\\Kmeans_model_v2.sav')
kmeans_model = joblib.load('E:\\20192\\Machine Learning\\Kmeans_model_v2.sav')

train_pre = kmeans_model.predict(data_train)
test_pre = kmeans_model.predict(data_test)
print("Train Accuracy: "+ str(purity(train_pre,label_train)))
print("Test Accuracy: "+ str(purity(test_pre,label_test)))