
# coding: utf-8

# In[4]:


import time
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from scipy.spatial import distance
from scipy.stats import chisquare
from scipy.stats import chi2
import re
import matplotlib.pyplot as plt
import matplotlib


# In[10]:


# robust distance
class outliers_clean_resampling(BaseEstimator,TransformerMixin):
    def __init__(self,p_free,n_subsamples,labels,y_dropped=pd.Series([]),md_dis=pd.Series([]),p_value_1=0.,p_value_2=0.,h_value=0):
        self.md_dis=md_dis
        self.p_value_1=p_value_1
        self.p_value_2=p_value_2
        self.p_free=p_free
        self.h_value=h_value
        self.labels=labels
        self.y_dropped=labels
        self.n_subsamples=n_subsamples
    def fit(self,X,y=None):
        self.h_value=np.int((X.shape[0]+self.p_free+1)/2)
        mean_value=np.array([X.mean()])
        cov_value=np.mat(X.cov().as_matrix()).I
        #print("MD calculation Start")
        self.md_dis=distance.cdist(X,mean_value,metric='mahalanobis',VI=cov_value).ravel()
        #print("MD calculation end")
        chi2.fit(self.md_dis,self.p_free)
        self.p_value_1=np.sqrt(chi2.ppf(0.99999999999999994375,self.p_free))
        self.p_value_2=np.sqrt(chi2.ppf(0.5,self.p_free))
        return self
    def transform(self,X,y=None):
        np.random.seed(30)
        mean_set,cov_set,m_dis_order,V_j=[],[],[],[]
        #print("Resampling begin")
        start1=time.time()
        for subset in range(self.n_subsamples):
            #if subset%1000==0:
                #print("replications number:%d time:%5.1f minute"%(subset,(time.time()-start1)/60))
            sample_ID=[]
            for index in range(self.p_free+1):
                sample_ID.append(np.random.choice(range(len(X)),replace=False))
            X_tr=np.array(X.iloc[sample_ID])
            sub_mean=np.array([(1/(self.p_free+1))*np.sum(X_tr,axis=0)])
            mean_set.append(sub_mean)
            sub_cov=np.mat((1/(self.p_free))*np.dot((X_tr-sub_mean).T,(X_tr-sub_mean))).I
            cov_set.append(sub_cov) 
            m_dis=pd.Series((distance.cdist(X,sub_mean,metric='mahalanobis',VI=sub_cov)**2).ravel())            .sort_values(ascending=True).iloc[self.h_value] #ascending=True : from small to big
            #if subset != 0 :
                #if m_dis>=(V_j[subset-1]/sub_cov.I.det())**(1/self.p_free):
                    #break
                #else:
                    #pass
            m_dis_order.append(m_dis)
            V_j.append(m_dis*np.linalg.det(sub_cov))
        #print("Resampling end")
        #print(m_dis_order[])
        J_index=pd.Series(V_j).sort_values(ascending=True).index.tolist()[0]
        m_dis_value=m_dis_order[J_index]
        robust_mean=mean_set[J_index]
        robust_cov=((1+15/(X.shape[0]-self.p_free))**2)*(1/self.p_value_2)*m_dis_value*cov_set[J_index]
        #print("RD calculation Start")
        robust_dis=distance.cdist(X,robust_mean,metric='mahalanobis',VI=robust_cov).ravel()
        #print("RD calculation end")
        #print("Robust distance: ",robust_dis)
        #print("Cutoff value: ",self.p_value_1)
        count,count1,count2=0,0,0
        count1=X.shape[0]
        #print("Drop Start")
        robust_dis=pd.DataFrame(robust_dis,columns=['robust_dis'])
        X=pd.concat([X,robust_dis],axis=1)
        self.labels=pd.concat([self.labels,robust_dis],axis=1)
        self.y_dropped=pd.concat([self.y_dropped,robust_dis],axis=1)
        X=X[X['robust_dis']<=self.p_value_1].copy()
        self.labels=self.labels[self.labels['robust_dis']<=self.p_value_1].copy()
        self.y_dropped=self.y_dropped[self.y_dropped['robust_dis']>self.p_value_1].copy()
        X=pd.DataFrame.reset_index(X).drop('index',axis=1)
        self.labels=pd.DataFrame.reset_index(self.labels).drop('index',axis=1)
        self.y_dropped=pd.DataFrame.reset_index(self.y_dropped).drop('index',axis=1)
        count2=X.shape[0]
        count=count1-count2
        #print("Drop End")
        print("drop count:",count)
        return X,self.labels,self.y_dropped,robust_dis


# In[9]:


def outliers_clean_resampling_group(X_data,y_data,stuck_amount):
    for i in range(stuck_amount):
        print ("current executing data stuck: "+str(i))
        X_input_temp = X_data[y_data['source_of_pixel']==i]
        X_input_temp=pd.DataFrame.reset_index(X_input_temp).drop('index',axis=1)
        y_input_temp = y_data[y_data['source_of_pixel']==i]
        y_input_temp=pd.DataFrame.reset_index(y_input_temp).drop('index',axis=1)
        X_temp,y_temp,y_temp_dropped,robust_dis_temp=outliers_clean_resampling(p_free=5,n_subsamples=3000,labels=y_input_temp).fit_transform(X_input_temp)
        y_temp_dropped=pd.DataFrame.reset_index(y_temp_dropped).drop('Unnamed: 0',axis=1)
        temp_setting=np.ones(len(robust_dis_temp))
        temp_setting=np.multiply(temp_setting,i)
        temp_setting=pd.DataFrame(data=temp_setting)
        temp_setting.columns=['source_of_pixel']
        robust_dis_temp=pd.concat([robust_dis_temp,temp_setting],axis=1,join='outer')
        print("            ")
        if (i==0):
            X_selected = pd.DataFrame(X_temp)
            y_selected = pd.DataFrame(y_temp)
            y_dropped = pd.DataFrame(y_temp_dropped)
            robust_dis=pd.DataFrame(robust_dis_temp)
        else:
            X_res = [X_selected,X_temp]
            X_selected = pd.concat(X_res)
            
            y_res = [y_selected,y_temp]
            y_selected = pd.concat(y_res)
            
            y_dropped_res = [y_dropped,y_temp_dropped]
            y_dropped = pd.concat(y_dropped_res)
            
            robust_dis_res =[robust_dis,robust_dis_temp]
            robust_dis = pd.concat(robust_dis_res)
    return X_selected,y_selected,y_dropped,robust_dis


# In[3]:


def plot_outliers(maha_dis,cdf1,cdf2,cdf3):
    x=range(len(maha_dis))
    plt.figure(figsize=(16,12))
    plt.scatter( x, maha_dis ,s=1)

    plt.hlines( np.sqrt(chi2.ppf(cdf1, 5)), 0, len(maha_dis), label ="%5f $\chi^2$ quantile"%(cdf1), linestyles = "solid" ) 
    plt.hlines( np.sqrt(chi2.ppf(cdf2, 5)), 0, len(maha_dis), label ="%5f $\chi^2$ quantile"%(cdf2), linestyles="dashed" ) 
    plt.hlines( np.sqrt(chi2.ppf(cdf3, 5)), 0, len(maha_dis), label ="%5f $\chi^2$ quantile"%(cdf3), linestyles = "dotted" )

    plt.legend()
    plt.ylabel("recorded value",fontsize=20)
    plt.xlabel("observation",fontsize=20)
    plt.title( 'Detection of outliers at different $\chi^2$ quantiles',fontsize=25 )

    plt.show()


# In[5]:


def check_resultofdropping (data,stuck,index,slices,features,selected,dropped):
    cmap1 = matplotlib.colors.LinearSegmentedColormap.from_list('my_cmap',['black','green','blue'],256)
    #plot the original prostate area and the cancer area
    target_data=data[stuck][0][0][0][0][:,:,slices,features]
    target_image1=target_data.reshape(target_data.shape[0],target_data.shape[1])
    target_label=data[stuck][0][0][0][index][:,:,slices]
    target_image2=target_label.reshape(target_label.shape[0],target_label.shape[1])
    plt.imshow(target_image1,cmap = matplotlib.cm.binary,alpha=0.4)
    plt.imshow(target_image2,cmap = cmap1,interpolation="bilinear",alpha=0.4)
    plt.axis("off") #close the axis number
    
    #plot the selected samples
    selected_x=[]
    selected_y=[]
    selected_matrix = selected[selected['source_of_pixel']==stuck]
    selected_matrix=pd.DataFrame.reset_index(selected_matrix).drop('index',axis=1)
    for i in range(len(selected_matrix)):
        #using Regular expression operations to find the point
        temparr = re.findall("\d+",selected_matrix.iloc[i]['index_of_pixel'])
        if (int(temparr[2]) == slices):
            selected_x.append(int(temparr[0]))
            selected_y.append(int(temparr[1]))
    plt.scatter(selected_y,selected_x,label="selected samples",s = 3)
    
    #plot the droped samples
    dropped_x=[]
    dropped_y=[]
    dropped_matrix = dropped[dropped['source_of_pixel']==stuck]
    dropped_matrix = pd.DataFrame.reset_index(dropped_matrix).drop('index',axis=1)
    for i in range(len(dropped_matrix)):
        temparr = re.findall("\d+",dropped_matrix.iloc[i]['index_of_pixel'])
        if (int(temparr[2]) == slices):
            dropped_x.append(int(temparr[0]))
            dropped_y.append(int(temparr[1]))
    plt.scatter(dropped_y,dropped_x, label="dropped samples", s = 2)
    plt.legend()
    plt.show()

