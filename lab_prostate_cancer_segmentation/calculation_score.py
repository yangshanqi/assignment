
# coding: utf-8

# In[1]:
import numpy as np
# calculate related indicators according to the defination on DPR slides.
def cal_score (y_pred,y_val):
    n11 = 0
    n12 = 0
    n21 = 0
    n22 = 0
    y_pred_array= np.array(y_pred)
    y_val_array= np.array(y_val)
    for j in range(len(y_pred_array)):
        if (y_pred_array[j]==2)&(y_val_array[j]==2):
            n22 = n22+1
        elif (y_pred_array[j]==1)&(y_val_array[j]==2):
            n12 = n12 +1
        elif (y_pred_array[j]==2)&(y_val_array[j]==1):
            n21 = n21+1
        else:
            n11 = n11+1 
    try:       
        Precall = n22 / ( n12 + n22)
        Pprecision = n22 / ( n21 + n22)
        f1_score = 2 / (1/Precall + 1/Pprecision)
        FPR = n21/(n21 + n11)
        FNR = n12/(n12 +n22 )
        BER = 1/2*(FPR+FNR)
        #print ("n11:"+str(n11)+"   n12:"+str(n12)+"   n21:"+str(n21)+"   n22:"+str(n22))
        #print ("TPR:"+str(Precall)+"   f1 score:" + str(f1_score)+"   FPR:"+ str(FPR)+"   BER:" + str(BER))
        return Precall,f1_score,BER,FPR
    except Exception as ex:
        #print ("divided by zero, just skip")
        return 0,0,0,0

