# -*- coding: utf-8 -*-
"""knnClassifier2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QBfcUQiQApMxvhnLJcGNRsV1qoA_5gSU
"""

import matplotlib.pyplot as plt
from keras.datasets import cifar10
import numpy as np
import statistics
(X_train, y_train), (X_test, y_test) = cifar10.load_data()

X = []  #stores 20 cat and dog images
y = []  #stores the label associated with each image

"""
function that gets n images of a particular class
and stores it in X and the labels in y
"""
def get_images(class_index, n):
  count = 0;
  i = 0
  while(count < n):
    if(y_train[i] == class_index):
      X.append(X_train[i])
      y.append(y_train[i])
      count += 1
    i += 1

"""
In CIFAR10, cats are labeled 3 and dogs are labeled 5
"""
get_images(3, 10) #adding 10 images of cats to X
get_images(5, 10) #adding 10 images of dogs to X

"""
function that displays n images belonging to class "cls"
"""
def displayImages(n, cls):
  d = 0
  if cls == 'dog':
    d = 10
  elif cls == 'cat':
    d = 0
  fig, *a = plt.subplots(1, n)
  for i in range(n):
    a[0][i].imshow(X[i + d])
    a[0][i].axis('off')

displayImages(3, 'cat')
displayImages(3, 'dog')
plt.show()

#Converting the lists into numpy arrays
#Coverting 32*32*3 image into 1*3072 array
X = np.array(X).reshape(20, 32*32*3)
y = np.array(y)

#Splitting data into training and testing tests (20% test data)
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size = 0.2, stratify = y, random_state = 2)


class knnClassifier():

  def __init__(self, distance_metric):
    self.distance_metric = distance_metric

  def get_distance(self, x_train, y_train, x_test):
    (m, n) = x_train.shape
    distance_list = []

    if self.distance_metric == 'manhattan':
      for i in range(m):
        dist = (abs(x_train[i] - x_test)).sum()
        distance_list.append([x_train[i], y_train[i][0], dist])
      return distance_list

    elif self.distance_metric == 'euclidean':
      for i in range(m):
        dist = np.sqrt(((x_train[i] - x_test)**2).sum())
        distance_list.append([x_train[i], y_train[i][0], dist])
      return distance_list

  def predict(self, x_train, y_train, x_test, k):
    label = []
    distance_list = self.get_distance(x_train, y_train, x_test)
    distance_list.sort(key = lambda x : x[2])
    for i in range(k):
      label.append(distance_list[i][1])
    return statistics.mode(label)

def accuracy_score(classifier, k):
  correct_predictions = 0
  for i in range(len(X_test)):
    if classifier.predict(X_train,Y_train, X_test[i], k) == Y_test[i]:
      correct_predictions += 1  
  print("Accuracy: ", end = ' ')
  print(correct_predictions/4)

k = 9
#predicting result for the test data (manhattan distance)
print("Using Manhattan Distance")
classifier1 = knnClassifier('manhattan')
accuracy_score(classifier1, k)

#predicting result for the test data (euclidean distance)
print("Using Euclidean Distance")
classifier2 = knnClassifier('euclidean')
accuracy_score(classifier2, k)