
# coding: utf-8

# In[1]:

url='http://opendap.renci.org:1935/thredds/dodsC/Experiments/Isabel_ex1/ADCIRC/12km/n01/maxele.63.nc'


# In[2]:

which ncgeodataset


# In[3]:

nc=ncgeodataset(url)


# In[4]:

g=ExtractGrid(nc)


# In[5]:

colormesh2d(g,'z');axeq;axtt;set(gca,'FontSize',6)


# In[ ]:



