
# coding: utf-8

# # Example of working with HYCOM output available on the hycom.org tds

# In[10]:

# Import packages we'll need
import netCDF4
import matplotlib.pyplot as plt
import numpy as np 
import datetime as dt  # Python standard library datetime  module
import math as math
from pylab import quiver
from mpl_toolkits.basemap import Basemap
get_ipython().magic(u'matplotlib inline')


# In[11]:

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]
def find_nearest_idx(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx


# In[12]:

# open pipes to hycom output
url='http://tds.hycom.org/thredds/dodsC/GLBa0.08/expt_91.1/2015'
nc=netCDF4.Dataset(url)
print 'Available variables are: ' +  str(nc.variables.keys())


# In[13]:

print nc


# In[14]:

# create variables for u,v,x,y,depth
lon=nc.variables['Longitude']
lat=nc.variables['Latitude']
latmin = np.mean(lat)  # needed for scaling lon/lat plots
depth=nc.variables['Depth']

lon_d=lon[1,:]
lat_d=lat[:,1]
depth_d=depth[:]

# extrat subgrid
lon1=262
lon2=295
lat1=7
lat2=32

ilon1=find_nearest_idx(lon_d, lon1)
ilon2=find_nearest_idx(lon_d, lon2)
ilat1=find_nearest_idx(lat_d, lat1) 
ilat2=find_nearest_idx(lat_d, lat2)

lon_d=lon_d[ilon1:ilon2]
lat_d=lat_d[ilat1:ilat2]

# create grid for plotting
lons,lats = np.meshgrid(lon_d,lat_d)


# In[15]:

# specify time level
it=1
Time=nc.variables['Date']
print Time
time=Time[it]
print time


# In[16]:

# 
var1_name='ssh'
var1=nc.variables[var1_name]

var1_d=var1[it,ilat1:ilat2,ilon1:ilon2]
vmin=var1_d.min()
vmax=var1_d.max()

# This min/max calc won't work in general, but is OK for data relatively well distributed about 0
vminmax=math.ceil(2*max(abs(vmin),abs(vmax)))/2
print vmin,vmax,vminmax


# In[17]:

ilev=1   # specify vertical level to extract
uvel_name='u'
uvel=nc.variables[uvel_name]
uvel_d=uvel[it,ilev,ilat1:ilat2,ilon1:ilon2]
uvel_min=uvel_d.min()
uvel_max=uvel_d.max()
print uvel_min,uvel_max
vvel_name='v'
vvel=nc.variables[vvel_name]
vvel_d=vvel[it,ilev,ilat1:ilat2,ilon1:ilon2]
vvel_min=vvel_d.min()
vvel_max=vvel_d.max()
print vvel_min,vvel_max


# In[21]:

# Let's plot ssh, for a test
fig = plt.figure(figsize=(18,9), dpi=144)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8]) 
ax.set_aspect(1.0/np.cos(latmin * np.pi / 180.0))

pc=plt.pcolormesh(lons, lats, var1_d, cmap=plt.cm.jet, vmin=-vminmax, vmax=vminmax)
plt.title("%s\n%s @ %s" % (nc.title, var1_name, time), fontsize=30)
plt.grid(True)
plt.xlim((lon1,lon2))
plt.ylim((lat1,lat2))
plt.tick_params(axis='both', which='major', labelsize=20)

ivecstride=5

Q = quiver(lons[::ivecstride, ::ivecstride],lats[::ivecstride, ::ivecstride], 
           uvel_d[::ivecstride , ::ivecstride], vvel_d[::ivecstride, ::ivecstride], angles='xy',scale_units='xy',scale=1)

# add colorbar
cbax = fig.add_axes([0.80, 0.1, 0.05, 0.8]) 
cb = plt.colorbar(pc, cax=cbax,  orientation='vertical')
cb.set_label(var1.units, fontsize=24)
cb.ax.tick_params(axis='both', which='major', labelsize=20)


# In[ ]:



