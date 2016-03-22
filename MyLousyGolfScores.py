
# coding: utf-8

# In[1]:

import numpy as np
import tables as PyT
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')


# In[2]:

f=pd.read_csv('golf_data.csv',parse_dates={'dt':[0]})


# In[3]:

n9=f.shape[0]/9


# In[4]:

d=np.flipud(np.reshape(f.Score,(n9,9)))
r=np.sum(d,axis=1)
t=np.flipud(np.reshape(f.dt,(n9,9)))
t=t[:,0]


# In[5]:

print d.shape, t.shape[0]
print t[0]
print r[0]


# In[6]:

plt.figure(figsize=(10,6))
plt.plot(np.sum(d,axis=1),'ro-')


# In[ ]:



