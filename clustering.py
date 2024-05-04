import sklearn
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

kmeans = KMeans(n_clusters=int(199*0.8))

knn = KNeighborsClassifier(n_neighbors=2)

arr = np.load('num.py.npy')
s = arr.shape
new_arr = arr.reshape((s[0] * s[1], s[2]))

labels = np.repeat(np.arange(199), 3)
(trainX, testX, trainY, testY) = train_test_split(new_arr, labels, train_size=0.80)

kmeans.fit(trainX)
knn.fit(trainX, trainY)
pred = kmeans.predict(testX)
pred2 = knn.predict(testX)
# print(classification_report(testY, pred2))

# print(classification_report(pred))


print(pred)
# print(pred2)
