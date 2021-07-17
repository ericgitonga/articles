#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import tkinter as tk
from tkinter import filedialog as fd

# Read in the data as a multi-hierarchical dataframe
root = tk.Tk()
file = fd.askopenfile()
root.destroy()

df = pd.read_excel("../data/mock-up.xlsx", header=[0,1])
df.head(2)


# If you want to get a list of columns, you will get a list of tuples (main name, sub-name).  
# We want a list of just main name, so iterate over the column names and form a new list of unique column names.  
# We want all but the first group of columns...
dates = []
for i in list(df.columns):
    if i[0] not in dates and not i[0].startswith("Unnamed"):
        dates.append(i[0])

# We now extract the columns under each main column name and set that as its own dataframe... We use the `globals()` function to create sequential variable names for the different dataframes.
extracted_dfs = []
for i, val in enumerate(dates):
    globals()["df%s" %i] = df[[val]]
    extracted_dfs.append(globals()["df%s" %i])

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
column_names = []
for i in list(df.columns):
    if i[1] not in column_names and not i[0].startswith("Unnamed"):
        column_names.append(i[1])

reorganized_dfs = []
for i, value in enumerate(extracted_dfs):
    value = df_flatten(value)
    value.columns = column_names
    value["date"] = dates[i]
    value = df_organize(value,-1)
    reorganized_dfs.append(value)

# We also want to create a dataframe of the first 3 columns of the spreadsheet. So subset it from the main dataframe, then flatten it and rename the columns.
column_names = []
for i in list(df.columns):
    if i[1] not in column_names and i[0].startswith("Unnamed"):
        column_names.append(i[1])

df_first_columns = df.iloc[:,:3]
df_flatten(df_first_columns)
df_first_columns.columns = column_names

# Now we want to create a new list of dataframes. These dataframes are concatenations of the first 3 columns and the 4 columns of each of the period dataframes.
dfs_to_concatenate = []
for i, value in enumerate(reorganized_dfs):
    globals()["d%s" %i] = pd.concat([df_first_columns,reorganized_dfs[i]],1)
    dfs_to_concatenate.append(globals()["d%s" %i])
df_final = pd.concat(dfs_to_concatenate,ignore_index=True)

# Now we move the date column to the beginning.  
# Then we convert it from the given format to the MMM-DD format.
df_final = df_organize(df_final,3)
df_final["date"] = pd.to_datetime(df_final["date"])
df_final["date"] = df_final["date"].apply(lambda x: x.strftime("%b-%d"))

# Finally we write the dataframe to file.
df_final.to_excel("../data/worlds census.xlsx",index=False)
