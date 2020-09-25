import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns

import models as ms

from sklearn.linear_model import LinearRegression, LogisticRegression, Lasso, Ridge, ElasticNet, SGDClassifier
from sklearn.svm import SVR, LinearSVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer, make_column_transformer, make_column_selector
from sklearn.metrics import mean_squared_error
from sklearn.feature_selection import VarianceThreshold, SelectKBest, GenericUnivariateSelect, RFE, SelectFromModel


from sklearn import set_config
from joblib import dump, load

class ModelSelection:
    '''
    This holds several functions to conduct and process batch pipeline
    and gridsearches
    
    The class takes in your Indepdendent Variables X and predictors y, and 
    handles creation of train and test variables.
    '''
    
    def __init__(self, X, y):
        '''
        This creates the X_train, X_test, y_train, y_test arrays
        
        self.X_train
        self.X_test
        self.y_train
        self.y_test
        
        This also creates the simple preprocessing object
        A column transformer with two sides able to automatically handle
        numerical and categeorical data.
        
        Default Numerical Simple Inputter uses strategy 'mean'
        Default Categoerical Simple Inputter uses fill value 'other'
        
        self.preprocessing
        '''
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        
        
        # Below is the basic preprocessing pipeline
         
        
        # https://scikit-learn.org/stable/auto_examples/compose/plot_column_transformer_mixed_types.html
        
        # set up numerical pipeline
        numeric_transformer = Pipeline(steps=[
            ('num_imputer', SimpleImputer(strategy='mean')),
            ('num_scaler', StandardScaler())])
        
        # Set up categorical papeline
        categorical_transformer = Pipeline(steps=[
            ('cat_imputer', SimpleImputer(strategy='constant', fill_value='Other')),
            ('cat_onehot', OneHotEncoder(handle_unknown='ignore')),
            ('cat_scaler', StandardScaler(with_mean=False))])
                                  
        # set up preprocessing column transformer
        preprocessing = ColumnTransformer(transformers=[
            ('num', numeric_transformer, make_column_selector(dtype_include=np.number)),
            ('cat', categorical_transformer, make_column_selector(dtype_include='object'))
        ])
        
        self.preprocessing = preprocessing
        
    def make_pipe(estimator_list, preprocessing=None):
        '''
        Output: List of Pipe Objects
        
        This takes in a list of estimators and a preprocessing pipe object
        It outputs a list of pipes with a preprocessing object and an estimator object
        
        If no preprocessing object is passed, the built in instance will be used
        '''
        if preprocessing == None:
            preprocessing = self.preprocessing
            
        pipe_list = []
        for estimator in estimator_list:
            pipe_list.append(make_pipeline(preprocessing, estimator))
        
        return pipe_list
    
    def make_pipe_wfs(self, feature_sel_list, estimator_list, preprocessing=None):
        '''
        Output: List of Pipe Objects
        
        make_pipe_with feature selection:
        
        This takes in a list of estimators, a list of feature selection objects 
        and a preprocessing pipe object
        It outputs a list of pipes with a preprocessing object, a feature selection process 
        and an estimator object
        
        If no preprocessing object is passed, the built in instance will be used
        '''
        if preprocessing == None:
            preprocessing = self.preprocessing
            
        pipe_list = []
        for estimator in estimator_list:
            for feature in feature_sel_list:
                pipe_list.append(make_pipeline(preprocessing, VarianceThreshold(), feature, estimator))
        
        return pipe_list        
        
    
    def evaluate_pipes(self, pipe_list):
        '''
        Output: List of Testing Accuracy Scores, List of Fitted Pipe Objects
        
        This evaluates each pipe object in a list and returns back a list of 
        scores and best params
        It takes in two X and Y, uses train_test_split to separate into 4 different arrays
        Then it evaluates each model on a test set and measures the accuracy
        The function returns the list of scores and the list of fitted pipe objects
        '''
        
        scores = []
        objects = []
        for pipe in pipe_list:
            pipe_object = pipe.fit(self.X_train,self.y_train)
            scores.append(pipe_object.score(self.X_test, self.y_test))
            objects.append(pipe_object)
        return scores, objects
    
    def calculate_rsme(self, fitted_pipe_objects, preprocessing=None):
        '''
        Output: List of Test RSME Scores
        (Root Mean Squared Error)
        
        This takes in a list of fitted pipe objects and then calculates the RSME on the test data
        
        If no preprocessing object is passed, the built in instance will be used
        '''
        if preprocessing == None:
            preprocessing = self.preprocessing
                       
        list_rsme = []
        for pipe in fitted_pipe_objects:
            preds = pipe.predict(self.X_test)
            rsme = mean_squared_error(self.y_test, preds, squared=False)
            list_rsme.append(rsme)
            
        return list_rsme
            
    def make_grid_search(self, estimator_list, params):
        '''
        Outputs: List of Pipe Objects, List of GridSearchCV Objects
        
        This is a function that uses the built in preprocessing pipeline, a list of estimator objects and params
        This returns a list of GridSearchCV Objects
        
        The Pipe object is an artifact of creating GridSearch Object
        
        '''
        
        pipe_array = self.make_pipe(self.preprocessing, estimator_list) 
        grid_array = []
        
        for pipe_object, param in list(zip(pipe_array, params)):
            grid_array.append(
                GridSearchCV(
                    estimator=pipe_object, 
                    param_grid=param,
                    n_jobs=-1))

        return pipe_array, grid_array
        
    def make_grid_search_no_pre(self, estimator_list, params):
        '''
        Output: List of Grid SearchCV Objects without Preprocessing
        
        If you do not want to use preprocessing, use this version of make_grid_search
        
        This takes in a list of estimators and a params argument as a dict
        '''
        
        grid_array = []
        
        for estimator_object, param in list(zip(estimator_list, params)):
            grid_array.append(
                GridSearchCV(
                estimator=estimator_object,
                param_grid = param,
                n_jobs=-1))
        return grid_array
    
    def make_grid_search_wfs(self, feature_list, estimator_list, params, preprocessing=None):
        '''
        Output: List of Pipe Objects, List of GridSearchCV objects
        
        This is a function that takes in a preprocessing pipeline, 
        a list of estimator objects and a list of params where each element is a dict
        
        This returns a list of pipe objects and a list of gridsearchcv objects
        
        If no preprocessing object is passed, the built in instance will be used
        '''
        if preprocessing == None:
            preprocessing = self.preprocessing
        
        pipe_array = self.make_pipe_wfs(preprocessing, feature_list, estimator_list) 
        grid_array = []
        
        for pipe_object, param in list(zip(pipe_array, params)):
            grid_array.append(
                GridSearchCV(
                    estimator=pipe_object, 
                    param_grid=param,
                    n_jobs=-1))

        return pipe_array, grid_array
    
    def evaluate_grid_search(self, grid_list):
        '''
        Output: List of Accuracy Test Score, List of Fitted GridSearchCV Object
        
        This takes in a list of GridSearchCV objects and fits them to the assigned train variables
        A list of accuracy scores for each estimator and the list of objects is returned 
        '''
        scores = []
        objects = []
        
        for grid in grid_list:
            grid_object = grid.fit(self.X_train, self.y_train)
            scores.append(grid.score(self.X_test, self.y_test))
            objects.append(grid_object)
        
        return scores, objects
    
    def predictions(fitted_object, test_data, to_file=False):
        '''
        Output: Model Predictions
        
        This takes in a single fitted object like a fitted pipeline or a fitted gridsearchcv object
        The output format is in the Kaggle Required documents.
        
        See the competition here: https://www.kaggle.com/c/ga-dsir-824-project-2-regression-challenge/leaderboard#score
        
        If to_file=True, it will output the Dataframe as a csv, ignoring the index and 
        place the csv file into your current working directory
        '''
        predictions = fitted_object.predict(test_data)
        predictions = pd.DataFrame(predictions)
        predictions = predictions.rename({0:'SalePrice'}, axis=1)
        predictions = predictions.join(df_test['Id'])
        predictions = predictions[['Id', 'SalePrice']]
        
        if to_file == True:
            predictions.to_csv('predictions.csv', index=False)
            return predictions
        else:
            return predictions
       