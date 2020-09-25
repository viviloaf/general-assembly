banner image

# Predicting the Sale Price of Properities in Ames, Iowa
The [Ames Housing Dataset](http://www.amstat.org/publications/jse/v19n3/decock.pdf) is a data set of 2930 descrete observations and a large number of explantory values (23 nominal, 23 ordinal, 14 discrete, and 20 continuous) involved in assessing home values. [^fn1]

At my time at General Assembly, this was the first major project involving any type of Machine Learning through the use of traditional methods such as Linear Regression, KNearestNeighbors and ElasticNet. 

There was huge emphasis on learning automation techniques such as pipelines and exhaustive hyperparameter searching. A batch of (50 * 50 * 19 * 20) has been suscessfully executed, taking 24hr to return accuracy scores and the fitted model. 

## Problem Statement:

### Given attributes of a property can we predict a sale price?

Is there a quantiable relationship that can be identified between the observations and explantory values of a home?

Null Hypothesis: There is no relationship between the data and the sale price in Ames, Iowa.

Alternative Hypothesis: There is a quantiable relationship between the data and the sale price of homes in Ames, Iowa

## Summary:

This project is the first effort to work with numerical and categoerical data in conjunction. I developed an automated workflow where the project will:

    * Take in raw data, 
    * Conduct Initial Data Analysis and handle null values, 
    * Data Wrangling through standardizing the numerical features, 
    * Conversion of categeorical features to numerical representations
    * Push this into an estimaator
    * Push in a list of estimators into a function for a baseline
    * Push in a list of dictionaries of desired estimators with their accompying parameters into another function
    * Evaluate all the estimators in batch fashion
    * Output the RSME and accuracy scores formatted into a DataFrame, optimized for multi-core preformance; easily reviewable results
    * Create a submittable csv file for Kaggle Submission

## Data and Methodology:
Information about the data can be found [here]() in the data description. Another can be found in the [data dictionary]().

The workflow is split into 5 distinct parts:

1. Exploratory Data Analysis
    * Independent numerical feature correlation with the predictor
    * Initial data visualizations
    * Manual Feature Selection
    
    
2. Feature Engineering and Feature Selection
    * Visualizing p-scores of independent features with respect to the predictor
    * Assigning a range of potential features that are suspected to have the greatest impact for regression analysis through a classification Chi-2 test and f-classification scores. 
    
    
3. Model Selection
    * Creating a helper class *ModelSelection* to batch run estimator models
    * Evaluating baseline estimator models
        * Estimators: KNeighbors Regression, Lasso, Linear Regression, Logistic Regression, Ridge, Support Vector Regression 
    * Validation through 5 fold cross validation from GridSearchCV()
    * Model Comparison by accuracy score on test dataset
    * Model Comparison by RSME (Root Mean Squared Error) for Kaggle Competition
    
    
4. Production Model Exploration, Predictions, Submissions
    * 4.1 Exploration of production model 1: KNearest Regressors, RSME: 30718
    * 4.2 Exploration of production model 2: Lasso, RSME: 33842
    * 4.3 Exploration of production model 3: Kaggle, RSMLE: 0.33909
    * Predictions to Project 2 Competition: [link](https://www.kaggle.com/c/ga-dsir-824-project-2-regression-challenge/leaderboard#score)
    * Predictions to Ames Kaggle Competition: [link](https://www.kaggle.com/c/house-prices-advanced-regression-techniques/overview)
    


## Findings:

We can reject the null hypothesis because there is a quantifiable relationship between the dataset and the predictors.

![qual]()

![quan]()

## File Structure:

```bash
project-2-master
├── datasets
│   ├── data_description.txt
│   ├── other_kaggle
│   │   ├── data_description.txt
│   │   ├── sample_submission.csv
│   │   ├── test.csv
│   │   └── train.csv
│   ├── sample_sub_reg.csv
│   ├── test.csv
│   └── train.csv
├── images
│   ├── 1200px-Iowa_State_University_seal.svg.png
│   ├── cafe-diem-coffee.jpeg
│   ├── kbestfeatures-numerical.png
│   ├── kbestfeatures.png
│   ├── Numerical Features vs SalePrice.png
│   ├── pairplot.png
│   ├── qual-top20.png
│   ├── quan-top22.png
│   ├── social-media-logo-horiz.jpg
│   └── usda-aphis-logo.jpg
├── main
│   ├── 01_EDA.ipynb
│   ├── 02_Feature_Engineering_KBestFeatures.ipynb
│   ├── model-comparison.ipynb
│   ├── models.py
│   ├── Predictions_kaggle.ipynb
│   ├── Production_Model_Exploration.ipynb
│   ├── __pycache__
│   │   └── models.cpython-38.pyc
│   └── RMSE, 30718.93563.ipynb
├── Nguyen, Vivian, GA, Project 2.pdf
├── other
│   ├── draftboard
│   │   ├── Drafting.ipynb
│   │   ├── failed-prediction.ipynb
│   │   ├── Roughspace.ipynb
│   │   └── Untitled1.ipynb
│   ├── manipulated-datasets
│   │   └── df_train_objects.csv
│   ├── outputted work
│   │   ├── baseline-924.csv
│   │   ├── baseline.csv
│   │   ├── lasso-rsme-22887.joblib
│   │   ├── model-comparison.csv
│   │   ├── overfit-lasso.joblib
│   │   └── whole-dataset-model-comparison.csv
│   └── predictions
│       ├── 0918-1-nguyen.csv
│       ├── 0918-2-nguyen.csv
│       ├── 920-lasso-alpha-20-predictions.csv
│       ├── 920-lasso-predictions-rsme-23328.csv
│       └── 925-lasso-kaggle.csv
├── project.md
├── README.md
└── suggestions.md

```

## Data Dictionary:
Data Name | Detailed Description | Data Type | 
----------|----------------------|-----------| 

## References:
[^fn1]: Cock, Dean De, "Ames, Iowa: Alternative to the Boston Housing Data as an End of Semester Regression Project", Journal of Statistics Education, Volume 19, Number 3(2011)
