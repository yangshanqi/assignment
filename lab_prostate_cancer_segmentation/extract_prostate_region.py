
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:

# select data according to the expert label. If the labels given by experts are different. It will also be selected and labeled as 1.5. This is for processing later.
def extract_prostate_region(data,datat_stuck_num):
    train_index_matrix = []
    train_isolated_feature0=[]
    train_isolated_feature1=[]
    train_isolated_feature2=[]
    train_isolated_feature3=[]
    train_isolated_feature4=[]
    train_isolated_label=[]
    train_sourceofpixels = []
    for i in range(datat_stuck_num):
        feature0 = data [i][0][0][0][0][:,:,:,0]
        feature1 = data [i][0][0][0][0][:,:,:,1]
        feature2 = data [i][0][0][0][0][:,:,:,2]
        feature3 = data [i][0][0][0][0][:,:,:,3]
        feature4 = data [i][0][0][0][0][:,:,:,4]
        tempA = data[i][0][0][0][1]
        tempB = data[i][0][0][0][2]
        ita = np.nditer(tempA, flags =['multi_index'])
        itb = np.nditer(tempB, flags =['multi_index'])
        itf0 = np.nditer(feature0,flags =['multi_index'])
        itf1 = np.nditer(feature1,flags =['multi_index'])
        itf2 = np.nditer(feature2,flags =['multi_index'])
        itf3 = np.nditer(feature3,flags =['multi_index'])
        itf4 = np.nditer(feature4,flags =['multi_index'])
        while not ita.finished:
            if ((ita[0]==1)&(itb[0]==1)):
                train_isolated_feature0.append(itf0[0])
                train_isolated_feature1.append(itf1[0])
                train_isolated_feature2.append(itf2[0])
                train_isolated_feature3.append(itf3[0])
                train_isolated_feature4.append(itf4[0])
                train_isolated_label.append(ita[0])
                train_index_matrix.append(np.array(ita.multi_index))
                train_sourceofpixels.append(i)
            elif ((ita[0]==2)&(itb[0]==2)):
                train_isolated_feature0.append(itf0[0])
                train_isolated_feature1.append(itf1[0])
                train_isolated_feature2.append(itf2[0])
                train_isolated_feature3.append(itf3[0])
                train_isolated_feature4.append(itf4[0])
                train_isolated_label.append(ita[0])
                train_index_matrix.append(np.array(ita.multi_index))
                train_sourceofpixels.append(i)
           
            elif((ita[0] == 1)&(itb[0]== 2)):
                train_isolated_feature0.append(itf0[0])
                train_isolated_feature1.append(itf1[0])
                train_isolated_feature2.append(itf2[0])
                train_isolated_feature3.append(itf3[0])
                train_isolated_feature4.append(itf4[0])
                train_isolated_label.append(1.5)
                train_index_matrix.append(np.array(ita.multi_index))
                train_sourceofpixels.append(i)
            elif((ita[0] ==2) & (itb[0]==1)):
                train_isolated_feature0.append(itf0[0])
                train_isolated_feature1.append(itf1[0])
                train_isolated_feature2.append(itf2[0])
                train_isolated_feature3.append(itf3[0])
                train_isolated_feature4.append(itf4[0])
                train_isolated_label.append(1.5)
                train_index_matrix.append(np.array(ita.multi_index))
                train_sourceofpixels.append(i)
            
            itf0.iternext()
            itf1.iternext()
            itf2.iternext()
            itf3.iternext()
            itf4.iternext()
            itb.iternext()
            ita.iternext()
    tempdic_train = {'feature0':train_isolated_feature0,'feature1':train_isolated_feature1,'feature2':train_isolated_feature2,'feature3':train_isolated_feature3,'feature4':train_isolated_feature4}
    train_feature= pd.DataFrame(data=tempdic_train)
    tempdic_train = {'label':train_isolated_label, 'source_of_pixel':train_sourceofpixels, 'index_of_pixel':train_index_matrix}
    train_label= pd.DataFrame(data=tempdic_train)
    
    return train_feature,train_label


# In[6]:

#select data according to the ground truth.
def extract_prostate_region_validation(data):
    validation_stuck_num=3 
    validation_index_matrix = []
    validation_isolated_feature0=[]
    validation_isolated_feature1=[]
    validation_isolated_feature2=[]
    validation_isolated_feature3=[]
    validation_isolated_feature4=[]
    validation_isolated_label=[]
    validation_sourceofpixel = []
    for i in range(validation_stuck_num):
        temp_label = data[i+11][0][0][0][3]
        temp_feature0 = data[i+11][0][0][0][0][:,:,:,0]
        temp_feature1 = data[i+11][0][0][0][0][:,:,:,1]
        temp_feature2 = data[i+11][0][0][0][0][:,:,:,2]
        temp_feature3 = data[i+11][0][0][0][0][:,:,:,3]
        temp_feature4 = data[i+11][0][0][0][0][:,:,:,4]
        it_label = np.nditer(temp_label, flags=['multi_index'])
        it_feature0 = np.nditer(temp_feature0, flags=['multi_index'])
        it_feature1 = np.nditer(temp_feature1, flags=['multi_index'])
        it_feature2 = np.nditer(temp_feature2, flags=['multi_index'])
        it_feature3 = np.nditer(temp_feature3, flags=['multi_index'])
        it_feature4 = np.nditer(temp_feature4, flags=['multi_index'])
        while not it_label.finished:
            if (it_label[0] != 0 ):
                validation_isolated_feature0.append(it_feature0[0])
                validation_isolated_feature1.append(it_feature1[0])
                validation_isolated_feature2.append(it_feature2[0])
                validation_isolated_feature3.append(it_feature3[0])
                validation_isolated_feature4.append(it_feature4[0])
                validation_isolated_label.append(it_label[0])
                validation_index_matrix.append(np.array(it_label.multi_index))
                validation_sourceofpixel.append(i+11)
            else:
                pass
            it_feature0.iternext()
            it_feature1.iternext()
            it_feature2.iternext()
            it_feature3.iternext()
            it_feature4.iternext()
            it_label.iternext()    
    tempdic_validation = {'label':validation_isolated_label , 'source_of_pixel':validation_sourceofpixel, 'index_of_pixel':validation_index_matrix}
    validation_label = pd.DataFrame(data=tempdic_validation)
    tempdic_validation = {'feature0':validation_isolated_feature0,'feature1':validation_isolated_feature1,'feature2':validation_isolated_feature2,'feature3':validation_isolated_feature3,'feature4':validation_isolated_feature4}
    validation_feature=pd.DataFrame(data=tempdic_validation)
    return validation_label,validation_feature

