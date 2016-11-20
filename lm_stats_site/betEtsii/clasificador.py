'''
Created on 28 jul. 2016

@author: mikamb93
'''

import csv
import numpy as np
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.neighbors.classification import KNeighborsClassifier
import pandas as pd
import matplotlib.pylab as plt
from sklearn.metrics.classification import accuracy_score
from petl import fromcsv, look, cut, tocsv 


data=pd.read_csv('C:/Users/mikam/Desktop/TFG/workspace/datosLiga1.csv')
X = data[['Posicion Local','%V Local','%E Local','%D Local','GF Local','GC Local','Posicion Visitante','%V Visitante','%E Visitante','%D Visitante','GF Visitante','GC Visitante']]
y = data['Resultado']



def evaluacion_train_test():
 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.02, random_state=0)
 
    # Creacion y entrenamiento del clasificador
    rfc = RFC(n_estimators=100,n_jobs=-1)
    rfc.fit(X_train, y_train)
     
    # Prediccion de la etiqueta del test y evaluacion
    y_pred = rfc.predict(X_test)
    y_pred_proba = rfc.predict_proba(X_test)
 
    return accuracy_score(y_test, y_pred),rfc


#     #create the training & test sets, skipping the header row with [1:]
#     dataset = np.genfromtxt(open('Data/train.csv','r'), delimiter=',', dtype='f8')[1:]    
#     target = [x[0] for x in dataset]
#     train = [x[1:] for x in dataset]
#     test = np.genfromtxt(open('Data/test.csv','r'), delimiter=',', dtype='f8')[1:]
#     
#     #create and train the random forest
#     #multi-core CPUs can use: rf = RandomForestClassifier(n_estimators=100, n_jobs=2)
#     rf = RFC(n_estimators=100)
#     rf.fit(train, target)
# 
#     np.savetxt('Data/submission2.csv', rf.predict(test), delimiter=',', fmt='%f')
    
# def evaluacion_val_cruzada(carpetas):
#     vecinos = RFC()
#     scores = cross_val_score(vecinos, X, y, cv=carpetas)
#     return scores.mean()

#-----------------------------------------------------------------------
# Ejecucion de metodos
#-----------------------------------------------------------------------

def seleccionaMejorRFC(intentos):
    mejor=0
    indiceMejor = 0
    rfc=None
    suma=0
    for i in range(intentos):
        evaluacion=evaluacion_train_test()
        score=evaluacion[0]
        classifier=evaluacion[1]
        suma += score
        print('test ',i,' : ',score)
        if(score > mejor):
            mejor=score
            rfc=classifier
            indiceMejor=i
        i+=1
    print(mejor,indiceMejor,'    Media : ',suma/(i))
    return rfc
# resultados = dict()
# for i in range(20):
#     resultados[i+2] = evaluacion_val_cruzada(i+2)
# resultados = pd.Series(resultados)
# resultados.plot()
# plt.show()


