import numpy as np
import pandas as pd
from math import *
import matplotlib.pyplot as plt
import sklearn.svm as svm
from sklearn import datasets
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
df_wine = pd.read_csv('csv', header=None)
df_wine.columns = ['no','trustor','trustee','trust lable','volatility','Integrity','Pearson','jaccard']

df_label1 = pd.read_csv('csv', header=None)
df_label1.columns = ['no','trustor','trustee','trust lable','volatility','Integrity','Pearson','jaccard']


l_d, l_c = df_wine.ix[:, 4:].values, df_wine.ix[:, 3].values
u_d, y1 = df_label1.ix[:, 4:].values, df_label1.ix[:, 3].values
lu_d = np.concatenate((l_d, u_d))
n = len(l_d)+len(u_d)

#print(l_d)
#print(l_c)
#print(u_d)
#print(u_c)

clf1 = svm.SVC(C=1,kernel='rbf')
clf1.fit(l_d, l_c)
#clf0 = svm.SVC(C=1,kernel='linear')
#clf0.fit(l_d, l_c)
#lu_c_0 = clf0.predict(lu_d) 
u_c_new = clf1.predict(u_d)  # the pseudo label for unlabelled samples 
cu, cl = 0.001, 1
sample_weight = np.ones(n)
sample_weight[len(l_c):] = cu
id_set = np.arange(len(u_d))

while cu < cl:
    print(cu)
    lu_c = np.concatenate((l_c, u_c_new))  # 70
    clf1.fit(lu_d, lu_c, sample_weight=sample_weight)
    while True:
        print("...")
        u_c_new = clf1.predict(u_d)  # the pseudo label for unlabelled samples
        #for i in range(len(u_c_new)):
            #print(u_c_new[i])
        
        u_dist = clf1.decision_function(u_d)  # the distance of each sample
        norm_weight = np.linalg.norm(clf1.coef_)  # norm of weight vector
        epsilon = 1 - u_dist * u_c_new * norm_weight
        #print(epsilon)
        plus_set, plus_id = epsilon[u_c_new > 0], id_set[u_c_new > 0]  # positive labelled samples
        minus_set, minus_id = epsilon[u_c_new < 0], id_set[u_c_new < 0]  # negative labelled samples
        #print(plus_set)
        #print(minus_set)
        plus_max_id, minus_max_id = plus_id[np.argmax(plus_set)], minus_id[np.argmax(minus_set)]
        a, b = epsilon[plus_max_id], epsilon[minus_max_id]

        if a > 0 and b > 0 and a + b > 2:
            u_c_new[plus_max_id], u_c_new[minus_max_id] = -u_c_new[plus_max_id], -u_c_new[minus_max_id]
            lu_c = np.concatenate((l_c, u_c_new))
            clf1.fit(lu_d, lu_c, sample_weight=sample_weight)
        else:
            break
    cu = min(cu * 2, cl)
    
    sample_weight[len(l_c):] = cu

joblib.dump(clf1,'D:\\TSVMMODEL.m')
print("saveover")
#lu_c = np.concatenate((l_c, u_c_new))
#test_c1 = clf0.predict(test_d)
#test_c2 = clf1.predict(test_d)
#score1 = clf0.score(test_d,test_c)
#score2 = clf1.score(test_d,test_c)


df_label1['trust lable']=u_c_new
save=df_label1[['trustor','trustee','trust lable','volatility','Integrity','Pearson','jaccard']]
print(save)
save.to_csv('.csv') 
