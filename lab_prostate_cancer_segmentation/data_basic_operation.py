
# coding: utf-8

# In[4]:


import pandas as pd


# In[6]:

# choose label 1 and label 2 data seperately according the specific amount.
def choose_data_seperately (training_feature,training_label,label_1_amount,label_2_amount):
    train_data= pd.concat([training_feature,training_label['label']],axis=1,join='outer')
    Class1_sample =pd.DataFrame.sample(train_data[train_data['label']==1],label_1_amount)
    Class2_sample =pd.DataFrame.sample(train_data[train_data['label']==2],label_2_amount)
    res = [Class1_sample, Class2_sample]
    train_com = pd.concat(res)
    sample_label = pd.DataFrame(train_com['label'])
    sample_feature=train_com.drop(["label"],axis=1)
    sample_feature = pd.DataFrame.reset_index(sample_feature).drop('index',axis=1)
    sample_label = pd.DataFrame.reset_index(sample_label).drop('index',axis=1)
    return sample_feature , sample_label


# In[7]:

# ramdomly choose data together.
def choose_data_together (X_train,y_train,sample_amount):
    train = pd.concat([X_train,y_train['label']],axis=1,join='outer')
    train = pd.DataFrame(data=train)
    sample =pd.DataFrame.sample(train,sample_amount)
    sample_label = pd.DataFrame(sample['label'])
    sample_feature=sample.drop(["label"],axis=1)
    sample_feature = pd.DataFrame.reset_index(sample_feature).drop('index',axis=1)
    sample_label = pd.DataFrame.reset_index(sample_label).drop('index',axis=1)
    return sample_feature,sample_label

