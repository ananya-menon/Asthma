# -*- coding: utf-8 -*-
"""Asthma_Bhavana.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1o2RAV_4JTZBu53KvB17H92FkXH3iaMn2
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.pyplot import figure
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import pickle
import sklearn
import scipy

 
sns.set()


df=pd.read_csv('asthma dataset.csv') 
#dataset=df.values

#for fn in uploaded.keys():
#  print('user uploaded file "{name}" with length {length} bytes'.format(
#      name=fn, length=len(uploaded[fn])))

#uploaded

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

df.shape

df.head()

df.tail()

df.shape

df.info()

df.describe().T

print(df.isnull().values.any())
df = df.dropna()
print(df.isnull().values.any())

def plot_corr(df, size=11):
    """
    Function plots a graphical correlation matrix for each pair of columns in the dataframe.

    Input:
        df: pandas DataFrame
        size: vertical and horizontal size of the plot

    Displays:
        matrix of correlation between columns.  Blue-cyan-yellow-red-darkred => less to more correlated
                                                0 ------------------>  1
                                                Expect a darkred line running from top left to bottom right
    """

    corr = df.corr()    # data frame correlation function
    fig, ax = plt.subplots(figsize=(size, size))
    ax.matshow(corr)   # color code the rectangles by correlation value
    plt.xticks(range(len(corr.columns)), corr.columns)  # draw x tick marks
    plt.yticks(range(len(corr.columns)), corr.columns)  # draw y tick marks

import seaborn as sns

plt.figure(figsize=(10,10))
sns.heatmap(df.corr(), annot = True, cmap = "Greens")
plt.show()

df.corr()

# for feature in data_feature:
#     plt.hist(data[feature])
#     plt.show()
#p = df.hist(figsize = (10,10))
df=df.drop(['VAX_TYPE'],axis=1) 
asthma_map = {True : 1, False : 0}
df['ASTHMA'] = df['ASTHMA'].map(asthma_map)

sleep_map = {True : 1, False : 0}
df['SLEEPING_PROB'] = df['SLEEPING_PROB'].map(sleep_map)

chest_map = {True : 1, False : 0}
df['CHEST_TIGHTNESS'] = df['CHEST_TIGHTNESS'].map(chest_map)

breath_map = {True : 1, False : 0}
df['BREATH'] = df['BREATH'].map(breath_map)

cough_map = {True : 1, False : 0}
df['COUGH'] = df['COUGH'].map(cough_map)

allergy_map = {True : 1, False : 0}
df['ALLERGY'] = df['ALLERGY'].map(allergy_map)

sex_map = {'M' : 1, 'F' : 0, 'U' : 2}
df['SEX'] = df['SEX'].map(sex_map)

wheezing_map = {True : 1, False : 0}
df['WHEEZING'] = df['WHEEZING'].map(wheezing_map)


#vax_data = df['VAX_TYPE']
#vax=[]
#for items in vax_data:
#    if items in vax:
#        continue
#    else:
        #print(items)
#        vax.append(items)
#print("Vax list: ")
#print(vax)

#key=0
#vax_map={key: value for (key, value) in zip(vax,range(len(vax))) }
#df['VAX_TYPE'] = df['VAX_TYPE'].map(vax_map)

df.head(10)

df.isnull().values.any()

num_obs = len(df)
num_true = len(df.loc[df['ASTHMA'] == 1])
num_false = len(df.loc[df['ASTHMA'] == 0])
print("Number of True cases:  {0} ({1:2.2f}%)".format(num_true, ((1.00 * num_true)/(1.0 * num_obs)) * 100))
print("Number of False cases: {0} ({1:2.2f}%)".format(num_false, (( 1.0 * num_false)/(1.0 * num_obs)) * 100))

from sklearn.model_selection import train_test_split

feature_col_names = ['AGE_YRS', 'SEX', 'SLEEPING_PROB', 'CHEST_TIGHTNESS', 'BREATH', 'COUGH', 'ALLERGY','WHEEZING']
predicted_class_names = ['ASTHMA']

X = df[feature_col_names].values     # predictor feature columns (8 X m)
y = df[predicted_class_names].values # predicted class (1=true, 0=false) column (1 X m)
split_test_size = 0.30

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split_test_size, random_state=42) 
                            # test_size = 0.3 is 30%, 42 is the answer to everything

#from sklearn.preprocessing import MinMaxScaler 
#from sklearn.preprocessing import StandardScaler 
#scaler=StandardScaler()
#scaler.fit(df) 
#scaled_data=scaler.transform(df) 
#scaled_data

#from sklearn.decomposition import PCA 

#pca=PCA(n_components=2) 

#pca.fit(scaled_data) 
#x_pca=pca.transform(scaled_data)

#scaled_data.shape

#x_pca.shape

from sklearn.model_selection import train_test_split 
print (y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

trainval = (1.0 * len(X_train)) / (1.0 * len(df.index))
testval = (1.0 * len(X_test)) / (1.0 * len(df.index))
print("{0:0.2f}% in training set".format(trainval * 100))
print("{0:0.2f}% in test set".format(testval * 100))

print("Original True  : {0} ({1:0.2f}%)".format(len(df.loc[df['ASTHMA'] == 1]), (len(df.loc[df['ASTHMA'] == 1])/len(df.index)) * 100.0))
print("Original False : {0} ({1:0.2f}%)".format(len(df.loc[df['ASTHMA'] == 0]), (len(df.loc[df['ASTHMA'] == 0])/len(df.index)) * 100.0))
print("")
print("Training True  : {0} ({1:0.2f}%)".format(len(y_train[y_train[:] == 1]), (len(y_train[y_train[:] == 1])/len(y_train) * 100.0)))
print("Training False : {0} ({1:0.2f}%)".format(len(y_train[y_train[:] == 0]), (len(y_train[y_train[:] == 0])/len(y_train) * 100.0)))
print("")
print("Test True      : {0} ({1:0.2f}%)".format(len(y_test[y_test[:] == 1]), (len(y_test[y_test[:] == 1])/len(y_test) * 100.0)))
print("Test False     : {0} ({1:0.2f}%)".format(len(y_test[y_test[:] == 0]), (len(y_test[y_test[:] == 0])/len(y_test) * 100.0)))

from sklearn.preprocessing import StandardScaler  
scaler = StandardScaler()  
scaler.fit(X_train)

X_train = scaler.transform(X_train)  
X_test = scaler.transform(X_test)

from sklearn.naive_bayes import GaussianNB

# create Gaussian Naive Bayes model object and train it with the data
nb_model = GaussianNB()

nb_model.fit(X_train, y_train.ravel())

from sklearn import metrics

# this returns array of predicted results
prediction_from_trained_data = nb_model.predict(X_train)
accuracy = metrics.accuracy_score(y_train, prediction_from_trained_data)

print("Accuracy of our train naive bayes model is : {0:.4f}".format(accuracy))

# this returns array of predicted results from test_data
prediction_from_test_data = nb_model.predict(X_test)

accuracy = metrics.accuracy_score(y_test, prediction_from_test_data)

print("Accuracy of our test naive bayes model is: {0:0.4f}".format(accuracy))

print("Confusion Matrix")

# labels for set 1=True to upper left and 0 = False to lower right
print("{0}".format(metrics.confusion_matrix(y_test, prediction_from_test_data, labels=[1, 0])))

print("Classification Report")

# labels for set 1=True to upper left and 0 = False to lower right
print("{0}".format(metrics.classification_report(y_test, prediction_from_test_data, labels=[1,0])))

# fpr, tpr
import numpy as np
#import matplotlib.pyplot as plt

naive_bayes = np.array([0, 0.66])

# plotting
plt.scatter(naive_bayes[0], naive_bayes[1], label = 'Naive Bayes', facecolors='black', edgecolors='orange', s=300)

plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([-0.02, 1.0])
plt.ylim([0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic curve')
plt.legend(loc='lower center')

plt.show()

from sklearn.linear_model import LogisticRegression

lr_model = LogisticRegression(C=0.7, random_state=50)
lr_model.fit(X_train, y_train.ravel())

lr_predict_train = lr_model.predict(X_train)

#get accuracy
from sklearn import metrics
lr_accuracy = metrics.accuracy_score(y_train, lr_predict_train)

#print accuracy
from sklearn import metrics
print("\nLR performance on Training Data:")
print("Accuracy: {0:.4f}\n".format(lr_accuracy))


lr_predict_test = lr_model.predict(X_test)

#get accuracy
lr_accuracy_testdata = metrics.accuracy_score(y_test, lr_predict_test)

#print accuracy
print("LR performance on Test Data:")
print("Accuracy: {0:.4f}\n".format(lr_accuracy_testdata))

from sklearn.metrics import classification_report, confusion_matrix 

print("Confusion Matrix for LR")
print("{0}".format(confusion_matrix(y_test,lr_predict_test,labels=[1,0])))  

print("\nClassification Report")
print("{0}".format(classification_report(y_test,lr_predict_test, labels=[1, 0])))

import numpy as np
#import matplotlib.pyplot as plt


logistic = np.array([0.003, 0.68])

# plotting
plt.scatter(logistic[0], logistic[1], label = 'Logistic Regression', facecolors='orange', edgecolors='orange', s=300)

plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([-0.02, 1.0])
plt.ylim([0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic curve')
plt.legend(loc='lower center')

plt.show()

from sklearn.neural_network import MLPClassifier  
mlp = MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=1000)  
mlp.fit(X_train, y_train.ravel())

from sklearn import metrics
print("ANN performance on Training Data:")
print("Accuracy: {0:.4f}\n".format(metrics.accuracy_score(y_train, mlp.predict(X_train))))

predictions = mlp.predict(X_test)  
print("ANN performance on Test Data:")
print("Accuracy: {0:.4f}\n".format(metrics.accuracy_score(y_test, predictions)))

from sklearn.metrics import classification_report, confusion_matrix 

print("Confusion Matrix for Artificial Neural Network")
print("{0}".format(confusion_matrix(y_test,predictions,labels=[1,0])))  

print("\nClassification Report")
print("{0}".format(classification_report(y_test,predictions, labels=[1, 0])))

import numpy as np
#import matplotlib.pyplot as plt

ann = np.array([0.006,0.70 ])

# plotting
plt.scatter(ann[0], ann[1], label = 'Artificial Neural Network', facecolors='red', edgecolors='black', s=300)

plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([-0.02, 1.0])
plt.ylim([0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic curve')
plt.legend(loc='lower center')

plt.show()

from sklearn.ensemble import RandomForestClassifier

# Create a RandomForestClassifier object
rf_model = RandomForestClassifier(random_state=42)

rf_model.fit(X_train, y_train.ravel())

#get accuracy
from sklearn import metrics
rf_predict_train = rf_model.predict(X_train)
rf_accuracy = metrics.accuracy_score(y_train, rf_predict_train)

#print accuracy
from sklearn import metrics
print("\nRF performance on Training Data:")
print("Accuracy: {0:.4f}\n".format(rf_accuracy))

rf_predict_test = rf_model.predict(X_test)

#get accuracy
rf_accuracy_testdata = metrics.accuracy_score(y_test, rf_predict_test)

#print accuracy
print("RF performance on Test Data:")
print("Accuracy: {0:.4f}\n".format(rf_accuracy_testdata))

from sklearn.metrics import classification_report, confusion_matrix 

print("Confusion Matrix for RF")
print("{0}".format(confusion_matrix(y_test,rf_predict_test,labels=[1,0])))  

print("\nClassification Report")
print("{0}".format(classification_report(y_test,rf_predict_test, labels=[1, 0])))

# fpr, tpr
import numpy as np
#import matplotlib.pyplot as plt

random_forest = np.array([0.017,0.73])


# plotting
plt.scatter(random_forest[0], random_forest[1], label = 'Random Forest', facecolors='blue', edgecolors='black', s=300)

plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([-0.02, 1.0])
plt.ylim([0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic curve')
plt.legend(loc='lower center')

plt.show()

from sklearn.tree import DecisionTreeClassifier

# Create a DecisionTreeClassifier object
dt_model = RandomForestClassifier(criterion='entropy',random_state=42)

dt_model.fit(X_train, y_train.ravel())

#get accuracy
from sklearn import metrics
dt_predict_train = rf_model.predict(X_train)
dt_accuracy = metrics.accuracy_score(y_train, dt_predict_train)

#print accuracy
from sklearn import metrics
print("\nDT performance on Training Data:")
print("Accuracy: {0:.4f}\n".format(dt_accuracy))

dt_predict_test = dt_model.predict(X_test)

#get accuracy
dt_accuracy_testdata = metrics.accuracy_score(y_test, dt_predict_test)

#print accuracy
print("DT performance on Test Data:")
print("Accuracy: {0:.4f}\n".format(dt_accuracy_testdata))

from sklearn.metrics import classification_report, confusion_matrix 

print("Confusion Matrix for RF")
print("{0}".format(confusion_matrix(y_test,dt_predict_test,labels=[1,0])))  

print("\nClassification Report")
print("{0}".format(classification_report(y_test,dt_predict_test, labels=[1, 0])))

# fpr, tpr
import numpy as np
#import matplotlib.pyplot as plt

decision_tree = np.array([0.017,0.73])


# plotting
plt.scatter(decision_tree[0], random_forest[1], label = 'Decision Tree', facecolors='lavender', edgecolors='black', s=300)

plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([-0.02, 1.0])
plt.ylim([0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic curve')
plt.legend(loc='lower center')

plt.show()

# fpr, tpr
import numpy as np
#import matplotlib.pyplot as plt

naive_bayes = np.array([0, 0.66])
logistic = np.array([0.003, 0.68])
ann = np.array([0.006,0.70 ])
random_forest = np.array([0.017,0.73])
decision_tree = np.array([0.026,1.02])


# plotting
plt.scatter(naive_bayes[0], naive_bayes[1], label = 'Naive Bayes', facecolors='black',
            edgecolors='orange', s=300)
plt.scatter(logistic[0], logistic[1], label = 'Logistic Regression', facecolors='orange',
            edgecolors='orange', s=300)
plt.scatter(random_forest[0], random_forest[1], label = 'Random Forest', facecolors='blue',
           edgecolors='black', s=300)
plt.scatter(ann[0], ann[1], label = 'Artificial Neural Network', facecolors='red',
            edgecolors='black', s=300)
plt.scatter(decision_tree[0], random_forest[1], label = 'decision_tree', facecolors='lavender',
           edgecolors='black', s=300)

plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([-0.02, 1.0])
plt.ylim([0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic curve')
plt.legend(loc='lower center')

plt.show()

#Naive:

#Train score : 0.94309676923076923
#Test score : 0.940179487179487
#----------------------------------------------------------------------------------------------------
#logistic Regression:

#Train score : 1.00
#Test score : 1.00
#----------------------------------------------------------------------------------------------------
#ANN:

#Train score :1.00
#Test score : 0.9993569230769231
#----------------------------------------------------------------------------------------------------
#Random Forest:

#Train score : 1.00
#Test score : 0.9978369230769231
#----------------------------------------------------------------------------------------------------
#Decision Tree:

#Train score : 1.00
#Test score : 0.9978769230769231
#----------------------------------------------------------------------------------------------------

import pickle
filename = 'Asthma.pkl' 
pickle.dump(lr_model, open(filename, 'wb'))