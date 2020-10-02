#!/usr/bin/env python3

"""
Quiz 3

Task:
Your task for quiz 3 is to write a python script that:
- Imports the libraries you need
- Reads in the data: data/nba_rookies.csv
- Processes data:
    1. Sets the 'Name' column as the index
    2. Converts the 'TARGET_5Yrs' column to 0/1 using 0 for 'No' and 1 for 'Yes'
- Models data using any classification algorithm you would like
    - If you do not know what to do here, feel free to fit a Logistic Regression model with default hyperparameters. But you are free to use any other model or methods that you know if you think that would be better!
    - Use a random state of 42 when splitting your data into training and testing
    - Use ALL columns (except your target) as your X matrix
- Generates predictions on your test data
- Creates a new DataFrame that has:
    1. One column called 'predictions' which is the predictions from your model on your test data
    2. An index that is the name of the player associated with the prediction from your test data
- Writes the DataFrame with the predictions to a csv called 'predictions.csv' in the data folder in this repository

This script should be able to be run in your terminal: python 03-quiz.py


Fill in this .py file with your solutions. Comments of the above instructions are included to guide your workflow.
"""

#################################
# Your Info
# Please fill out the following questions:

# Your name: Vivian Nguyen

# Your section: DSIR 824

# Your email: ngux.vinh@gmail.com

#################################

# Import the libraries you need
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# adding more classifiers

from sklearn.preprocessing import StandardScaler

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier

# adding some pipeline stuff, some of these classifiers need scaling before input
from sklearn.pipeline import make_pipeline

# for fun, add a timer
import datetime as dt

# Read in the data: data/nba_rookies.csv
df_raw = pd.read_csv('./data/nba_rookies.csv')
df = df_raw.copy()

# Process data:
# 1. Set the 'Name' column as the index
df.set_index('Name', inplace=True)
#print(df.head())

#print(df.columns)

# 2. Convert the 'TARGET_5Yrs' column to 0/1 using 0 for 'No' and 1 for 'Yes'
#print(df['TARGET_5Yrs'].head())

df['TARGET_5Yrs'] = df['TARGET_5Yrs'].map({'No':0, 'Yes':1})

#print(df['TARGET_5Yrs'].head())


# Model data using any classification algorithm you would like
# If you do not know what to do here, feel free to fit a Logistic Regression model with default hyperparameters
# But you are free to use any other model or methods that you know if you think that would be better!
# Use a random state of 42 when splitting your data into training and testing

# Create X and y
X = df.drop('TARGET_5Yrs', axis=1)
y = df['TARGET_5Yrs']

X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=42)

#print(X_train.head())
#print(y_test.head())

# Train Logistic 
time_start = dt.datetime.now()
lr = LogisticRegression(n_jobs=-1, max_iter=100_000)
lr.fit(X_train, y_train)
train_score = lr.score(X_train, y_train)
test_score = lr.score(X_test, y_test)
time_done = dt.datetime.now()
print(f'Train Score: {train_score}, \n Test Score: {test_score} \n Time Taken: {time_done-time_start}')

# Train Trees
# Fun fact, we don't need to scale here
list_estimators = [DecisionTreeClassifier(), RandomForestClassifier(), ExtraTreesClassifier()]

for estimator in list_estimators:
    time_start = dt.datetime.now()
    estimator.fit(X_train, y_train)
    train_score = estimator.score(X_train, y_train)
    test_score = estimator.score(X_test, y_test)
    time_done = dt.datetime.now()
    print(f'Train Score: {train_score}, \n Test Score: {test_score} \n Time Taken: {time_done-time_start}')
    

# Generate predictions on your test data
predictions = lr.predict(X_test)

# predict our list of estmators
list_predictions = []
for estimator in list_estimators:
    list_predictions.append(estimator.predict(X_test))
    
#print(pd.DataFrame(list_predictions).head())
# Create a new DataFrame for predictions
#print(y_test.head())
df_predictions = pd.DataFrame(predictions, columns=['predictions - logr'], index=y_test.index)
df_list_predictions = list_predictions

df_predictions = df_predictions.join(
    pd.DataFrame(list_predictions,index = [
        'predictions - tree', 
        'predictions - rtree', 
        'predictions - etree'], columns=y_test.index).T)

print(df_predictions.head())

#print(df_predictions.head())

# 2. Have one column called 'predictions'
# which is the predictions from your model on your test data

# 1. Have an index that is the name of the player


# Write the DataFrame you created to a csv called 'predictions.csv'
# in the data folder in this repository
#df_predictions.to_csv('predictions-2.csv')
