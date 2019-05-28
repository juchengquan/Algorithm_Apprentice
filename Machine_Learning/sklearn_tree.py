import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

from sklearn.ensemble import AdaBoostRegressor 
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

np.random.seed(2019)


dat = pd.read_csv("./dataset/Admission_Predict_Ver1.1.csv", index_col=0)

X = dat.iloc[:, 0:7].values
y = dat.iloc[:,-1].values

scaler = preprocessing.MinMaxScaler()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

scaler = scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

### Random Forest
rnd_clf = RandomForestRegressor(n_estimators=100) 
rnd_clf = rnd_clf.fit(X_train, y_train)
y_t_rnd = rnd_clf.predict(X_train)
y_pred_rnd = rnd_clf.predict(X_test)
rnd_r2 = r2_score(y_train, y_t_rnd)
rnd_error = mean_squared_error(y_test, y_pred_rnd) 

### adaboost
ada_reg = AdaBoostRegressor(n_estimators=100, learning_rate=0.01)
ada_reg = ada_reg.fit(X_train, y_train)
y_pred_ada = ada_reg.predict(X_test)

ada_error = mean_squared_error(y_test, y_pred_ada)

### SVM
svm_reg = SVR(kernel="rbf", degree= 3, gamma="scale")
svm_reg =svm_reg.fit(X_train, y_train)
y_pred_svm = svm_reg.predict(X_test)
svm_error = mean_squared_error(y_test, y_pred_svm)


### decision tree
tree_reg = DecisionTreeRegressor()
tree_reg = tree_reg.fit(X_train, y_train)
y_pred_tree = tree_reg.predict(X_test)
y_t_tree = tree_reg.predict(X_train)
tree_r2 = r2_score(y_train, y_t_tree)
tree_error = mean_squared_error(y_test, y_pred_tree)


#dat.hist()