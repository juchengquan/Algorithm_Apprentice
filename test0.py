# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import sklearn
from sklearn import datasets
from sklearn.model_selection import train_test_split

# mnist = datasets.fetch_openml(name="mnist_784", version=1, return_X_y=True, cache=True)

X = mnist[0] 
y = mnist[1].astype(np.int8) 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=10000)

sorted_train = np.array(sorted([(target, i) for i,target in enumerate(y_train)]))[:,1]
sorted_test = np.array(sorted([(target, i) for i,target in enumerate(y_test)]))[:,1] 

X_train = X_train[sorted_train]
y_train = y_train[sorted_train]

