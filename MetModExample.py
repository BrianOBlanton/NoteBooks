
# coding: utf-8

# In[12]:

from mpl_toolkits.basemap import Basemap
import netCDF4
from pylab import *
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from datetime import datetime
import math as math
#get_ipython().magic(u'matplotlib inline')


# In[4]:

url='http://localhost:8080/thredds/dodsC/testAll/2004050300_eta_211.nc'
nc=netCDF4.Dataset(url)
print nc.variables.keys()


# In[5]:

print nc.variables['grid_number'][:]


# In[6]:

Lo1=nc.variables['Lo1'][:]
La1=nc.variables['La1'][:]
Nx=nc.variables['Nx'][:]
Ny=nc.variables['Ny'][:]
Dx=nc.variables['Dx'][:]
Dy=nc.variables['Dy'][:]
print Lo1, La1, Nx, Ny, Dx, Dy


# In[7]:

x = np.linspace(0, 1, Nx)
y = np.linspace(0, 1, Ny)
x,y=meshgrid(x,y)
z=nc.variables['Z_sfc'][0,:,:]
print z.shape


# In[8]:

plt.pcolor(x,y,z)


# In[9]:

#%pinfo Basemap


# In[10]:

llcrnrlon=-160    # lower-left corner, lon
llcrnrlat=  20    # lower-left corner, lat
urcrnrlon= -60    # upper-right corner, lon
urcrnrlat=  60    # upper-right corner, lat
lon_0   =Lo1      # center of desired map domain (in degrees).
lat_1   =La1      # first standard parallel for lambert conformal
m = Basemap(llcrnrlon=llcrnrlon,
            llcrnrlat=llcrnrlat, 
            urcrnrlon=urcrnrlon,
            urcrnrlat=urcrnrlat, 
            projection='lcc',
            resolution ='i',
            area_thresh=1000.,
            lat_1=La1,
            lon_0=Lo1)


# In[11]:

m.drawmapboundary(fill_color='0.8')
m.drawcoastlines(linewidth=1.)
pc=m.pcolor(z, cmap=plt.cm.jet, vmin=0, vmax=1000, latlon=True)



# In[ ]:



