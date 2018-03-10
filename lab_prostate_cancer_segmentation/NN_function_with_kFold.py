
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from scipy.spatial import distance
from sklearn.model_selection import StratifiedKFold
import itertools


# In[2]:


import sys
sys.path.append(r"C:\Users\yangshanqi\Documents\lab\labgithubcopy\task_1_version_3")
from calculation_score import cal_score
from CalList import CalList
from CalList import CalParList



# In[3]:

# calculate the point in the validation data set with cluster center mean 1 ans cluster center mean 2
def nn_distance_calculate(X_val,X_train,y_train):
    class_1=X_train[y_train['label']==1]
    class_2=X_train[y_train['label']==2]
    mean_1=np.array(class_1.mean()).reshape(1,-1)
    mean_2=np.array(class_2.mean()).reshape(1,-1)
    cov_1=np.matrix(class_1.cov())
    cov_2=np.matrix(class_2.cov())
    dis_1=distance.cdist(X_val,mean_1,metric='mahalanobis',V=cov_1).ravel()
    dis_2=distance.cdist(X_val,mean_2,metric='mahalanobis',V=cov_2).ravel()
    return dis_1, dis_2


# In[2]:
 
# This is the basic part of adjustment phase. For training data, it will be splitesd into 10 slices, the average results will be returned.
def NN_cross_validation(training_feature,training_label,alpha):
    skf = StratifiedKFold(n_splits=10,shuffle=True)
    skf.get_n_splits(training_feature,training_label['label'])
    Cal_Result_List = CalList ()
    skf = StratifiedKFold(n_splits=10,shuffle=True)
    skf.get_n_splits(training_feature,training_label['label'])
   
    for train_index, test_index in skf.split(training_feature,training_label['label']):

        X_train, X_val = training_feature.loc[train_index], training_feature.loc[test_index]
        y_train, y_val = training_label.loc[train_index], training_label.loc[test_index]
        
        dis_1,dis_2=nn_distance_calculate(X_val,X_train,y_train)
        y_pred_temp=nn_predict(dis_1,dis_2,alpha,X_val)
        Precall,f1_score,BER,FPR = cal_score (y_pred_temp,y_val['label'])
        Cal_Result_List.list_append(Precall,f1_score,BER,FPR)
        
    Precall,FPR,BER,f1_score = Cal_Result_List.list_average_cal()
    
    return Precall,FPR,BER,f1_score


# In[4]:


#Nearest Mean algorithm
#fundamental function, give a label for every validation sample.
def nn_predict(dis_1,dis_2,alpha,X_val):
    y_pred=[]
    for index in range(len(X_val)):
        if (alpha)*dis_1[index]<(1-alpha)*dis_2[index]:
                y_pred.append(np.float64(1.0)) 
        else:
                y_pred.append(np.float64(2.0))
    y_pred=pd.Series(y_pred)
    return y_pred


# In[3]:

# Change the distances bias, for every change, have a cross-validaion and analysis the result.
def nn_predict_with_distance_adjust (training_feature,training_label):#,#X_val,y_val):
    
    Result_List = CalParList (1,"alpha")
    alpha = 0.10
    
    while(alpha<=0.9):
        
        Precall,FPR,BER,f1_score = NN_cross_validation(training_feature,training_label,alpha)
        
        Result_List.list_append (Precall,f1_score,BER,FPR,alpha)

        if (0.4<=alpha<=0.6):
            alpha=alpha+0.01
        else:
            alpha=alpha+0.05        
    
    result = Result_List.return_result()
    return result


# In[8]:

# Change the distances bias in small scale
def nn_predict_with_distance_adjust_presion (training_feature,training_label,alpha_lower_bound,alpha_higher_bound):
    #dis_1,dis_2=nn_distance_calculate(X_val,X_train,y_train)
    alpha =alpha_lower_bound
    Result_List = CalParList (1,"alpha")
    
    while(alpha<=alpha_higher_bound):
        
        Precall,FPR,BER,f1_score = NN_cross_validation(training_feature,training_label,alpha)
        
        Result_List.list_append (Precall,f1_score,BER,FPR,alpha)

        alpha=alpha+0.001
    
    result = Result_List.return_result()
    return result


# In[15]:

#final validation
def nn_validation (X_train,y_train,X_val,y_val,alpha):
    dis_1,dis_2=nn_distance_calculate(X_val,X_train,y_train)
    y_pred_temp=nn_predict(dis_1,dis_2,alpha,X_val)
    Precall,f1_score,BER,FPR = cal_score (y_pred_temp,y_val['label'])
    print ("TPR:"+str(Precall)+"   f1 score:" + str(f1_score)+"   FPR:"+ str(FPR)+"   BER:" + str(BER))
    return


# In[16]:

# try every pair of feature choice, and adjust the distance bias, return the max f1 score one for every pair of feature choice.
def nn_feature_selection_wrap(training_feature,training_label,alpha):
    
    Result_List = CalParList (3,"alpha","feature_0","feature_1")
    
    skf = StratifiedKFold(n_splits=10,shuffle=True)
    skf.get_n_splits(training_feature,training_label['label'])
    
    feature_avaliable = ['feature0','feature1','feature2','feature3','feature4']
    feature_choice=list(itertools.combinations(feature_avaliable ,2))
   
    for i in range(len(feature_choice)):
        
        Cal_Result_List = CalList ()
        for train_index, test_index in skf.split(training_feature,training_label['label']):
            X_train, X_val = training_feature.loc[train_index], training_feature.loc[test_index]
            y_train, y_val = training_label.loc[train_index], training_label.loc[test_index]
            X_train=X_train.loc[:,[feature_choice[i][0],feature_choice[i][1]]]
            X_val=X_val.loc[:,[feature_choice[i][0],feature_choice[i][1]]]
            dis_1,dis_2=nn_distance_calculate(X_val,X_train,y_train)
            y_pred_temp=nn_predict(dis_1,dis_2,alpha,X_val)
            Precall,f1_score,BER,FPR = cal_score (y_pred_temp,y_val['label'])           
            Cal_Result_List.list_append(Precall,f1_score,BER,FPR)

        Precall,FPR,BER,f1_score = Cal_Result_List.list_average_cal()
        Result_List.list_append (Precall,f1_score,BER,FPR,alpha,feature_choice[i][0],feature_choice[i][1])
    
    result = Result_List.return_result()
    return result

