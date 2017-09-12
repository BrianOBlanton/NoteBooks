
# coding: utf-8

# In[7]:

# Example of iRODS get in Python client API
# Just file in your password and file names

# Need to make sure irods client API is installed in your env:
# pip install git+git://github.com/irods/python-irodsclient.git

# See for more info: https://github.com/iPlantCollaborativeOpenSource/python-irodsclient/blob/master/README.md

import os
import tempfile
from irods.session import iRODSSession
import netCDF4


irods_path = "/eesZone/home/bblanton/jan.nc"
local_path = "banana.nc"
local_f = None
irods_f = None

# get irods session
sess = iRODSSession(host='ees.renci.org', port=1247, user='bblanton', password='renci!ees', zone='eesZone')

# get irods object info
obj = sess.data_objects.get(irods_path)

# now do actual iget to local file
try:
    # open irods data object file
    with obj.open("r") as irods_f:
        data = irods_f.read()
            
    # write to local file 
    with open(local_path, 'w+') as local_f:
        local_f.write(data)
            
except Exception as ex:
    print("Unable to iget: " + irods_path)
finally:
    # close everything
    if local_f is not None:
        local_f.close()
    if irods_f is not None:
        irods_f.close()


# In[3]:

print irods_f
# nc=netCDF4.Dataset(local_path)


# In[4]:

print data


# In[5]:

print obj.manager


# In[ ]:



