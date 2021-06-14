#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import re
from IPython.display import YouTubeVideo as yt


# In[2]:


df = pd.read_csv('cleaned salary.csv')


# ## State field

# In[3]:


len(df.loc[46,'Location'].split(', '))


# In[4]:


df.index


# In[5]:


df.loc[106,'Location']


# In[6]:


x = df.loc[106,'Location'].split(', ')
x


# In[7]:


len(x)


# In[8]:


x[1]


# In[9]:


for i in df.index:
    if len(df.loc[i,'Location'].split(', ')) == 1:
        pass
    if len(df.loc[i,'Location'].split(', ')) == 3:
#         print(i)
        df['City'] = df.loc[i,'Location'].split(', ')[1]
#         print('after 3 items')
df[df['Location'] == 'Westlake Village, Los Angeles, CA']['City']


# In[10]:


lin = []

for i in df.index:
#     if len(df.loc[i,'Location'].split(', ')) == 1:
# #         pass
    if len(df.loc[i,'Location'].split(', ')) == 3:
        lin.append(i)
lin[:5]


# In[11]:


df.loc[760,'City']


# In[12]:


for i in df.index:
    if len(df.loc[i,'Location'].split(', ')) == 3:
        df.loc[i, 'City'] = df.loc[i, 'Location'].split(', ')[1]
    elif len(df.loc[i,'Location'].split(', ')) == 2:
        df.loc[i, 'City'] = df.loc[i, 'Location'].split(', ')[0]
    else:
        df.loc[i, 'City'] = np.nan
        
df[df['Location'] == 'University City, St. Louis, MO'][['Location', 'City']],df[df['Location'] == 'Westlake Village, Los Angeles, CA'][['Location', 'City']],df[df['Location'] == 'Prairie Village, Johnson, KS'][['Location', 'City']],df[df['Location'] == 'Sandy Springs, Fulton, GA'][['Location', 'City']]


# In[13]:


df['City'] = df['Location'].apply(lambda x: x.split(', ')[0])
df['State'] = df['Location'].apply(lambda x: x.split(', ')[1])
df[['Location', 'City']].head()


# In[14]:


df['Location'].apply(lambda x: x.split(', ')).loc[2][1]


# In[15]:


df['Location'].apply(lambda x: x.split(', '))


# In[16]:


place = df['Location'].apply(lambda x: x.split(', '))


# In[17]:


place.head()


# In[18]:


place.loc[0][1]


# In[19]:


place[1]


# In[20]:


df.loc[1,'State'] = df.loc[1,'Location'].split(', ')[1]
df[['Location', 'City', 'State']].head(2)


# In[21]:


state = df['Location'].apply(lambda x: x.split(', '))
state.head()
df[['Location', 'State']].head(2)


# In[22]:


state.loc[4][1]


# In[23]:


df.loc[4,'Location']


# In[24]:


df.loc[4,'Location'].split()


# In[25]:


df.loc[4,'Location'].split(', ')


# In[26]:


df.loc[4,'Location'].split(', ')[0]


# In[27]:


df.loc[4,'Location'].split(', ')[1]


# In[28]:


df.index


# In[29]:


[df.loc[i, 'Location'].split(', ')[0] for i in df.index]


# In[30]:


place.head()


# In[31]:


place.value_counts()


# Problem is, some places had no city name. I suspect some have city name, but no state... So... What to do about this? How did this suspision come about? That index error... Why should it throw that error when I "know" that there are two items in each cell? Unless, of course, that is not the case... So, how do we confirm this?

# In[32]:


df['City'].unique()


# In[33]:


df['City'].nunique()


# In[34]:


df['City'].value_counts()


# In[35]:


type(place), len(place)


# In[36]:


len(place.loc[1])


# Test and see if place has 2 elements. If it does not, print out. To see what we get back. Using this to confirm the suspicion that there are certain locations with only one entry, as opposed to the dual city/state expected...
# 
# Also, add an NaN to the place element with one item...

# In[37]:


place = df['Location'].apply(lambda x: x.split(', '))

stateless = []

for i in range(len(place)):
    if len(place.loc[i]) == 1:
        place.loc[i].append(np.nan)
        stateless.append(place[i][0])
stateless


# In[38]:


p = pd.DataFrame(place)
p['Location'].str.contains('Remote')


# In[39]:


len(stateless)


# In[40]:


pd.Series(stateless).nunique(), pd.Series(stateless).unique()


# And that was indeed the case!
# 
# The possibilities! 
# 
# So, do I figure out how to transform these places that are state names into states, then have the cities be missing values? Or should I just do away with them? The former seems to me a better option. I can vaguely see a solution to this... But, I also see that will need some digging. Do I want to do that? Hmm... Trade-offs...
# 
# For those names I saw in the list of cities that are other countries (Brazil, Germany, Prague...), how do I handle those? What's the best way to deal with that? 
# 
# This venture looks like it will take me down some very deep rabbit holes... And we haven't even gotten to the actual EDA. This is just purely cleaning the data.

# In[41]:


df['State'] = place.apply(lambda x: x[1])


# In[42]:


df[['Location', 'City', 'State']].sample(10)


# Hmm... So those cities with country names (Brazil, Germany, Prague, et. al...), are they actual cities? Let's see...

# In[43]:


df[df['City'] == 'Brazil'][['Location', 'City', 'State']]


# In[44]:


df[df['City'] == 'Germany'][['Location', 'City', 'State']].sample()


# In[45]:


df[df['City'] == 'Prague'][['Location', 'City', 'State']]


# In[46]:


df[df['City'] == 'Italy'][['Location', 'City', 'State']]


# Turns out that these are actual city names... Checked each of those and they are bona fide...
# 
# And there is a place called Location. Huh!
# 
# Also checked Vienna. And USAF Academy. And King of Prussia.

# In[47]:


df[df['City'] == 'Location'][['Location', 'City', 'State']].sample()


# In[48]:


df[df['City'] == 'King of Prussia'][['Location', 'City', 'State']]


# In[49]:


df[df['City'] == 'Vienna'][['Location', 'City', 'State']]


# In[50]:


df[df['City'] == 'United States Air Force Acad'][['Location', 'City', 'State']]


# Checked on Remote and USA... The for loop worked in replacing missing item with NaN.
# 
# My suspicion... Remote might mean the job is listed as one that can be done remotely... Will verify with data in other columns. Keep it for now.

# In[51]:


df[df['City'] == 'Remote'][['Location', 'City', 'State']]


# In[52]:


df[df['City'] == 'United States'][['Location', 'City', 'State']]


# There are only 38 locations that are missing second item. And from cursory glance, majority USA and Remote. So this should work... So let's do this...

# In[53]:


pd.Series(stateless).value_counts()


# Yup, this confirms that majority of single item are US and Remote. The rest each have just one entry...
# 
# So... I have to loop through. If only one entry, if state name, then have first entry in place be NaN, second place be state. Get abbreviation for state programmatically.
# 
# If US or Remote, then list NaN for both city and state. Add column indicating presence or lack thereoff of city/state? So 1 if city state is there, 0 if not. Also another column of Remote... 1 if so, 0 if not...

# In[54]:


place


# In[55]:


pd.DataFrame(df['City'].unique(), columns = ['City']).sort_values(by = 'City').to_excel('city.xlsx', index = False)


# In[56]:


df[['Location', 'City', 'State']].head(10)


# In[57]:


df['State'].nunique(), df['State'].unique()


# Found more states! Some locations had two city names... So have to figure out how to deal with this. Fortunately, it is just 4 locations, 5 jobs...

# In[58]:


df[df['State'] == 'St. Louis'][['Location', 'City', 'State']]


# In[59]:


df[df['State'] == 'Johnson'][['Location', 'City', 'State']]


# In[60]:


df[df['State'] == 'Fulton'][['Location', 'City', 'State']]


# In[61]:


df[df['State'] == 'Los Angeles'][['Location', 'City', 'State']]


# Solved by indexing last item in `place` list.

# In[62]:


df['State'] = place.apply(lambda x: x[-1])
df['State'].nunique(), df['State'].unique()


# In[63]:


df[df['Location'] == 'University City, St. Louis, MO'][['Location', 'City', 'State']],df[df['Location'] == 'Westlake Village, Los Angeles, CA'][['Location', 'City', 'State']],df[df['Location'] == 'Prairie Village, Johnson, KS'][['Location', 'City', 'State']],df[df['Location'] == 'Sandy Springs, Fulton, GA'][['Location', 'City', 'State']]


# Need to fill remote in states with city remote...

# In[64]:


df.loc[df['City'] == 'Remote', 'State'] = 'Remote'


# Remote fixed.
# 
# Now to sort out United States...

# In[65]:


df['State'].isnull().sum()


# In[66]:


df[(df['State'].isnull()) & (df['City'] == 'United States')]                            [['Job Title', 'Location', 'City', 'State']]


# There are only 17 rows with United States as City out of 1860 rows, so I can afford to drop those rows...
# 
# Looking at the job description, I see two that show remote... Therefore I could have gotten those two as part of the remote jobs... But for now I have just decided to get rid of all

# In[67]:


df = df[df['City'] != 'United States']


# That leaves us with 6 jobs where we need to fix state (leaving city blank). City could be obtained from search of company online, but for now I will not explore that option. 

# In[68]:


df[df['State'].isnull()][['Location', 'City', 'State']]


# First changing city to unknown...

# In[69]:


df.loc[df['State'].isnull(), 'City'] = 'Unknown'
df[df['State'].isnull()][['Location', 'City', 'State']]


# Now to make Location State...
# 
# Get list of US states and their abbreviations...

# In[70]:


states = pd.read_csv('us-states.csv', sep = ' - ', engine = 'python', header = None,
                     names = ['State', 'Abbreviation'])
states.head()


# In[71]:


df.loc[df['State'].isnull(), 'Location']


# In[72]:


list(states['State'].unique())


# In[73]:


df.loc[127, 'Location'] in list(states['State'].unique())


# In[74]:


x = df.loc[127, 'Location']
x


# In[75]:


y = states[states['State'] == 'New Jersey']['Abbreviation']
y


# In[76]:


list(y)[0]


# In[77]:


dfs = df[df['State'].isnull()][['Location', 'City', 'State']]
dfs


# In[78]:


dfs.loc[127, 'State'] = list(y)[0]
dfs


# In[79]:


for i in df.index:
    if df.loc[i, 'Location'] in list(states['State'].unique()):
        state_full = df.loc[i, 'Location']
        state_abbrev = list(states[states['State'] == state_full]['Abbreviation'])[0]
        df.loc[i, 'State'] = state_abbrev


# In[80]:


df[df['City'] == 'Unknown'][['Location', 'City', 'State']]


# In[81]:


df['State'].nunique(), df['State'].unique()


# In[82]:


df[['Location', 'Salary Average', 'City', 'State']].sample(20)


# In[83]:


df['State'].value_counts()


# In[84]:


df.to_csv('cleaned state.csv', index = False)


# # Done! Yowzah! 
