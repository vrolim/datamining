#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 20:45:52 2019

@author: Valdi Ferreira
"""

import pandas as pd
import numpy as np
#from sklearn import preprocessing
import matplotlib.pyplot as plt 
plt.rc("font", size=14)
from sklearn.model_selection import train_test_split
#from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import statsmodels.api as sm
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import seaborn as sns


def correlation(dataset, threshold):
    col_corr = set() 
    corr_matrix = dataset.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if (corr_matrix.iloc[i, j] >= threshold) and (corr_matrix.columns[j] not in col_corr):
                colname = corr_matrix.columns[i] 
                col_corr.add(colname)
                if colname in dataset.columns:
                    dataset=dataset.drop(colname, axis=1)
                    print (colname)

def dummer (colunas, dataframe):
    for item_cat in colunas:
        dataframe[item_cat] = dataframe[item_cat].replace(np.nan, dataframe[item_cat].mode(), regex=True)
        replace = dataframe[item_cat].mode()[0]
        dataframe[item_cat] = dataframe[item_cat].fillna(str(replace))
        index=dataframe[item_cat].unique()
        dataframe= pd.concat((dataframe,pd.get_dummies(dataframe[item_cat])),1)
        label_encoder = LabelEncoder()
        dataframe[item_cat] = label_encoder.fit_transform((dataframe[item_cat]).astype(str))
        one_hot_encoder = OneHotEncoder(sparse=False)
        print (dataframe[item_cat].unique())
        dataframe[index] = one_hot_encoder.fit_transform(dataframe[item_cat].values.reshape(-1,1))
        dataframe=dataframe.drop([item_cat], axis=1)
    return dataframe


df=pd.read_csv('out.csv')
#Remove colunas com pouco significado ou já agregadas
df=df.drop(['Month',"Neighbourhood",'Unnamed: 0','ScheduledDay', 'AppointmentDay', 'Week'], axis=1)

df=dummer(["Gender","Day", "Adm_Zone",],df)
#Justa a ordem das colunas após as dummmies serem criadas
dependent_column=df['No-show']
df=df.drop('No-show', axis=1)
df.insert(loc=23, column='No-show', value=dependent_column)

#Retira registros nulos que surgem após as dummies
df=df.dropna()
label_encoder_noshow = LabelEncoder()
df['No-show'] = label_encoder_noshow.fit_transform((df['No-show']).astype(str))

#Handling handcap
mask = (df['Handcap'] != 0)
column_name = 'Handcap'
df.loc[mask, column_name] = 1


#Testa correlação entre as variáveis (Para salvar imagem descomente as linhas)
corr = df.corr()
#plt.figure(figsize=(16, 12))
svm=sns.heatmap(corr)
#fig=svm.get_figure()
#fig.savefig("Mapa de Calor de Correlação das Variáveis") 
correlation (df, 0.9)

#Separa o dataframe em variáveis independentes e dependentes
X = df.loc[:, df.columns != 'No-show']
y = df.loc[:, df.columns == 'No-show']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

#Seleciona as colunas categóricas
categorical_columns=[]
for column in X.columns:
    categorical_columns.append(X.columns.get_loc(column))
    for x in X[column]:
        if (x!=1 and x!=0):
            categorical_columns.remove(X.columns.get_loc(column))
            break
        
#Faz oversampling para balancear as classes
from imblearn.over_sampling import SMOTENC
smote_nc = SMOTENC(categorical_features=categorical_columns, random_state=0)
X_resampled, y_resampled = smote_nc.fit_resample(X_train, y_train.values.ravel())

#Renomeia as colunas após o oversamplig
X_resampled=pd.DataFrame(data=X_resampled)
X_resampled = pd.DataFrame(X_resampled.values , columns=X_train.columns)
y_resampled=pd.DataFrame(data=y_resampled)
y_resampled = pd.DataFrame(y_resampled.values , columns=y_train.columns)

#Exporta os dataframes
#X_train.to_csv('X_train.csv')
#X_test.to_csv('X_test.csv')
#y_train.to_csv("y_train.csv")
#y_test.to_csv("y_test.csv")
#X_resampled.to_csv("X_resampled.csv")
#y_resampled.to_csv("y_resampled.csv")

#Faz a regressão com atributos iniciais
#logreg = LogisticRegression(random_state = 0, solver="liblinear")
#logreg.fit(X_resampled, y_resampled.values.ravel())
#
#y_pred = logreg.predict(X_test)
#cm = confusion_matrix(y_test, y_pred)

logit_model=sm.Logit(y_resampled,X_resampled)
result=logit_model.fit()
print(result.summary2())

#Backward Elimination
pVals = result.pvalues
sigLevel=0.05
while pVals[np.argmax(pVals)] > sigLevel:
     X_resampled= X_resampled.drop(np.argmax(pVals), axis=1)
     X_test= X_test.drop(np.argmax(pVals), axis=1)
     print("pval of dim removed: " + str(np.argmax(pVals)))
     print(str(X_resampled.shape[1]) + " dimensions remaining...")
     logit_model=sm.Logit(y_resampled,X_resampled)
     result=logit_model.fit()
     pVals = result.pvalues

print(result.summary2())
logreg = LogisticRegression(random_state = 0, solver="liblinear")
logreg.fit(X_resampled, y_resampled.values.ravel())

y_pred = logreg.predict(X_test)
cm = confusion_matrix(y_test, y_pred)

print('Precisão do classificador de regressão logística no conjunto de testes {:.2f}'
      .format(logreg.score(X_test, y_test)))

#report precision and recall
print(classification_report(y_test, y_pred))


#desenha curva ROC
logit_roc_auc = roc_auc_score(y_test, logreg.predict(X_test))
fpr, tpr, thresholds = roc_curve(y_test, logreg.predict_proba(X_test)[:,1])
plt.figure()
plt.plot(fpr, tpr, label='Regressão Logística (area = %0.2f)' % logit_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Taxa de Falso Positivo')
plt.ylabel('Taxa de Positivos Verdadeiros')
plt.title('Curva ROC')
plt.legend(loc="lower right")
fig = plt.gcf()
plt.show()
#fig.savefig('ROC.png', format='png')





