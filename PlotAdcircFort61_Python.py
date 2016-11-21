
# coding: utf-8

# In[1]:

import netCDF4
import matplotlib.pyplot as plt
import numpy as np
import time as TIME
import datetime
import math as math
get_ipython().magic(u'matplotlib notebook')


# In[2]:

url='http://opendap.renci.org:1935/thredds/dodsC/tc/matthew/00/nc_inundation_v9.99_w_rivers/hatteras.renci.org/hindmatt/gahm/fort.61.nc'
#http://localhost:8080/thredds/dodsC/testAll/fort.61.nc'
var_name='zeta'
nc=netCDF4.Dataset(url)
print nc.variables.keys()


# In[3]:

time=nc.variables['time']
var=nc.variables[var_name]
dtime = netCDF4.num2date(time[:],time.units)
tstart=dtime[0].strftime('%Y-%b-%d')
tstr=nc.comments
#print tstr/
sn=nc.variables['station_name']
lstr=[]
for i in range(sn.shape[0]) :
    temp=sn[i,:].tostring()
    temp=temp.strip('\x00')  # gets rid of some garbage in the strings
    lstr.append(temp)

for p in lstr: print p


# In[5]:

fig = plt.figure(figsize=(12,6))
pc=plt.plot(dtime,var)
plt.title("%s\n%s\n%s" % (nc.title, var.long_name, tstr), fontsize=20)
plt.grid(True)
plt.tick_params(axis='both', which='major', labelsize=10)
plt.ylabel("%s\n[%s]" % (var.long_name, var.units), fontsize=20)
plt.legend(lstr, fontsize=8)


# In[52]:

#plt.hist2d
y=np.transpose(var[:,0])
fig = plt.figure(figsize=(4,4), dpi=72)
h=plt.hist(y,bins=25);
x=h[1]
y2=h[0]
pdf=y2/len(y)

cdf=(np.cumsum(pdf))
fig = plt.figure(figsize=(4,4), dpi=72)
plt.plot(x[0:-1],cdf)
#print cdf


# In[ ]:

plt.plot(x,cdf)


# ## Let's build an OPeNDAP url to retrieve NOAA gauge data directly into python

# In[142]:

STATION_ID="8651370"
DATUM="MSL"
BEGIN_DATE="19810101 00:00"
END_DATE  ="19820101 00:00"
url=['http://opendap.co-ops.nos.noaa.gov/dods/IOOS/Hourly_Height_Verified_Water_Level?',
     'WATERLEVEL_HOURLY_VFD_PX.DATE_TIME,',
     'WATERLEVEL_HOURLY_VFD_PX.WL_VALUE&',
     'WATERLEVEL_HOURLY_VFD_PX._STATION_ID="%s"&',
     'WATERLEVEL_HOURLY_VFD_PX._DATUM="%s"&',
     'WATERLEVEL_HOURLY_VFD_PX._BEGIN_DATE="%s"&',
     'WATERLEVEL_HOURLY_VFD_PX._END_DATE="%s"'
     ]
url[3] = url[3] % STATION_ID
url[4] = url[4] % DATUM
url[5] = url[5] % BEGIN_DATE
url[6] = url[6] % END_DATE

FullUrl="".join(url)
nc2=netCDF4.Dataset(FullUrl)


# In[149]:

print nc2.variables.keys()
wl=nc2.variables['WATERLEVEL_HOURLY_VFD_PX.WL_VALUE']
time=nc2.variables['WATERLEVEL_HOURLY_VFD_PX.DATE_TIME']
print time


# In[175]:

print time.name


# In[147]:

### the time data returned above is in an almost useless format. 
### it's a huge character array

print np.size(time[:,0])

for i in range(0,np.size(time[:,0])) :
    print i
    temp="".join(time[i,:])
    t.append(TIME.strptime(temp,"%b %d %Y %I:%M%p"))


# In[41]:

###     

# let's build a datetime vector, assuming hourly data


import datetime 
d = datetime.timedelta(microseconds=-1)
print (d.days, d.seconds, d.microseconds)
print datetime.datetime.utcnow()
start=datetime.datetime.strptime(BEGIN_DATE,"%Y%m%d %H:%M")
end=datetime.datetime.strptime(END_DATE,"%Y%m%d %H:%M")
timevec=[start + datetime.timedelta(hours=x) for x in range(0, 1+24*(end-start).days)]
print start,end, "dt=", end-start, timevec[0], timevec[-1], np.shape(timevec)


# In[28]:

print np.shape(timevec), np.shape(wl)


# In[29]:

print 365*24+1


# In[154]:

x = np.arange(10)


# In[155]:

x


# In[158]:

print x[-2]


# In[159]:

print type(x)


# In[166]:

t0=time[100,:]; print t0


# In[ ]:



