
# coding: utf-8

# In[191]:

import numpy as np
import tables as PyT
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')


# In[192]:

f=pd.read_csv('golf_data.csv',parse_dates={'dt':[18]})


# In[199]:

NumberOfRounds=f.shape[0]/9
print "Number of 9-hole rounds = " + str(NumberOfRounds)
# slopes/ratings (divided by 2 for 18-hole courses)
# Hillandale slope = 112, rating = 64.5/2
# Occoneechee slope = 124, rating 68.6/2
# Twin Lakes slope = 113, rating = 34.2
# Lakeshore slope = 117, rating = 67.3/2
ratings = {'Hillandale Golf Course': 64.5/2, 'Occoneechee Golf Club': 68.6/2, 'Twin Lakes Golf Course': 34.2, 'Lakeshore Golf Course': 67.3/2}
slopes  = {'Hillandale Golf Course': 112,    'Occoneechee Golf Club': 124, 'Twin Lakes Golf Course': 113, 'Lakeshore Golf Course': 117}

Courses=np.flipud(np.reshape(f.Course,(NumberOfRounds,9)))
Courses=Courses[:,0]
#print set(Courses)

CourseRatings=np.ones([NumberOfRounds,])
for i in range(0,Courses.shape[0]):
    CourseRatings[i]=ratings[Courses[i]]


# In[200]:

PerHoleScores=np.flipud(np.reshape(f.Score,(NumberOfRounds,9)))
RoundScores=np.sum(PerHoleScores,axis=1)
t=np.flipud(np.reshape(f.dt,(NumberOfRounds,9)))
dates=t[:,0]


# In[201]:

regression = np.polyfit(range(0,NumberOfRounds), RoundScores, 1)
r_x, r_y = zip(*((i, i*regression[0] + regression[1]) for i in range(NumberOfRounds)))
regression2 = np.polyfit(range(1,NumberOfRounds), RoundScores[1:], 1)
r2_x, r2_y = zip(*((i, i*regression2[0] + regression2[1]) for i in range(NumberOfRounds)))


# In[202]:

plt.figure(figsize=(10,6))
plt.plot(RoundScores,'ro-')
plt.ylabel("9-hole score",fontsize=14)
plt.xlabel("Round number",fontsize=14)
plt.grid(True)
plt.plot(r_x, r_y, color="red")
plt.plot(r2_x, r2_y, color="blue")
lstr=[]
lstr.append('Scores')
lstr.append('All rounds')
lstr.append('Excluding first (83)')
plt.legend(lstr, fontsize=12);


# In[203]:

#plt.hist(RoundScores)


# In[204]:

# adjusted gross score
# max of 9 on any hole
PerHoleScores_adj=np.copy(PerHoleScores);
PerHoleScores_adj[PerHoleScores_adj>9]=9
RoundScores_adj=np.sum(PerHoleScores_adj,axis=1)
regression_adj = np.polyfit(range(0,NumberOfRounds), RoundScores_adj, 1)
r_x_adj, r_y_adj = zip(*((i, i*regression_adj[0] + regression_adj[1]) for i in range(NumberOfRounds)))


# In[213]:

plt.figure(figsize=(10,6))
plt.plot(RoundScores,'ro-')
plt.plot(RoundScores_adj,'g*-')
#plt.plot(64.5*np.ones([NumberOfRounds+1,1]),'b-')
plt.ylabel("9-hole score",fontsize=14)
plt.xlabel("Round number",fontsize=14)
plt.grid(True)
plt.plot(r_x, r_y, color="red")
plt.plot(r_x_adj, r_y_adj, color="green")
lstr=[]
lstr.append('Raw Scores')
lstr.append('Adjusted Scores')
#lstr.append('Hillandale Course Rating')
#lstr.append('Excluding first (83)')
plt.legend(lstr, fontsize=12);


# In[215]:

## Handicap differential = (Adjusted Gross Score - Course Rating) x 113 ÷ Slope Rating
## https://www.golfnow.com/courses/1033123-hillandale-golf-course-details

HandicapDifferential=(RoundScores_adj-CourseRatings)*113/112
# sort hd, and take 10 best
HandicapDifferential=np.sort(HandicapDifferential)
HandicapDifferential=HandicapDifferential[-10:-1]
#hd=np.trunc(hd*10)/10


# In[216]:

MeanHandicapDifferential=np.mean(HandicapDifferential)


# In[217]:

HandiCapIndex=np.trunc(.96*MeanHandicapDifferential*10)/10
print "Handicap Index = " + str(HandiCapIndex)


# In[218]:

# hillandale hc
print 'Hillandale HC = ' + str(int(np.round(HandiCapIndex*slopes['Hillandale Golf Course']/113)))
print 'Occoneechee HC = ' + str(int(np.round(HandiCapIndex*slopes['Occoneechee Golf Club']/113)))
print 'Twin Lakes HC = ' + str(int(np.round(HandiCapIndex*slopes['Twin Lakes Golf Course']/113)))
print 'Lakeshore HC = ' + str(int(np.round(HandiCapIndex*slopes['Lakeshore Golf Course']/113)))


# In[ ]:



