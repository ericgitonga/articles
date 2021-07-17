#!/usr/bin/env python
# coding: utf-8

import pandas as pd

# Read in the data as a multi-hierarchical dataframe
df = pd.read_excel("Mock-Up Data.xlsx", header=[0,1])
df.head(2)


# If you want to get a list of columns, you will get a list of tuples (main name, sub-name).  
# We want a list of just main name, so iterate over the column names and form a new list of unique column names.  
# We want all but the first group of columns...
items = []
for i in list(df.columns):
    if i[0] not in items and not i[0].startswith("Unnamed"):
        items.append(i[0])

# We now extract the columns under each main column name and set that as its own dataframe... We use the `globals()` function to create sequential variable names for the different dataframes.
dftest = []
for i, val in enumerate(items):
    globals()["df%s" %i] = df[[val]]
    dftest.append(globals()["df%s" %i])

# We need to define two functions...
# 1. df_flatten will help flatten the multi-hierarchical dataframe into a flat dataframe. We use the `to_records()` method for this.
# 2. df_organize will move the date column to the start of the dataframe.
def df_flatten(df):
    df = pd.DataFrame(df.to_records())
    df.drop("index",axis="columns",inplace=True)
    return df

def df_organize(df,index):
    date = df[list(df.columns)[index]]
    df = df.drop(['date'],axis=1)
    df.insert(0,'date',date)    
    return df

# We shall create a new list of the dataframes. We will process them so that for each dataframe we got:
# 1. Flatten it
# 2. Rename the columns
# 3. Add a date column
# 4. Move the date column to the beginning of the dataframe
reorg_dfs = []

for i, value in enumerate(dftest):
    value = df_flatten(value)
    value.columns = ["Revenue", "Customers", "#Orders", "Order frequency"]
    value["date"] = items[i]
    value = df_organize(value,-1)
    reorg_dfs.append(value)

# We also want to create a dataframe of the first 3 columns of the spreadsheet. So subset it from the main dataframe, then flatten it and rename the columns.
dfa = df.iloc[:,:3]
df_flatten(dfa)
dfa.columns = ["agent_id", "Location", "Agent_age_Months"]

# Now we want to create a new list of dataframes. These dataframes are concatenations of the first 3 columns and the 4 columns of each of the period dataframes.
d = []
for i, val in enumerate(reorg_dfs):
    globals()["d%s" %i] = pd.concat([dfa,reorg_dfs[i]],1)
    d.append(globals()["d%s" %i])
df_final = pd.concat(d,ignore_index=True)

# Now we move the date column to the beginning.  
# Then we convert it from the given format to the MMM-DD format.
df_final = df_organize(df_final,3)
df_final["date"] = pd.to_datetime(df_final["date"])
df_final["date"] = df_final["date"].apply(lambda x: x.strftime("%b-%d"))

# Finally we write the dataframe to file.
df_final.to_excel("fiona.xlsx",index=False)
