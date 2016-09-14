#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi'] # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


### Data Exploration
print "number of data points:", len(data_dict)

poi = 0
for key in data_dict:
	if data_dict[key]["poi"]==1:
		poi += 1
print "number of POIs:", poi

print "number of features:", len(data_dict.values()[0])

table_nans = []
for feature in data_dict.values()[0]:
	i = 0
	k = 0
	for key in data_dict:
		if data_dict[key][feature]=='NaN':
			i += 1
			if data_dict[key]["poi"]==1:
				k += 1
	feature_nans = i / float(len(data_dict))
	pois_nans = k / float(poi)
	table_nans.append([feature, "%.2f" % feature_nans, "%.2f" % pois_nans, "%.2f" % abs(feature_nans-pois_nans)])

from operator import itemgetter
table_nans = sorted(table_nans, key=itemgetter(3))

from tabulate import tabulate
print "\n***** find NaNs *****"
print tabulate(table_nans, headers=["feature name","NaNs % of total", "NaNs % of pois", "NaNs % difference"]), "\n"


### Task 2: Remove outliers
financial_features = ['salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees']

# exclude feature "email_address" from the list of email features
email_features = ['to_messages', 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi']

features_list = email_features + financial_features
import numpy as np

# calculate mean and sd for each feature
features_mean = {}
features_sd = {}
for feature in features_list:
	features_mean[feature] = np.nanmean([float(i[feature]) for i in data_dict.values()])
	features_sd[feature] = np.nanstd([float(i[feature]) for i in data_dict.values()])

# find outliers
table_outliers = []
for feature in financial_features:
	for key in data_dict:
		if data_dict[key][feature] != 'NaN':
			if abs(data_dict[key][feature] - features_mean[feature]) > 3 * features_sd[feature]:
				table_outliers.append([feature, key, data_dict[key][feature]])

print "\n***** find outliers *****"
print tabulate(table_outliers, headers=["feature name","dict key", "value"]), "\n"

# remove outliers
data_dict.pop('TOTAL')

# after a manual check 2 more outliers were identified
data_dict.pop('THE TRAVEL AGENCY IN THE PARK')
data_dict.pop('LOCKHART EUGENE E')


# calculate new measures of central tendency (after removing outliers), to use in manual imputation
# features_median = {}
# for feature in features_list:
# 	features_median[feature] = np.nanmedian([float(i[feature]) for i in data_dict.values()])

# check score via cross-validation to decide imputation of missing values
from sklearn.ensemble import RandomForestClassifier
estimator = RandomForestClassifier(random_state=0, n_estimators=100)
from sklearn.cross_validation import cross_val_score

import copy
features_list = ['poi'] + email_features + financial_features

# Store to my_dataset for easy export below.
my_dataset = copy.deepcopy(data_dict)

# Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

score = cross_val_score(estimator, features, labels).mean()
print("Score with the entire dataset = %.2f" % score)

# Store to my_dataset for easy export below.
my_dataset = copy.deepcopy(data_dict)

# impute missing values manually
# for feature in features_list:
# 	for key in my_dataset:
# 		if my_dataset[key][feature] == 'NaN':
# 			my_dataset[key][feature] = features_median[feature]

# Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, remove_NaN = False, sort_keys = True)
labels, features = targetFeatureSplit(data)

# OR impute missing values using Imputer
from sklearn.preprocessing import Imputer
imp = Imputer(missing_values='NaN', strategy='median')
features = imp.fit_transform(features)

score = cross_val_score(estimator, features, labels).mean()
print("Score after imputation of the missing values = %.2f" % score)


### Task 3: Create new feature(s)
# Store to my_dataset for easy export below.
my_dataset = copy.deepcopy(data_dict)

# create new features
for key in my_dataset:
	if(my_dataset[key]['from_poi_to_this_person']=='NaN' or my_dataset[key]['from_this_person_to_poi']=='NaN' or my_dataset[key]['shared_receipt_with_poi']=='NaN'):
		my_dataset[key]['poi_correspondence'] = 'NaN'
	else:
		my_dataset[key]['poi_correspondence'] = my_dataset[key]['from_poi_to_this_person'] + my_dataset[key]['from_this_person_to_poi'] + my_dataset[key]['shared_receipt_with_poi']

new_features = ['poi_correspondence']

# feature selection
features_list = ['poi'] + email_features + financial_features + new_features

# Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

from sklearn.feature_selection import SelectKBest
k_best = SelectKBest(k='all')
k_best.fit(features, labels)

# remove first feature, which is the label
features_list.pop(0)

table_features = zip(features_list, k_best.pvalues_, k_best.scores_)
table_features = sorted(table_features, key=itemgetter(1))

print "\n***** select features *****"
print tabulate(table_features, headers=["feature name", "p-value", "F value"]), "\n"

# select features having p<0.05 in F test
features_list = np.array(features_list)
features_list = features_list[k_best.pvalues_<.05]
print "number of selected features:", len(features_list)
features_list = features_list.tolist()

# Extract features and labels from dataset for local testing
# again to include only selected features
features_list = ['poi'] + features_list
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)


### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

from sklearn.grid_search import GridSearchCV

# Split into a training and testing set
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

def tune_clf(clf, param_grid):
	if bool(param_grid)==True:
		clf = GridSearchCV(clf, param_grid)

	clf = clf.fit(features_train, labels_train)

	labels_pred = clf.predict(features_test)

	from sklearn.metrics import accuracy_score, precision_score, recall_score
	print "precision:", precision_score(labels_test, labels_pred)
	print "recall:", recall_score(labels_test, labels_pred)
	if hasattr(clf, 'best_estimator_'):
		print "Best estimator found by grid search:", clf.best_estimator_


print "\n***** algorithm tuning and selection *****"

print "\nGaussianNB"
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
param_grid = {}
tune_clf(clf, param_grid)

print "\nDecisionTreeClassifier"
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier()
param_grid = {
	'criterion': ['gini', 'entropy'],
	'max_depth': [None, 1, 5, 10],
	'min_samples_split': [2, 5, 10],
	'min_samples_leaf': [1, 5, 10],
	'min_weight_fraction_leaf': [0., .05, .1],
	'max_leaf_nodes': [None, 5, 10, 20]
	}
tune_clf(clf, param_grid)

print "\nRandomForestClassifier"
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier()
param_grid = {
	'criterion': ['gini', 'entropy'],
	'max_depth': [None, 1, 5, 10],
	'min_samples_split': [2, 5, 10],
	'min_samples_leaf': [1, 5, 10],
	'min_weight_fraction_leaf': [0., .05, .1],
	'max_leaf_nodes': [None, 5, 10, 20]
	}
tune_clf(clf, param_grid)


### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()


### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)