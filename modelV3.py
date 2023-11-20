# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 14:34:49 2023
@author: alexs
"""

# Importing necessary libraries
import pandas as pd
import numpy as np
import statsmodels.api as sm  # For statistical models

# Loading the dataset
df = pd.read_csv('job_data_salary_cleaned_eda_model.csv')
df.drop('company_age', inplace=True, axis=1)
df = df.select_dtypes(include='number')  # Select only columns with numeric data

# Preparing the data for modeling
X = df.drop('salary', axis=1)  # Feature matrix (independent variables)
y = df.salary.values  # Target vector (dependent variable, 'salary')

# Adding a constant term to the predictor (needed for statsmodels)
X_sm = sm.add_constant(X)

# Ordinary Least Squares (OLS) Regression Model
model = sm.OLS(y,X_sm)
print(model.fit().summary())

# Importing additional libraries for machine learning
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Linear Regression Model
lm = LinearRegression()
lm_cross_val_scores = cross_val_score(lm, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)
print(np.mean(lm_cross_val_scores))

# Lasso Regression Model
lm_l = Lasso()
lm_l_cross_val_scores = cross_val_score(lm_l, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)
print(np.mean(lm_l_cross_val_scores))

# Random Forest Regressor Model
rf = RandomForestRegressor()
print(np.mean(cross_val_score(rf, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))

# Grid Search Cross-Validation for optimizing Random Forest parameters
param_grid = {
    'n_estimators': [10, 50, 100, 200],  # Number of trees in the forest
    'max_features': ['sqrt', 'log2'],  # The number of features to consider when looking for the best split
    'max_depth': [None, 10, 20, 30],  # Maximum depth of the tree
    'min_samples_split': [2, 5, 10],  # Minimum number of samples required to split a node
    'min_samples_leaf': [1, 2, 4],  # Minimum number of samples required at each leaf node
    'bootstrap': [True, False]  # Method for sampling data points
}
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid,
                           cv=3, n_jobs=-1, verbose=2, scoring='neg_mean_absolute_error')

grid_search.fit(X_train, y_train)  # Fitting the grid search model
best_rf_model = grid_search.best_estimator_  # Getting the best random forest model

# Testing the best model on the test set
tpred_rf = best_rf_model.predict(X_test)
print(mean_absolute_error(y_test, tpred_rf))

# Assessing the importance of each variable in the Random Forest model
importances = best_rf_model.feature_importances_
feature_names = X.columns
feature_importances = pd.Series(importances, index=feature_names).sort_values(ascending=False)
print(feature_importances)

# Importing the SHAP library for explainable AI
import shap

# Calculate SHAP values to understand the impact of each feature
explainer = shap.TreeExplainer(best_rf_model)
shap_values = explainer.shap_values(X_train)

# Plot SHAP values to visualize the importance of features
shap.summary_plot(shap_values, X_train, plot_type="bar")  # Bar plot of SHAP values
# Plot SHAP values for the first few instances
shap.summary_plot(shap_values, X_train, plot_type="bar")
