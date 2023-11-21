# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 14:34:49 2023

@author: alexs
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm


df = pd.read_csv('job_data_salary_cleaned_eda_model.csv')
df.drop('company_age', inplace=True, axis=1)
df = df.select_dtypes(include='number')

X = df.drop('salary', axis=1)
y = df.salary.values

X_sm = X = sm.add_constant(X)

model = sm.OLS(y,X_sm)
print(model.fit().summary())

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Linear model
lm = LinearRegression()
lm_cross_val_scores = cross_val_score(lm, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)
print(np.mean(cross_val_score(lm, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))

# Lasso regression
lm_l = Lasso()
lm_l_cross_val_scores = cross_val_score(lm_l, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)
print(np.mean(cross_val_score(lm_l, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))

# Random forest
rf = RandomForestRegressor()
print(np.mean(cross_val_score(rf, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))

# Grid search to decrease the error of the RF model
param_grid = {
    'n_estimators': [10, 50, 100, 200],
    'max_features': ['sqrt', 'log2'],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]
}
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, 
                           cv=3, n_jobs=-1, verbose=2, scoring='neg_mean_absolute_error')

grid_search.fit(X_train, y_train)
best_rf_model = grid_search.best_estimator_

# Test ensembles
tpred_rf = best_rf_model.predict(X_test)
print(mean_absolute_error(y_test, tpred_rf))

# Analysing the importance of each feature

importances = best_rf_model.feature_importances_
feature_names = X.columns
feature_importances = pd.Series(importances, index=feature_names).sort_values(ascending=False)
print(feature_importances)


import shap

# Calculate SHAP values
explainer = shap.TreeExplainer(best_rf_model)
shap_values = explainer.shap_values(X_train)

# Plot SHAP values for the first few instances
shap.summary_plot(shap_values, X_train, plot_type="bar")

