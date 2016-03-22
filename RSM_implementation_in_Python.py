
# coding: utf-8

# import matlab .mat file into python
# 

# In[1]:

from pylab import *
import matplotlib.tri as Tri
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')

#import tables
import h5py
import numpy as np
import numpy.matlib as ml
import numpy.linalg as la


# In[2]:

# get the model in a matlab file, stored as -v7.3
# the model components must be saved as individual variables, 
# not as a struct.  See the matlab code structfields2vars
mf='temp3.mat';
#f = tables.openFile(mf, "r")
f = h5py.File(mf, "r")
print f


# In[3]:

print f.keys()
#for name in f:
#     print name
print "P" in f
c=np.squeeze(f['c'][:])
k=np.squeeze(f['k'][:])
Nd=np.squeeze(f['n_d'][:])
P=np.transpose(f['P'][:])
R=np.transpose(f['R'][:])
weights=np.squeeze(f['weights'][:])
index=np.squeeze(f['index'][:])
#xtest=np.squeeze(f['X'][:])
xtest=np.array([ 66.8, 1.06, 7.5, 38, 5.23, 5.25])
xtest=np.squeeze(np.transpose(xtest))

p1=xtest[0]
p2=xtest[1]
p3=xtest[2]
p4=xtest[3]
p5=xtest[4]
p6=xtest[5]

p1min=np.min(P[:,0]); p1max=np.max(P[:,0])  # rmw
p2min=np.min(P[:,1]); p2max=np.max(P[:,1])  # H_b
p3min=np.min(P[:,2]); p3max=np.max(P[:,2])  # TS
p4min=np.min(P[:,3]); p4max=np.max(P[:,3])  # Vmax
p5min=np.min(P[:,4]); p5max=np.max(P[:,4])  # LatNorth
p6min=np.min(P[:,5]); p6max=np.max(P[:,5])  # LatSouth

dp1=(p1max-p1min)/20
dp2=(p2max-p2min)/20
dp3=(p3max-p3min)/20
dp4=(p4max-p4min)/20
dp5=(p5max-p5min)/20
dp6=(p6max-p6min)/20

#print P.shape, type(P), P[45,4]
#print R.shape, type(R), R[45,4]
#print c.shape, type(c), c
#print type(index), index


global c, k, Nd
global P, R, weights, index

# get the FEM grid parts from f to create a triangulation object
lon = np.squeeze(f['x'][:])
lat = np.squeeze(f['y'][:])
latmin = np.mean(lat)  # needed for scaling lon/lat plots
nv  = np.squeeze(f['e'][:,:] -1)
nv=np.transpose(nv)
tri = Tri.Triangulation(lon,lat, triangles=nv)


NodeIndices=np.squeeze(f['NodeIndices'][:])
NodeIndices=(NodeIndices-1).astype(int)


# In[4]:

def master(p1,p2,p3,p4,p5,p6):
    
    global c, k, Nd
    global P, R, weights, index
    
    xtest=np.array([p1,p2,p3,p4,p5,p6])
    temp=central_ckv(P,R,c,k,weights,Nd,index,xtest)
    
    # put response into variable sized as lon.shape
    print tri.x.shape
    zhat=np.zeros(tri.x.shape)
    #zhat.fill(np.nan)
    #print zhat[0:10]
    zhat[NodeIndices]=temp
    
    #print 'Making contours in figure ...'
    fig = plt.figure(figsize=(10,5), dpi=144)
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8]) 
    ax.set_aspect(1.0/np.cos(latmin * np.pi / 180.0))

    #print 'Calling tricontourf  ...'
    vmax=np.max(np.abs(temp))
    levels = linspace(0.,np.ceil(vmax),11)
    #print levels
    
    contour = tricontourf(tri, zhat, levels=levels,shading='faceted')
    plt.grid(True)
    plt.xlim((-80,-74))
    plt.ylim((33,37))
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.title('RSM test in Python', fontsize=16)

    # add colorbar
    cbax = fig.add_axes([0.80, 0.1, 0.05, 0.8]) 
    cb = plt.colorbar(contour, cax=cbax,  orientation='vertical')
    cb.set_label('[m MSL]', fontsize=24)
    cb.ax.tick_params(axis='both', which='major', labelsize=12)
    


# In[5]:

def central_ckv (P,R,c,k,weights,Nd,index,xtest):
    
    one=np.ones(1)
    one=np.expand_dims(one,axis=1)

    P=np.transpose(P)
    ni=index.shape[0]
    index=(index-1).astype(int)    
    
    # normalization of model parameters 
    v_aux=np.diag(1/np.mean(P,axis=1))
    
    # convert model parameters to normalised space
    Normalized_P=np.dot(v_aux,P)
    
    NSupportPoints=Normalized_P.shape[1];  
    Weight_Matrix=np.diag(weights/np.std(Normalized_P,axis=1,ddof=1)); 
    mean_R=np.mean(R,axis=0); 
    mean_R=np.expand_dims(mean_R,axis=1)
    mean_R=np.transpose(mean_R)

    std_R=np.std(R,axis=0,ddof=1);
    std_R=np.expand_dims(std_R,axis=1)

    temp=ml.repmat(mean_R,NSupportPoints,1)
    numer=R-temp

    S=np.array(1/std_R)
    S=np.diag(np.squeeze(S),k=0)
    
    Normalized_R=np.dot(numer,S);

    BasisFxns=np.array([])
    for i in range(0,NSupportPoints): 
        
        for j in range(0,ni):
            ii=index[j]
            temp=np.array([Normalized_P[ii,i]*Normalized_P[index[j:ni],i]])
            temp=np.transpose(temp)

            if (j == 0):
                aux=np.array(temp)
            else:
                aux=np.vstack((aux, temp))
                
        temp=Normalized_P[:,i] 
        temp=np.expand_dims(temp,axis=0)
        aux=np.transpose(aux)
        temp=np.hstack((one,temp, aux))
      
        if (i==0):
            BasisFxns=temp
        else:
            BasisFxns=np.vstack((BasisFxns,temp))
                        
    zhat=sur_model(xtest,v_aux,Weight_Matrix,Normalized_P,Nd,c,k,BasisFxns,Normalized_R,mean_R,std_R,NSupportPoints,index)   
    return zhat


# In[6]:

def sur_model(x,v_aux,Weight_Matrix,Normalized_P,Nd,c,k,BasisFxns,Normalized_R,mean_R,std_R,NSupportPoints,index):

    one=np.ones(1)
    one=np.expand_dims(one,axis=1)
    
    # normalize input vector x
    Normalized_X=np.dot(v_aux,x)
    Normalized_X=np.expand_dims(Normalized_X,axis=1)

    Parameter_Diffs=ml.repmat(Normalized_X,1,NSupportPoints)-Normalized_P
    Parameter_Diffs_Weighted=np.dot(Weight_Matrix,Parameter_Diffs)
    
    temp=np.square(Parameter_Diffs_Weighted,Parameter_Diffs_Weighted)
    temp=np.sum(temp,axis=0)
    temp=np.expand_dims(temp,axis=0)
    Distance=np.sqrt(temp);

    SortedDistanceIndex=np.argsort(Distance); 
    SortedDistance=Distance[0,SortedDistanceIndex]    
    D=SortedDistance[0,Nd.astype(int)-1]
    SelectedStorms=SortedDistanceIndex[0,:Nd.astype(int)]

    f=np.exp(-np.power(1/c,k))
    denom=(1-f)
    numer=np.exp(-(np.power(Distance/D/c,k)))-f
    aux1=numer/denom;

    W=np.diag(aux1[0,SelectedStorms]); 

    Ba=BasisFxns[SelectedStorms,:];
    
    ni=index.shape[0]

    for j in range(0,ni):
        ii=index[j]
        temp=np.array([Normalized_X[ii]*Normalized_X[index[j:ni]]])
        temp=np.squeeze(temp)
        temp=np.expand_dims(temp,axis=1)

        if (j == 0):
            aux=np.array(temp)
        else:
            aux=np.vstack((aux, temp))

    b=np.hstack((one,np.transpose(Normalized_X), np.transpose(aux)))

    # auxiliary matrices
    L=np.dot(np.transpose(Ba),W)
    M=np.dot(L,Ba) 
    
    # auxM are the b'*inv(M)*L coefficients in eqn 24 of Taflanidis 2012
    Mi=la.inv(M)
    temp=np.dot(b,Mi)
    auxM=np.dot(temp,L);

    Fi=Normalized_R[SelectedStorms,:];

    temp=np.dot(auxM,Fi)
    std_R=np.transpose(std_R)

    temp2=temp[0,:]*std_R
    f=temp2+mean_R
    f=np.squeeze(f)
    
    return f


# In[7]:

# evaluate the model at xtest parameters
#zhat=master(p1,p2,p3,p4,p5,p6)


# In[8]:

#from __future__ import print_function # for python 2
from ipywidgets import interact, interactive, fixed
import ipywidgets as widgets


# In[10]:

interact(master,          p1=widgets.FloatSlider(min=p1min,max=p1max,step=dp1,value=p1),         p2=widgets.FloatSlider(min=p2min,max=p2max,step=dp2,value=p2),         p3=widgets.FloatSlider(min=p3min,max=p3max,step=dp3,value=p3),         p4=widgets.FloatSlider(min=p4min,max=p4max,step=dp4,value=p4),         p5=widgets.FloatSlider(min=p5min,max=p5max,step=dp5,value=p5),         p6=widgets.FloatSlider(min=p6min,max=p6max,step=dp6,value=p6))


# In[ ]:



