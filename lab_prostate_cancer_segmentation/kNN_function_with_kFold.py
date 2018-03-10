
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import time
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import StratifiedKFold
import sys
import itertools
sys.path.append(r"C:\Users\yangshanqi\Documents\lab\labgithubcopy\task_1_version_2")
from calculation_score import cal_score
from CalList import CalList
from CalList import CalParList

# In[2]:


from data_basic_operation import choose_data_seperately


# In[2]:

# the basic and core part of kNN: build the model, test on the validation set and calculate the result.
def kNN_base_function (X_train,y_train,X_val,y_val,k_value):
    neigh = KNeighborsClassifier(n_neighbors=k_value,algorithm='auto',weights ='distance')
    #print(X_train)
    #print(y_train['label'])
    neigh.fit(X_train, y_train['label'])
    y_pred = neigh.predict(X_val)
    y_pred = {"label_pred":y_pred}
    y_pred = pd.DataFrame(data=y_pred)
    Precall,f1_score,BER,FPR = cal_score (y_pred,y_val['label']) 
    return Precall,f1_score,BER,FPR


# In[2]:

#After cross-validation stage, this is for the validation on the last 3 patients' data. Because there is a sample process, there are 10 iterations to get the average results for more accurate results. 
def kNN_validation (X_train,y_train,X_val,y_val,sample_amount,data_ratio,k_value):
    #sample_amount = 40000
    #data_ratio = 1.2
    label_1_amount = int(sample_amount * (data_ratio/(data_ratio+1)))
    label_2_amount = int(sample_amount-label_1_amount)
    
    Cal_Result_List = CalList ()
    iter_max = 10
    count = 0
   
    while (count < iter_max):
        sample_feature,sample_label = choose_data_seperately (X_train,y_train,label_1_amount,label_2_amount)
        Precall,f1_score,BER,FPR = kNN_base_function (sample_feature,sample_label,X_val,y_val,k_value)
        Cal_Result_List.list_append(Precall,f1_score,BER,FPR)
        count = count+1
    
    Precall,FPR,BER,f1_score = Cal_Result_List.list_average_cal()    
    return Precall,FPR,BER,f1_score 
        


# In[2]:

# This is the basic part in training stage, training data will be split into 10 pieces. And there are 10 iterations to get a average result. The return results will be used in parameter adjustment. 
def kNN_cross_validation (training_feature, training_label, k_value):
    Cal_Result_List = CalList ()
    time_list_temp = []
    skf = StratifiedKFold(n_splits=10,shuffle=True)
    skf.get_n_splits(training_feature,training_label['label'])
   
    for train_index, test_index in skf.split(training_feature,training_label['label']):
        start1=time.time()
        X_train, X_val = training_feature.loc[train_index], training_feature.loc[test_index]
        y_train, y_val = training_label.loc[train_index], training_label.loc[test_index]

        Precall,f1_score,BER,FPR = kNN_base_function (X_train,y_train,X_val,y_val,k_value)
        Cal_Result_List.list_append(Precall,f1_score,BER,FPR)
        time_list_temp.append(time.time()-start1)
        
    Precall,FPR,BER,f1_score = Cal_Result_List.list_average_cal()
    time_var=(sum(time_list_temp)/len(time_list_temp))
    return Precall,FPR,BER,f1_score,time_var


# In[3]:

# For each k, do a cross-validation and get the adjuatment table to get the best parameter in the cross-validation.
def kNN_k_parameter_adjust (training_feature,training_label):
    #start=time.time()
    k_value=5    
    Result_List = CalParList (2,"k_value","time")   

    while (k_value<10):
        
        Precall,FPR,BER,f1_score,time_var = kNN_cross_validation (training_feature, training_label, k_value)

        Result_List.list_append (Precall,f1_score,BER,FPR,k_value,time_var)
        
        if (k_value < 27):
            k_value=k_value+2
        else:
            k_value = k_value+5
        
    #print("the total executing time:%5.1fminute"%((time.time()-start)/60))
    result = Result_List.return_result()
    return result


# In[4]:

# For each data-ratio, do a cross-validation and get the adjuatment table to get the best parameter in the cross-validation.
def kNN_data_ratio_adjust (training_feature,training_label,k_value):
    start=time.time()
    label_1_amount = 40000
    label_2_amount = 10000
    
    Result_List = CalParList (4,"label_1_amount","label_2_amount","ratio","time")  
    iter_amount = 5
    train_data= pd.concat([training_feature,training_label['label']],axis=1,join='outer')
       
    while (label_1_amount > 2000):
        count=0
        Cal_Result_List = CalList ()
        time_list_temp=[]

        while (count<iter_amount):
            start1=time.time()
            
            sample_feature , sample_label = choose_data_seperately (training_feature,training_label,label_1_amount,label_2_amount)

            Precall,FPR,BER,f1_score,time_var = kNN_cross_validation (sample_feature, sample_label, k_value)          
            Cal_Result_List.list_append(Precall,f1_score,BER,FPR)           
            time_list_temp.append(time_var)
            count = count+1   
            
        Precall,FPR,BER,f1_score = Cal_Result_List.list_average_cal()
        time_ave=sum(time_list_temp)/len(time_list_temp)
        Result_List.list_append (Precall,f1_score,BER,FPR,label_1_amount,label_2_amount,label_1_amount/label_2_amount,time_ave)
  
        #print("current data labe 1 size:%d ,fit time:%5.1fminute"%(t,(time.time()-start1)/60))
        if (label_1_amount > 10000):
            label_1_amount = label_1_amount-5000
        else:
            label_1_amount = label_1_amount-2500
        
    print("the total executing time:%5.1fminute"%((time.time()-start)/60))       
    result = Result_List.return_result()
    return result
            
            


# In[3]:

# For the specific data-ratio, do a cross-validation with incresing k and get the adjuatment table to get the best parameter in the cross-validation.
def kNN_k_parameter_adjust_with_specific_data_ratio (X_train,y_train,data_ratio):
    tpr_list = []
    fpr_list = []
    BER_list = []
    f1_score_list = []
    count = 0
    iter_count = 5
    while (count<iter_count):
        
        label_1_amount=int(20000*data_ratio)
        label_2_amount=20000

        sample_feature , sample_label = choose_data_seperately (X_train,y_train,label_1_amount,label_2_amount)

        result = kNN_k_parameter_adjust (sample_feature,sample_label)
        
        if(count==0):
            tpr_list = result['TPR']
            fpr_list = result['FPR']
            f1_score_list = result['f1_score']
            BER_list = result['BER']
        else:
            tpr_list = (count*tpr_list+ result['TPR'])/(count+1)
            fpr_list = (count*fpr_list+ result['FPR'])/(count+1)
            f1_score_list = (count*f1_score_list+ result['f1_score'])/(count+1)
            BER_list = (count*BER_list+ result['BER'])/(count+1)
        count = count +1
    
    result_total = {"k_value":result['k_value'],"TPR":tpr_list,"FPR":fpr_list,"f1_score":f1_score_list,"BER":BER_list}
    columns = ["k_value","f1_score","TPR","FPR","BER"]
    result = pd.DataFrame (data=result,columns=columns)
    return result


# In[4]:

# Because data-ratio has a more effect on this, in the feature selection, the variable is data ratio. For every pair of features, have a adjustment of the data ratio adn return the table for analysis.
def kNN_feature_selection_wrap(X_train,y_train,k_value):
    feature_avaliable = ['feature0','feature1','feature2','feature3','feature4']
    feature_choice=list(itertools.combinations(feature_avaliable ,2))
    count = 0
    for i in range(len(feature_choice)):    
        print("current feature choosen:")
        print(feature_choice[i])

        X_train_temp = X_train.loc[:,[feature_choice[i][0],feature_choice[i][1]]]
        
        res = kNN_data_ratio_adjust (X_train_temp,y_train ,k_value)
        
        res['feature0']=feature_choice[i][0]
        res['feature1']=feature_choice[i][1]
        if (count==0):
            res_total = res
            count = count+1
        else :
            res_temp =[res_total,res]
            res_total = pd.concat (res_temp)
    return res_total

