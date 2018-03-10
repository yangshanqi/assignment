
# coding: utf-8

# In[3]:

import matplotlib
import matplotlib.pyplot as plt


# In[1]:

#plot the original plot
def plot_image(data,stuck,slices,features,alphapara,cmap):
    target_data=data[stuck][0][0][0][0][:,:,slices,features]
    target_image=target_data.reshape(target_data.shape[0],target_data.shape[1])
    plt.imshow(target_image,cmap,alpha=alphapara)
    plt.axis("off")



# In[2]:

# plot the 5 features of one slice of the data
def plot_set_images(data,stuck,slices):
    alphapara = 1;
    cmap = matplotlib.cm.binary
    features = 0
    plt.subplot(151)
    plt.title("T2 weighted")
    plot_image(data,stuck,slices,features,alphapara,cmap)

    plt.subplot(152)
    plt.title("ADC")
    plot_image(data,stuck,slices,features+1,alphapara,cmap)

    plt.subplot(153)
    plt.title("Ktrans")
    plot_image(data,stuck,slices,features+2,alphapara,cmap)
    
    plt.subplot(154)
    plt.title("Kep")
    plot_image(data,stuck,slices,features+3,alphapara,cmap)

    plt.subplot(155)
    plt.title("PET")
    plot_image(data,stuck,slices,features+4,alphapara,cmap)
    plt.show()

#Based on the last plot. plot the prediction of the expert also.    
def plot_orinale_image_with_prediction(data,stuck,index,slices,features):
    cmap1 = matplotlib.colors.LinearSegmentedColormap.from_list('my_cmap',['black','green','blue'],256)
    target_data=data[stuck][0][0][0][0][:,:,slices,features]
    target_image1=target_data.reshape(target_data.shape[0],target_data.shape[1])
    target_label=data[stuck][0][0][0][index][:,:,slices]
    target_image2=target_label.reshape(target_label.shape[0],target_label.shape[1])
    plt.imshow(target_image1,cmap = matplotlib.cm.binary,alpha=0.8)
    plt.imshow(target_image2,cmap = cmap1,interpolation="bilinear",alpha=0.2)
    plt.axis("off") #close the axis number
    plt.show()