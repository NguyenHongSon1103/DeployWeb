from data_preprocessing import *
from tf_idf import *
from word2vec_model import *
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
path=r"D:\20192\machine_learning\data\train.crash"

#get data and processing
data,label=get_data(path)
#train model word2vec
word2vec_model=start(data) 
#convert word to vector
X=tf_idf(data,word2vec_model)
y=[]
for i in label:
  y.append(i)
X=np.array(X)
y=np.array(y)
#split train test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


svm = SVC()
param = {'C': [10], 'kernel': ['rbf']}

gs = GridSearchCV(estimator=svm, param_grid=param, cv=3, n_jobs=4)
print(gs)
gs.fit(X_train, y_train)
gs.score(X_train, y_train)

gs.score(X_test, y_test)