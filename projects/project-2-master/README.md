banner image

# Predicting the Sale Price of Properities in Ames, Iowa
---
The [Ames Housing Dataset](http://www.amstat.org/publications/jse/v19n3/decock.pdf) is a data set of 2930 descrete observations and a large number of explantory values (23 nominal, 23 ordinal, 14 discrete, and 20 continuous) involved in assessing home values. [^fn1]

At my time at General Assembly, this was the first major project involving any type of Machine Learning through the use of traditional methods such as Linear Regression, KNearestNeighbors and ElasticNet. 

There was huge emphasis on learning automation techniques such as pipelines and exhaustive hyperparameter searching. A batch of (50 * 50 * 19 * 20) has been suscessfully executed, taking 24hr to return accuracy scores and the fitted model. 

## Problem Statement:
---

### Given attributes of a property can we predict a sale price?

Is there a quantiable relationship that can be identified between the observations and explantory values of a home?

Null Hypothesis: There is no relationship between the data and the sale price in Ames, Iowa.

Alternative Hypothesis: There is a quantiable relationship between the data and the sale price of homes in Ames, Iowa

## Summary:
---

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
---
Information about the data can be found [here]() in the data description and in the data dictionary below.

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
---

We can reject the null hypothesis because there is a quantifiable relationship between the dataset and the predictors.

![qual]()

![quan]()

## File Structure:

```bash


```

## Data Dictionary:
Data Name | Detailed Description | Data Type | 
----------|----------------------|-----------| 
MSSubClass| Identifies the type of dwelling involved in the sale | int |
MSZoning| Identifies the general zoning classification of the sale | str |
LotFrontage| Linear feet of street connected to property | int |
LotArea| Lot size in square feet|int|
Street| Type of road access to property|str|
Alley| Type of alley access to property|str
LotShape| General shape of property|str
LandContour| Flatness of the property|str
Utilities| Type of utilities available|str
LotConfig| Lot configuration|str
LandSlope| Slope of property|str
LandSlope| Slope of property|str
LandSlope| Slope of property|str
Condition2| Proximity to various conditions (if more than one is present)|str
BldgType| Type of dwelling|str
HouseStyle| Style of dwelling|str
OverallQual| Rates the overall material and finish of the house|int
YearRemodAdd| Remodel date (same as construction date if no remodeling or additions|int
RoofMatl| Roof material|str
Exterior1st| Exterior covering on house|str
Exterior2nd| Exterior covering on house (if more than one material)|str
MasVnrType| Masonry veneer type|str
MasVnrArea| Masonry veneer area in square feet|int
ExterQual| Evaluates the quality of the material on the exterior |str
ExterCond| Evaluates the present condition of the material on the exterior|str
Foundation| Type of foundation|str
BsmtQual| Evaluates the height of the basement|str
BsmtCond| Evaluates the general condition of the basement|str
BsmtExposure| Refers to walkout or garden level walls|str
BsmtFinType1| Rating of basement finished area|str
BsmtFinSF1| Type 1 finished square feet|int
BsmtFinType2| Rating of basement finished area (if multiple types)|int
BsmtFinSF2| Type 2 finished square feet|int
BsmtUnfSF| Unfinished square feet of basement area|int
TotalBsmtSF| Total square feet of basement area|int
Heating| Type of heating|str
HeatingQC| Heating quality and condition|str
CentralAir| Central air conditioning|str
Electrical| Electrical system|str
1stFlrSF| First Floor square feet|int
2ndFlrSF| Second floor square feet|int
LowQualFinSF| Low quality finished square feet (all floors)|int
GrLivArea| Above grade (ground) living area square feet|int
BsmtFullBath| Basement full bathrooms|int
BsmtHalfBath| Basement half bathrooms|int
FullBath| Full bathrooms above grade|int
HalfBath| Half baths above grade|int
Bedroom| Bedrooms above grade (does NOT include basement bedrooms)|int
Kitchen| Kitchens above grade|int
KitchenQual| Kitchen quality|str
TotRmsAbvGrd| Total rooms above grade (does not include bathrooms)|int
Functional| Home functionality (Assume typical unless deductions are warranted)|str
Fireplaces| Number of fireplaces|int
FireplaceQu| Fireplace quality|str
GarageType| Garage location|str
GarageYrBlt| Year garage was built|int
GarageFinish| Interior finish of the garage|str
GarageCars| Size of garage in car capacity|int
GarageArea| Size of garage in square feet|int
GarageQual| Garage quality|str
GarageCond| Garage condition|str
PavedDrive| Paved driveway|str
WoodDeckSF| Wood deck area in square feet|int
OpenPorchSF| Open porch area in square feet|int
3SsnPorch| Three season porch area in square feet|int
ScreenPorch| Screen porch area in square feet|int
PoolArea| Pool area in square feet|int
PoolQC| Pool quality|str
Fence| Fence quality|str
MiscFeature| Miscellaneous feature not covered in other categories|str
MiscVal| Value of miscellaneous feature|int
MoSold| Month Sold (MM)|int
YrSold| Year Sold (YYYY)|int
SaleType| Type of sale| str
SaleType| Type of sale|str


## References:
[^fn1]: Cock, Dean De, "Ames, Iowa: Alternative to the Boston Housing Data as an End of Semester Regression Project", Journal of Statistics Education, Volume 19, Number 3(2011)