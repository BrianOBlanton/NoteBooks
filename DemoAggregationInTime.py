
# coding: utf-8

# In[1]:

from pylab import *
import matplotlib.pyplot as plt
import netCDF4 as netCDF4
get_ipython().magic(u'matplotlib inline')


# In[ ]:




# In[3]:

url='http://mrtee.europa.renci.org:8080/thredds/dodsC/DataLayers/oedata_test/fort61.ncml'
#url='http://opendap.renci.org:1935/thredds/dodsC/oedata/fort61.ncml'

#url='http://mrtee.europa.renci.org:8080/thredds/dodsC/testAll/oedata_test/1981/1981.fort.63.nc'
nc=netCDF4.Dataset(url)


# In[4]:

print nc.variables.keys()


# In[5]:

Time=nc.variables['time']
nidx=1  #  node number near Duck
Zeta=nc.variables['zeta']
print Zeta


# In[6]:

time=Time[:]
dtime = netCDF4.num2date(time,Time.units)
zeta=Zeta[:,nidx]


# In[7]:

fig = plt.figure(figsize=(12,6), dpi=144)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
plt.plot(dtime,zeta)


# In[ ]:



