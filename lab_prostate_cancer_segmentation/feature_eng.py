
# coding: utf-8

# In[8]:


from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd


# In[2]:

# minmax
scaler1=MinMaxScaler(feature_range=(0, 1), copy=True)
class Feature_scaling(BaseEstimator,TransformerMixin):
    def fit(self,X,y=None):
        scaler1.fit(np.array(X['feature0']).reshape(-1,1))
        return self
    def transform(self,X,y=None):
        X['feature0']=scaler1.transform(np.array(X['feature0']).reshape(-1,1))
        return X


# In[3]:

#normalization
scaler2=StandardScaler()
class Normalization(BaseEstimator,TransformerMixin):
    def fit(self,X,y=None):
        scaler2.fit(X[['feature0','feature1','feature2','feature3','feature4']])
        return self
    def transform(self,X,y=None):
        X[['feature0','feature1','feature2','feature3','feature4']]=scaler2.transform(X[['feature0','feature1','feature2','feature3','feature4']])
        return pd.DataFrame(X)


# In[7]:

#pipeline
feature_eng=Pipeline([("feature_scale",Feature_scaling()),
                     ("normalization",Normalization())])

