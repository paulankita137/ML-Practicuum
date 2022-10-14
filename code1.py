# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 13:26:59 2022

@author: squid
"""
import pickle
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score


# Get Data
file = 'appml-assignment1-dataset.pkl'
data = pd.read_pickle(file)

X = data['X']
y = pd.DataFrame(data['y'])
cad_high_data = y

# Clip Data
cad_data = X[['date', 'CAD-open', 'CAD-high', 'CAD-low', 'CAD-close', 'EUR-open', 'EUR-high', 'EUR-low', 'EUR-close']]
cad_data = cad_data.sort_values(by='date')
cad_data = cad_data.drop('date', axis=1)

# Split Data
train_set_cad_data, test_set_cad_data = train_test_split(cad_data,test_size=0.8,random_state=42)
train_set_cad_high_data, test_set_cad_high_data = train_test_split(cad_high_data,test_size=0.75,random_state=42)

# Train/Test Sets
cad_data_tr = train_set_cad_data.copy() #X
cad_data_test = test_set_cad_data.copy()

cad_high_data_tr = train_set_cad_high_data.copy() #y
cad_high_data_test = test_set_cad_high_data.copy()

# Data Labels
cad_data_tr_labels = cad_data_tr.copy()
cad_data_test_labels = cad_data_test.copy()

cad_high_data_tr_labels = cad_high_data_tr.copy()
cad_high_data_test_labels = cad_high_data_test.copy()

# Pipeline
num_pipeline = Pipeline([
      ('imputer', SimpleImputer(strategy="median")),
      ('std_scaler', StandardScaler()),
    ])

# Transform Data
cad_data_tr_trans = num_pipeline.fit_transform(cad_data_tr)
cad_data_test_trans = num_pipeline.transform(cad_data_test)

# Linear Regression
lin_reg=LinearRegression()
lin_reg.fit(cad_data_tr_trans,cad_data_tr_labels)

# Decision Tree Regressor
tree_reg=DecisionTreeRegressor()
tree_reg.fit(cad_data_tr_trans,cad_data_tr_labels)

# Random Forest Regressor
forest_reg=RandomForestRegressor()
forest_reg.fit(cad_data_tr_trans,cad_data_tr_labels)
# ----- Save after fit -----

# RMSE TRAIN
linPreds_tr=lin_reg.predict(cad_data_tr_trans)
treePreds_tr=tree_reg.predict(cad_data_tr_trans)
forestPreds_tr=forest_reg.predict(cad_data_tr_trans)

lin_rmse_tr=np.sqrt(mean_squared_error(cad_data_tr_labels,linPreds_tr))
tree_rmse_tr=np.sqrt(mean_squared_error(cad_data_tr_labels,treePreds_tr))
forest_rmse_tr=np.sqrt(mean_squared_error(cad_data_tr_labels,forestPreds_tr))

print('\nRMSE TRAIN Linear: ', lin_rmse_tr)
print('RMSE TRAIN Tree: ', tree_rmse_tr)
print('RMSE TRAIN Forest: ', forest_rmse_tr)

# RMSE TEST
linPreds_test=lin_reg.predict(cad_data_test_trans)
treePreds_test=tree_reg.predict(cad_data_test_trans)
forestPreds_test=forest_reg.predict(cad_data_test_trans)

from sklearn.metrics import mean_squared_error
lin_rmse_test=np.sqrt(mean_squared_error(cad_data_test_labels,linPreds_test))
tree_rmse_test=np.sqrt(mean_squared_error(cad_data_test_labels,treePreds_test))
forest_rmse_test=np.sqrt(mean_squared_error(cad_data_test_labels,forestPreds_test))

print('\nRMSE TEST Linear: ', lin_rmse_test)
print('RMSE TEST Tree: ', tree_rmse_test)
print('RMSE TEST Forest: ', forest_rmse_test)

# Cross Validation TRAIN
scores=cross_val_score(lin_reg,cad_data_tr_trans,cad_data_tr_labels,
  scoring="neg_mean_squared_error",cv=10)
lin_rms_scores=np.sqrt(-scores)
scores=cross_val_score(tree_reg,cad_data_tr_trans,cad_data_tr_labels,
  scoring="neg_mean_squared_error",cv=10)
tree_rms_scores=np.sqrt(-scores)
scores=cross_val_score(forest_reg,cad_data_tr_trans,cad_data_tr_labels,
  scoring="neg_mean_squared_error",cv=10)
forest_rms_scores=np.sqrt(-scores)
print('\n --Cross Validation TRAIN--')
print('\nLin Reg: ', lin_rms_scores)
print('\nTree: ', tree_rms_scores)
print('\nForest: ', forest_rms_scores)

# Cross Validation TEST
scores=cross_val_score(lin_reg,cad_data_test_trans,cad_data_test_labels,
  scoring="neg_mean_squared_error",cv=10)
lin_rms_scores=np.sqrt(-scores)
scores=cross_val_score(tree_reg,cad_data_test_trans,cad_data_test_labels,
  scoring="neg_mean_squared_error",cv=10)
tree_rms_scores=np.sqrt(-scores)
scores=cross_val_score(forest_reg,cad_data_test_trans,cad_data_test_labels,
  scoring="neg_mean_squared_error",cv=10)
forest_rms_scores=np.sqrt(-scores)
print('\n --Cross Validation TEST--')
print('\nLin Reg: ', lin_rms_scores)
print('\nTree: ', tree_rms_scores)
print('\nForest: ', forest_rms_scores)

# Save file to pickle
with open('pipeline1.pkl', 'wb') as f:
    pickle.dump(num_pipeline, f)

with open('model1.pkl', 'wb') as f:
    pickle.dump(lin_reg, f)