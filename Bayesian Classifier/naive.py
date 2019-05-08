import numpy as np
import pandas as pd
from sklearn import datasets

iris = datasets.load_iris()
from sklearn.naive_bayes import GaussianNB
model = GaussianNB()
model = model.fit(iris.data, iris.target)
yhat = model.predict(iris.data)



print ((iris.target != yhat).sum() )

pass
