import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor

df = pd.read_csv('job_data_salary_eda.csv')

# Choose relevant columns
df.columns
df_model = df[['salary', 'company_size', 'company_type', 'company_sector', 'company_revenue',
               'company_rating', 'state', 'python', 'SQL', 'excel', 'tableau', 'power_bi', 'math',
               'machine_learning', 'statistics', 'presentation', 'reporting', 'senior']]

# Calculate the mean of the company_rating column, excluding NaN values
mean_company_rating = df_model['company_rating'].mean()
# Fill NaN values in the company_rating column with this mean
df_model.loc[:, 'company_rating'] = df_model['company_rating'].fillna(mean_company_rating)

# Get dummy variables
df_dum = pd.get_dummies(df_model)
# Identify boolean columns
bool_columns = df_dum.select_dtypes(include=['bool']).columns
# Convert boolean columns to int type
df_dum[bool_columns] = df_dum[bool_columns].astype(int)

# Train test splits
from sklearn.model_selection import train_test_split

X = df_dum.drop('salary', axis=1)
y = df_dum.salary.values

# Function to calculate VIF for each feature
def calculate_vif(df):
    vif_data = pd.DataFrame()
    vif_data["feature"] = df.columns
    vif_data["VIF"] = [variance_inflation_factor(df.values, i) for i in range(len(df.columns))]
    return vif_data

vif_df = calculate_vif(X)
print(vif_df[vif_df['VIF'] > 5])

# Dropping columns with a VIF > 5
df_dum_VIF_adj = df_dum.drop(vif_df[vif_df['VIF'] > 5]['feature'], axis=1)

XVIF = df_dum_VIF_adj.drop('salary', axis=1)
yVIF = df_dum_VIF_adj.salary.values

XVIF_train, XVIF_test, yVIF_train, yVIF_test = train_test_split(XVIF, yVIF, test_size=0.2, random_state=42)

# Multiple linear regression with VIF adjsted df
import statsmodels.api as sm

X_sm = X = sm.add_constant(X)

model = sm.OLS(y,X_sm)
print(model.fit().summary())

# Multiple linear regression without VIF adjustment to compare to other models
X = df_dum.drop('salary', axis=1)
y = df_dum.salary.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_sm = X = sm.add_constant(X)

model = sm.OLS(y,X_sm)
print(model.fit().summary())

# Cross validating the model
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


lm = LinearRegression()
lm.fit(X_train, y_train)

lm_cross_val_scores = cross_val_score(lm, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)
print(np.mean(cross_val_score(lm, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))

# Lasso regression
lm_l = Lasso()
lm_l_cross_val_scores = cross_val_score(lm_l, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)
print(np.mean(cross_val_score(lm_l, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))

#alpha = []
#error = []

#for i in range(1, 1000):
#    alpha.append(i)
#    lml = Lasso(alpha=(i))
#    error.append(np.mean(cross_val_score(lml, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))

#plt.plot(alpha,error)

#lm_l_a variable if a different alpha value is desired

lm_l_a = Lasso()
lm_l_a.fit(X_train, y_train)
y_train_pred = lm_l_a.predict(X_train)
y_test_pred = lm_l_a.predict(X_test)

def regression_metrics(model, X_train, y_train, X_test, y_test):
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    metrics = {
        'R-squared (Train)': r2_score(y_train, y_train_pred),
        'R-squared (Test)': r2_score(y_test, y_test_pred),
        'MAE (Train)': mean_absolute_error(y_train, y_train_pred),
        'MAE (Test)': mean_absolute_error(y_test, y_test_pred),
        'MSE (Train)': mean_squared_error(y_train, y_train_pred),
        'MSE (Test)': mean_squared_error(y_test, y_test_pred)
    }
    return metrics

# Calculate metrics for Linear Regression
lm_metrics = regression_metrics(lm, X_train, y_train, X_test, y_test)

# Calculate metrics for Lasso Regression
lm_l_a_metrics = regression_metrics(lm_l_a, X_train, y_train, X_test, y_test)

# Creating summary tables
lm_summary = pd.DataFrame({'Linear Regression': lm.coef_}, index=X_train.columns)
lm_l_a_summary = pd.DataFrame({'Lasso Regression': lm_l_a.coef_}, index=X_train.columns)

# Optionally, add the performance metrics to the summary table
for key, value in lm_metrics.items():
    lm_summary.loc[key] = value
for key, value in lm_l_a_metrics.items():
    lm_l_a_summary.loc[key] = value

# Print summary tables
print("Linear Regression Summary:\n", lm_summary)
print("\nLasso Regression Summary:\n", lm_l_a_summary)

# Random forest
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()

print(np.mean(cross_val_score(rf, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))

# Making modifications to the model df to improve error stats:
# The fields 'company_size', 'company_type', 'company_sector', 'company_revenue' have a high number
# of NaN values that may be distorting the results. I'll inititally try a model without any of 
# those variables aside from company_type (may have some influence with NaN values dropped. Then I'll try 
# without any of those variables.

df_model = df[['salary', 'company_rating', 'company_type', 'company_sector', 'state', 'python', 'SQL', 
               'excel', 'tableau', 'power_bi', 'math', 'machine_learning', 'statistics', 
               'presentation', 'reporting', 'senior']]

# Calculate the mean of the company_rating column, excluding NaN values
mean_company_rating = df_model['company_rating'].mean()
# Fill NaN values in the company_rating column with this mean
df_model.loc[:, 'company_rating'] = df_model['company_rating'].fillna(mean_company_rating)

# Drop NaN values
df_model.dropna(inplace=True)

# Get dummy variables
df_dum = pd.get_dummies(df_model)
# Identify boolean columns
bool_columns = df_dum.select_dtypes(include=['bool']).columns
# Convert boolean columns to int type
df_dum[bool_columns] = df_dum[bool_columns].astype(int)

# Train test splits
from sklearn.model_selection import train_test_split

X = df_dum.drop('salary', axis=1)
y = df_dum.salary.values

import statsmodels.api as sm

X_sm = X = sm.add_constant(X)

model = sm.OLS(y,X_sm)
print(model.fit().summary())

lm = LinearRegression()
lm.fit(X_train, y_train)

lm_cross_val_scores = cross_val_score(lm, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)
print(np.mean(cross_val_score(lm, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))

# Lasso regression
lm_l = Lasso()
lm_l_cross_val_scores = cross_val_score(lm_l, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)
print(np.mean(cross_val_score(lm_l, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))

# Random forest
rf = RandomForestRegressor()
print(np.mean(cross_val_score(rf, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))

# Tune models using GridsearchCV
from sklearn.model_selection import GridSearchCV
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

grid_search.best_params_

# Test ensembles
tpred_rf = grid_search.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test, tpred_rf)