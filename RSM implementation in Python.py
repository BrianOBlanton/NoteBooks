
# coding: utf-8

# import matlab .mat file into python
# 

# In[1]:

#import tables
import h5py
import numpy as np

mf='temp.mat';


f = h5py.File(mf, "r")
#f = tables.openFile(mf, "r")


# In[78]:

#print f.keys()
#for name in f:
#     print name
"P" in f
c=np.squeeze(f['c'][:])
k=np.squeeze(f['k'][:])
Nd=np.squeeze(f['n_d'][:])
P=np.transpose(f['P'][:])
R=np.transpose(f['R'][:])
weights=np.squeeze(f['weights'][:])
index=np.squeeze(f['index'][:])
xtest=np.squeeze(f['X'][:])
xtest=np.squeeze(np.transpose(xtest))
print P.shape, type(P), P[45,4]
print R.shape, type(R), R[45,4]
print c.shape, type(c), c
print xtest.shape,xtest[0]
print type(index), index


# In[151]:

def central_ckv (P,R,c,k,weights,Nd,index,xtest):
    
    P=np.transpose(P)
    ni=index.shape[0]
    index=(index-1).astype(int)    
    print index, ni
    
    # normalization of model parameters 
    v_aux=np.diag(1/np.mean(P,axis=1))
    
    # convert model parameters to normalised space
    Normalized_P=np.dot(v_aux,P)
    
    # number of support points
    NSupportPoints=Normalized_P.shape[1];  
    Weight_Matrix=np.diag(weights/np.std(Normalized_P,axis=1)); 
    mean_R=np.mean(R,axis=0); 
    std_R=np.std(R,axis=0);

    for i in range(0,1): # NSupportPoints):
        aux=np.empty
        for j in range(0,ni):
            ii=index[j]
            print i,j,ii,ni,index[j:ni]
            temp=[Normalized_P[ii,i]*Normalized_P[index[j:ni],i]];
            print aux.shape,temp.shape
            aux=np.column_stack((aux, temp))



    print temp, aux
    #print Weight_Matrix
    #print c*k
    #print P[45,4],R[45,4]
    #print xtest[0]
    #print v_aux.shape,P.shape, type(P)
    #print p.shape, type(p)
    #print type(v_aux),type(P)
    #print v_aux
    #print NSupportPoints


# In[152]:

central_ckv(P,R,c,k,weights,Nd,index,xtest)


# In[ ]:

x1 = np.arange(9.0).reshape((3, 3))
x2 = np.arange(3.0)
print type(x1),type(x2)
print x1.shape
print x2.shape
np.multiply(x1, x2)
    


# In[22]:

x = np.arange(10)
print x
print x[2]
print x[-2]
print x[2:5:1]
print x[1:7:2]


# In[19]:

x.shape = (2,5) 
print x
print x[1,3]
print x[0][2], x[0,2]


# In[ ]:



