
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[9]:


class CalList (object):
    
    def __init__ (self):
        self.tpr_list_cal = []
        self.fpr_list_cal = []
        self.BER_list_cal = []
        self.f1_score_list_cal = []
        
    def list_append (self,Precall,f1_score,BER,FPR):
        self.tpr_list_cal.append(Precall)
        self.fpr_list_cal.append(FPR)
        self.BER_list_cal.append(BER)
        self.f1_score_list_cal.append(f1_score)
        
    def list_average_cal (self):       
        Precall=(sum(self.tpr_list_cal)/len(self.tpr_list_cal))
        FPR=(sum(self.fpr_list_cal)/len(self.fpr_list_cal))
        BER=(sum(self.BER_list_cal)/len(self.BER_list_cal))
        f1_score=(sum(self.f1_score_list_cal)/len(self.f1_score_list_cal))
        return Precall,FPR,BER,f1_score


# In[11]:


class CalParList (CalList):

    def __init__ (self, number_of_parameter, *par_name):
        CalList.__init__(self)
        
        self.parameter_list = []
        for i in range (number_of_parameter):
            column=[]
            self.parameter_list.append(column)
            
        j=0
        self.Name_String = []
        for element in par_name:
            self.Name_String.append(element)
            j=j+1
            
    def list_append (self,Precall,f1_score,BER,FPR,*parameter):
        
        CalList.list_append(self,Precall,f1_score,BER,FPR)
        #self.tpr_list_cal.append(Precall)
        #self.fpr_list_cal.append(FPR)
        #self.BER_list_cal.append(BER)
        #self.f1_score_list_cal.append(f1_score)
              
        interation = 0
        for par in parameter:
            self.parameter_list[interation].append(par)
            interation = interation +1   
            
    def return_result (self):
        result = {"TPR":self.tpr_list_cal,"FPR":self.fpr_list_cal,"f1_score":self.f1_score_list_cal,"BER":self.BER_list_cal}
        
        for i in range(len(self.Name_String)):
            result[self.Name_String[i]]=self.parameter_list[i]
        
        columns = self.Name_String
        columns.append("f1_score")
        columns.append("TPR")
        columns.append("FPR")
        columns.append("BER")
        result = pd.DataFrame (data=result,columns=columns)
        
        return result

