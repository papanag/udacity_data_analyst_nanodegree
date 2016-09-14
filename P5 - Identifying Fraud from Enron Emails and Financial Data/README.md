# Project 5: Identifying Fraud from Enron Emails and Financial Data

In 2000, Enron was one of the largest companies in the United States. By 2002, it had collapsed into bankruptcy due to widespread corporate fraud. In the resulting Federal investigation, a significant amount of typically confidential information entered into the public record, including tens of thousands of emails and detailed financial data for top executives.

In this project, we will be using machine learning to identify persons of interest based on data sources publicly available.


## Data Exploration
The dataset contains **146 data points** with **21 features**, from which only **18 are labeled as persons of interest**. Arguably the most important characteristic of the dataset is the disproportion of class distribution.

After thorough inspection, we find that all features (except target feature "poi") have missing values. Moreover, we find that POIs show different percentages of missing values. Thus, a classification algorithm might interpret “NaN” for these features as a clue that someone is a POI or not. We should mitigate this bias before building our model.

```
feature name                 NaNs % of total    NaNs % of pois    NaNs % difference
-------------------------  -----------------  ----------------  -------------------
poi                                     0                 0                    0
deferral_payments                       0.73              0.72                 0.01
exercised_stock_options                 0.3               0.33                 0.03
loan_advances                           0.97              0.94                 0.03
restricted_stock_deferred               0.88              1                    0.12
director_fees                           0.88              1                    0.12
total_payments                          0.14              0                    0.14
total_stock_value                       0.14              0                    0.14
to_messages                             0.41              0.22                 0.19
restricted_stock                        0.25              0.06                 0.19
shared_receipt_with_poi                 0.41              0.22                 0.19
from_messages                           0.41              0.22                 0.19
from_this_person_to_poi                 0.41              0.22                 0.19
from_poi_to_this_person                 0.41              0.22                 0.19
long_term_incentive                     0.55              0.33                 0.21
email_address                           0.24              0                    0.24
deferred_income                         0.66              0.39                 0.28
salary                                  0.35              0.06                 0.29
bonus                                   0.44              0.11                 0.33
expenses                                0.35              0                    0.35
other                                   0.36              0                    0.36 
```

Next, we identify outliers for each financial feature by spotting data points with values beyond 3 s.d. from each feature mean. Alternatively, we could have sketched scatter plots and visually chosen the outliers, but this is not viable for a big number of features.

```
feature name               dict key              value
-------------------------  ----------------  ---------
salary                     TOTAL              26704229
deferral_payments          TOTAL              32083396
total_payments             LAY KENNETH L     103559793
total_payments             TOTAL             309886585
bonus                      TOTAL              97343619
restricted_stock_deferred  BHATNAGAR SANJAY   15456290
deferred_income            TOTAL             -27992891
total_stock_value          TOTAL             434509511
expenses                   TOTAL               5235198
exercised_stock_options    TOTAL             311764000
other                      TOTAL              42667589
long_term_incentive        TOTAL              48521928
restricted_stock           TOTAL             130322299
director_fees              TOTAL               1398517 
```

It is obvious that most outliers correspond to the name "TOTAL", which is an artifact from the imported spreadsheet, and thus, they must be taken out. The two other outliers seem to be valid data points, as they correspond to actual names. Indeed, after removing this outlier that stands out the most, the scores of our model are improved.

Moreover, given the small size of this dataset, a manual check can really help to get a good feel for the data and spot anything unusual. There were 2 other outliers that were not identified, "THE TRAVEL AGENCY IN THE PARK" and "LOCKHART EUGENE E". The first one is clearly not a person, therefore it is not a valid datapoint, and the second one after inspecting it only contains "NaN", therefore it does not add value to the model. Even though the scores of our model are a bit lower if we exclude these observations, we must do so to preserve its correctness and generality.

After having the outliers removed, we can decide the imputation of missing values by checking the score via cross-validation. The score with the entire dataset is 0.86 and the score after imputation with median values is 0.85. Thus, we do not perform any replacement of missing values.


## Feature Selection
From the 21 features in our dataset, one is the label ("poi") and another is the actual email address as text ("email_address"). The rest 19 features are candidates to include in our model. There is no need for any further preprocessing, such as conversions due to data type, as all of them take numerical values, or rescaling, as we will not be using any clustering algorithm.

In addition, we implement one more feature named "poi_correspondence", which aggregates the related fields "from_this_person_to_poi", "from_poi_to_this_person" and "shared_receipt_with_poi". This is intended to gauge the strength of connection with pois.

We assess the effect of all features with selectKbest algorithm. The results of the F test for each feature and the correspondent p-value are shown below.

```
feature name                   p-value     F value
-------------------------  -----------  ----------
exercised_stock_options    1.8182e-06   24.8151
total_stock_value          2.40432e-06  24.1829
bonus                      1.1013e-05   20.7923
salary                     3.47827e-05  18.2897
deferred_income            0.000922037  11.4585
long_term_incentive        0.00199418    9.92219
restricted_stock           0.0028628     9.21281
total_payments             0.00358933    8.77278
poi_correspondence         0.00389064    8.61665
shared_receipt_with_poi    0.0039458     8.58942
loan_advances              0.00823185    7.18406
expenses                   0.0147582     6.09417
from_poi_to_this_person    0.0235139     5.24345
other                      0.0425817     4.18748
from_this_person_to_poi    0.124934      2.38261
director_fees              0.147011      2.12633
to_messages                0.201563      1.64634
deferral_payments          0.636282      0.224611
from_messages              0.681003      0.169701
restricted_stock_deferred  0.798379      0.0654997 
```

To avoid any arbitrary selection of k, we keep all features with p-value < 0.05 (14 out of 20 features).


## Algorithm Selection and Tuning
We test three different classification algorithms, one of which is an ensemble method. To choose between them, we split the dataset in train and test data, and then we use as metric the precision and recall scores. Also, we use GridSearchCV for parameter tuning on each algorithm during the selection, and thus, we are comparing the best version of each algorithm. 

Parameters are arguments passed when the classifier is created, before fitting, and thus they can make a huge difference in the decision boundary that the algorithm arrives at. For this reason, if the parameters are not set appropriately, the decision boundary might end up very complicated and then the model is overfitted and performs very poorly.

```
GaussianNB
precision: 0.4
recall: 0.4
```

```
DecisionTreeClassifier
precision: 0.33
recall: 0.4

Best estimator found by grid search: DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=None,
            max_features=None, max_leaf_nodes=None, min_samples_leaf=10,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            presort=False, random_state=None, splitter='best')
```

```
RandomForestClassifier
precision: 0.0
recall: 0.0

Best estimator found by grid search: RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            max_depth=1, max_features='auto', max_leaf_nodes=10,
            min_samples_leaf=5, min_samples_split=5,
            min_weight_fraction_leaf=0.05, n_estimators=10, n_jobs=1,
            oob_score=False, random_state=None, verbose=0,
            warm_start=False)
```

Naive Bayes achieves a satisfying score on both metrics. On the contrary, Random Forest achieves very small scores (it is improbable the values to be exactly 0, and this may be an artifact of the small size of the dataset). Consequently, we choose GaussianNB. We note also that this algorithm does not require any parameter setting.


## Validation and Evaluation
We have used precision and recall scores to evaluate and select our model.

Accuracy is defined as the fraction of correct predictions. It is not ideal for skewed data, and thus it is not a suitable metric for this dataset, as the number of given POIs is very small.

The precision is the ratio `tp / (tp + fp)` where `tp` is the number of true positives and `fp` the number of false positives. Precision measures the ability of the classifier to avoid false positives, namely to identify as POIs some non-POIs.

The recall is the ratio `tp / (tp + fn)` where `tp` is the number of true positives and `fn` the number of false negatives. Recall measures the ability of the classifier to find all the positive samples, in other words to find all POIs. 

Validation is the process of testing the performance of a trained model on a test set. It serves as check for overfitting, and thus it gives an estimate of the performance on an independent dataset.

In the previous section we used a tentative score of precision and recall to select the best algorithm. Nevertheless, these scores may not be accurate, as they were obtained by splitting one time the given dataset in train and test data. In the given tester function, there is being made use of the class StratifiedShuffleSplit, which provides stratified randomized folds for training and testing. As a result, the obtained scores represent more correctly the predictive power of our model.

```
Accuracy: 0.81747
Precision: 0.31173
Recall: 0.30550
```

Indeed, the scores of precision and recall happen to be lower than our first results, but they are above the required 0.3 limit.

