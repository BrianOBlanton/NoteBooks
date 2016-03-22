
# coding: utf-8

# # Quick Python notebook to illustrate COOPS model output things

# In[1]:

# we'll need the netCDF4 class
import netCDF4


# #### First, in the CBOFS output
# The sea level pressure variable (Pair) has units of millibars, but the variable's data is not consistent with this.

# In[2]:

url='http://opendap.co-ops.nos.noaa.gov/thredds/dodsC/NOAA/CBOFS/MODELS/201601/nos.cbofs.fields.f000.20160127.t00z.nc'


# In[3]:

nc=netCDF4.Dataset(url)


# In[4]:

# get the pressure variable
pair = nc.variables['Pair']
pair.units


# In[5]:

pair[:].min(), pair[:].max()


# #### Next, in the CREOFS output:
# The pressure variable is all zero:

# In[6]:

url2='http://opendap.co-ops.nos.noaa.gov/thredds/dodsC/NOAA/CREOFS/MODELS/201601/nos.creofs.fields.n000.20160128.t03z.nc'
nc2=netCDF4.Dataset(url2)
print nc2.variables.keys()


# In[7]:

pair2 = nc2.variables['Pair'][:]
print pair2.min(), pair2.max()


# ##### Plus also, the wind velocity is similarly set. zero

# In[8]:

uwind_speed = nc2.variables['uwind_speed'][:]
print uwind_speed.min(), uwind_speed.max()

vwind_speed = nc2.variables['vwind_speed'][:]
print vwind_speed.min(), vwind_speed.max()


# In[ ]:



