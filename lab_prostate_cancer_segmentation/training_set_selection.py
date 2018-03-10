
# coding: utf-8

# In[8]:


from sklearn.base import BaseEstimator, TransformerMixin
import re
import time
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from scipy.spatial import distance
from scipy.spatial import distance_matrix
from sklearn.cluster import MiniBatchKMeans
from copy import deepcopy
import math


# In[3]:


#boundary detection
class training_set_selection_miniBatch_kmeans(BaseEstimator,TransformerMixin):
    def __init__(self,labels,kmeans):
        self.labels=labels
        self.kmeans=kmeans
    def fit(self,X,y=None):
        start=time.time()
        print("fit start")
        self.kmeans.fit(X)
        print("fit end")
        print("fit time:%5.1fminute"%((time.time()-start)/60))
        return self
    def transform(self,X,y=None):
        #dataset=pd.concat([X,self.labels],axis=1)
        count1=X.shape[0]
        predict_cluster = self.kmeans.predict(X)
        predict_cluster=pd.DataFrame( predict_cluster,columns=['predict_cluster'])
        X=pd.concat([X,predict_cluster],axis=1)
        self.labels=pd.concat([self.labels,predict_cluster],axis=1)
        #center_set = pd.DataFrame(columns = ['feature0','feature1','feature2','feature3','feature4','predict_label'])
        center_set = list()
        i = 0
        #print (X)
        #print (self.kmeans.cluster_centers_)
        print("drop start")
        for cluster in range(np.int((X.shape[0])/50)):
            if cluster%1000==0:
                print("cluster number:",cluster)
            temp_list = list(self.labels[self.labels['predict_cluster']==cluster]['label'])
            if 1 and 2 in temp_list:
                pass
            elif temp_list == []:  
                pass
            else:
                #temp =temp_list[0]
                #temp_center = np.append(self.kmeans.cluster_centers_[cluster],temp)
                temp_center_set = {'feature0':self.kmeans.cluster_centers_[cluster][0],                                  'feature1':self.kmeans.cluster_centers_[cluster][1],                                  'feature2':self.kmeans.cluster_centers_[cluster][2],                                  'feature3':self.kmeans.cluster_centers_[cluster][3],                                  'feature4':self.kmeans.cluster_centers_[cluster][4],                                  'predict_label':temp_list[0]}
                #temp = pd.DataFrame(data=temp_center_set,index = cluster)
                #center_set = pd.concat(center_set,temp_center_set)
                center_set.append(temp_center_set)
                self.labels = self.labels[self.labels.predict_cluster !=cluster]
                X = X[X.predict_cluster != cluster]
        #dataset.append(pd.DataFrame(self.kmeans.cluster_centers_))#save all the centers of abandoned clusters
        print("drop end")
        count2=X.shape[0]
        print("Drop count:",count1-count2)        
        return X,self.labels,center_set


# In[4]:

# check the selected data after boundary selection
def check_result_after_selection (data,stuck,index,slices,features,selected):
    cmap1 = matplotlib.colors.LinearSegmentedColormap.from_list('my_cmap',['black','green','blue'],256)
    target_data=data[stuck][0][0][0][0][:,:,slices,features]
    target_image1=target_data.reshape(target_data.shape[0],target_data.shape[1])
    target_label=data[stuck][0][0][0][index][:,:,slices]
    target_image2=target_label.reshape(target_label.shape[0],target_label.shape[1])
    plt.imshow(target_image1,cmap = matplotlib.cm.binary,alpha=0.4)
    plt.imshow(target_image2,cmap = cmap1,interpolation="bilinear",alpha=0.4)
    plt.axis("off") #close the axis number

    selected_x=[]
    selected_y=[]
    selected_matrix = selected[selected['source_of_pixel']==stuck]
    selected_matrix=pd.DataFrame.reset_index(selected_matrix).drop('index',axis=1)
    for i in range(len(selected_matrix)):
        temparr = re.findall("\d+",selected_matrix.iloc[i]['index_of_pixel']) 
        if (int(temparr[2]) == slices):
            selected_x.append(int(temparr[0]))
            selected_y.append(int(temparr[1]))
    plt.scatter(selected_y,selected_x,color='r',label="selected boundary",s = 3)
    plt.legend()
    plt.show()


# In[5]:

# FCNN 
def training_set_selection_FCNN (X_train,y_train):
    train = {'feature0':X_train['feature0'],'feature1':X_train['feature1'],'feature2':X_train['feature2'],'feature3':X_train['feature3'],'feature4':X_train['feature4'],'label':y_train['label'],'index_of_pixel':y_train['index_of_pixel'],'source_of_pixel':y_train['source_of_pixel']}
    train = pd.DataFrame(data=train)
    train = pd.DataFrame.sample(train,frac=1)
    
    start1=time.time()
    #define how many data a group contains
    data_size_per_slice = 10000
    data_slice_number = math.ceil(len(train)/data_size_per_slice)
    print("The tatal amount of data slices: %d"%(data_slice_number ))
    print("                           ")

    for j in range(data_slice_number):
        print("current data slice:"+str(j))
        train_slice = train[j*data_size_per_slice:(j+1)*data_size_per_slice]
        train_slice = pd.DataFrame.reset_index(train_slice).drop('index',axis=1)

        class1_indices=np.random.choice(train_slice[train_slice['label']==1].index,1,replace=False)
        class2_indices=np.random.choice(train_slice[train_slice['label']==2].index,1,replace=False)
        class1_sample = train_slice.iloc[class1_indices]
        class2_sample = train_slice.iloc[class2_indices]
        train_slice=train_slice.drop(class1_indices)
        train_slice=train_slice.drop(class2_indices)
        train_slice = pd.DataFrame.reset_index(train_slice).drop('index',axis=1)
        class1_sample = pd.DataFrame.reset_index(class1_sample).drop('index',axis=1)
        class2_sample = pd.DataFrame.reset_index(class2_sample).drop('index',axis=1)

        Store=list()
        newStore=list()
        class1_sample= {'feature0':class1_sample.iloc[0]['feature0'],'feature1':class1_sample.iloc[0]['feature1'],'feature2':class1_sample.iloc[0]['feature2'],'feature3':class1_sample.iloc[0]['feature3'],'feature4':class1_sample.iloc[0]['feature4'],'label':class1_sample.iloc[0]['label'],'index_of_pixel':class1_sample.iloc[0]['index_of_pixel'],'source_of_pixel':class1_sample.iloc[0]['source_of_pixel']}
        class2_sample= {'feature0':class2_sample.iloc[0]['feature0'],'feature1':class2_sample.iloc[0]['feature1'],'feature2':class2_sample.iloc[0]['feature2'],'feature3':class2_sample.iloc[0]['feature3'],'feature4':class2_sample.iloc[0]['feature4'],'label':class2_sample.iloc[0]['label'],'index_of_pixel':class2_sample.iloc[0]['index_of_pixel'],'source_of_pixel':class2_sample.iloc[0]['source_of_pixel']}
        newStore.append(class1_sample)
        newStore.append(class2_sample)

        start=time.time()
        count=0
        while newStore:
            count = count+1
            oldlength = len(Store)
            for element in newStore:
                Store.append(element)

            temp=pd.DataFrame(data=newStore)
            temp=np.array(temp)
            temp=temp[:,0:5]
            np.cast[float](temp)

            train_temp=np.array(train_slice)
            train_temp=train_temp[:,0:5]

            start1=time.time()
            dis=distance.cdist(temp.reshape(len(newStore),5),train_temp,'euclidean')
            nearest_q_matrix=dis.min(0)
            nearest_q_indexmat=dis.argmin(axis=0)

            #update the nearest distance of q in (T-S) dataset, and the corresponding p in S.
            if count==1:
                nearest_q={'p_index':nearest_q_indexmat,'nearest_dis':nearest_q_matrix}
                nearest_q=pd.DataFrame(data=nearest_q)
                nearest_q=pd.concat([nearest_q,train_slice['label']],axis=1,join='outer')
            else:
                nearest_q_indexmat=nearest_q_indexmat+oldlength
                nearest_q_new={'p_index_new':nearest_q_indexmat,'nearest_dis_new':nearest_q_matrix}
                nearest_q_new=pd.DataFrame(data=nearest_q_new)
                nearest_q=pd.concat([nearest_q,nearest_q_new],axis=1,join='outer')
                nearest_q['p_index'] = np.where((nearest_q['nearest_dis_new']<nearest_q['nearest_dis']),nearest_q['p_index_new'],nearest_q['p_index'])
                nearest_q['nearest_dis'] = np.where((nearest_q['nearest_dis_new']<nearest_q['nearest_dis']),nearest_q['nearest_dis_new'],nearest_q['nearest_dis'])
                nearest_q=nearest_q.drop('p_index_new',axis=1)
                nearest_q=nearest_q.drop('nearest_dis_new',axis=1)

            Store_dataframe=pd.DataFrame(data=Store)
            #attach p's label to the dataframe of nearest_q
            p_label=pd.DataFrame(Store_dataframe.iloc[nearest_q['p_index']]['label'])
            p_label.columns=['p_label']
            p_label=pd.DataFrame.reset_index(p_label).drop('index',axis=1)
            nearest_q=pd.concat([nearest_q,p_label],axis=1,join='outer')

            #choose those data  q whose label is not equal to the lapel of nearest_q
            # and then creat the dataframe called different_predict_points
            temp_setting=np.ones(len(train_slice))
            temp_setting=pd.DataFrame(data=temp_setting)
            temp_setting.columns=['setting']
            nearest_q=pd.concat([nearest_q,temp_setting],axis=1,join='outer')
            nearest_q['choose'] = np.where((nearest_q['label']!=nearest_q['p_label']),nearest_q['setting'],np.nan)

            different_predic_points=pd.DataFrame(nearest_q[nearest_q['choose']==1])

            nearest_q=nearest_q.drop('setting',axis=1)
            nearest_q=nearest_q.drop('choose',axis=1)


            newStore=list()

            start2=time.time()
            for i in range(len(Store)):
                temp=different_predic_points[different_predic_points['p_index']==i]
                temp=pd.DataFrame.reset_index(temp)
                if len(temp)>0 :
                    location=temp['nearest_dis'].idxmin(axis=1)
                    add_positon=int(temp.loc[location]['index'])
                    temp_newone= {'feature0':train_slice.loc[add_positon]['feature0'],'feature1':train_slice.loc[add_positon]['feature1'],'feature2':train_slice.loc[add_positon]['feature2'],'feature3':train_slice.loc[add_positon]['feature3'],'feature4':train_slice.loc[add_positon]['feature4'],'label':train_slice.loc[add_positon]['label'],'index_of_pixel':train_slice.loc[add_positon]['index_of_pixel'],'source_of_pixel':train_slice.loc[add_positon]['source_of_pixel']}
                    newStore.append(temp_newone)
                    train_slice=train_slice.drop(add_positon)
                    nearest_q=nearest_q.drop(add_positon)

            nearest_q=nearest_q.drop('p_label',axis=1)
            train_slice=pd.DataFrame.reset_index(train_slice).drop('index',axis=1)
            nearest_q=pd.DataFrame.reset_index(nearest_q).drop('index',axis=1)
        print("current count:%d current size of store:%d time:%5.1f minute"%(count,len(Store),(time.time()-start)/60))

        Store=pd.DataFrame(data=Store)
        if (j==0):
            Store_total=Store
        else:
            frame=[Store_total,Store]
            Store_total=pd.concat(frame)
            Store_total=pd.DataFrame.reset_index(Store_total).drop('index',axis=1)
    print("The total execution time:%5.1f minute"%((time.time()-start1)/60))
    
    Store_total_feature=Store_total.loc[:,['feature0','feature1','feature2','feature3','feature4']]
    Store_total_label = Store_total.loc[:,['index_of_pixel','label','source_of_pixel']]
    return Store_total_feature,Store_total_label


# In[6]:

#CNN 
def training_set_selection_CNN (X_train,y_train):
    train = {'feature0':X_train['feature0'],'feature1':X_train['feature1'],'feature2':X_train['feature2'],'feature3':X_train['feature3'],'feature4':X_train['feature4'],'label':y_train['label'],'index_of_pixel':y_train['index_of_pixel'],'source_of_pixel':y_train['source_of_pixel']}
    train = pd.DataFrame(data=train)
    train = pd.DataFrame.sample(train,frac=1)
    
    data_size_per_slice = 10000
    data_slice_number = math.ceil(len(train)/data_size_per_slice)
    print("The tatal amount of data slices: %d"%(data_slice_number ))
    print("                           ")
    drop=0
    start1=time.time()

    for j in range(data_slice_number):
        #print (j)
        print("current data slice:"+str(j))
        data_slice = train[j*data_size_per_slice:(j+1)*data_size_per_slice]
        train_feature = data_slice[['feature0','feature1','feature2','feature3','feature4']]
        train_label = data_slice[['index_of_pixel','label','source_of_pixel']]
        train_feature=pd.DataFrame.reset_index(train_feature).drop('index',axis=1)
        train_label=pd.DataFrame.reset_index(train_label).drop('index',axis=1)
        Store_feature = train_feature
        Store_label = train_label
        count=1
        drop_temp=0
        start=time.time()
        for i in range(len(train_feature)-1):
            sample=np.array(train_feature.iloc[i+1]).reshape(1,-1)
            temp = np.array(Store_feature[:count])
            m_dis=np.array(distance.cdist(temp,sample,metric='euclidean'))
            m_dis =list(m_dis)
            min_index=m_dis.index(min(m_dis))
            if (int(Store_label.iloc[min_index]['label'])!=int(train_label.iloc[i]['label'])):
                count=count+1
            else:
                drop_temp=drop_temp+1
                Store_feature=Store_feature.drop(count)
                Store_label=Store_label.drop(count)
                Store_feature = pd.DataFrame.reset_index(Store_feature).drop('index',axis=1)
                Store_label = pd.DataFrame.reset_index(Store_label).drop('index',axis=1)       
        print("During this iteratiron, %d data is discarded"%(drop_temp))
        print("this interation costs time:%5.1f minute"%((time.time()-start)/60))
        print("              ")
        if (j==0):
            drop=drop+drop_temp
            Store_feature_total=Store_feature
            Store_label_total=Store_label
        else:
            drop=drop+drop_temp
            frame=[Store_feature_total,Store_feature]
            Store_feature_total=pd.concat(frame)
            Store_feature_total = pd.DataFrame.reset_index(Store_feature_total).drop('index',axis=1)
            frame_2=[Store_label_total,Store_label]
            Store_label_total=pd.concat(frame_2)
            Store_label_total = pd.DataFrame.reset_index(Store_label_total).drop('index',axis=1)
    
    print("The total executing time:%5.1f minute"%((time.time()-start1)/60))
    print("The total discarded data: %d"%(drop))
    return Store_feature_total,Store_label_total

