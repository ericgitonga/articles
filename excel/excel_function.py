#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import tkinter as tk
from tkinter import filedialog as fd

def df_flatten(df):
    df = pd.DataFrame(df.to_records())
    df.drop("index",axis="columns",inplace=True)
    return df

def df_organize(df,index):
    date = df[list(df.columns)[index]]
    df = df.drop(['date'],axis=1)
    df.insert(0,'date',date)    
    return df

def prepare_excel():
    root = tk.Tk()
    file = fd.askopenfile()
    root.destroy()

    df = pd.read_excel(file.name, header=[0,1])
    
    dates = []
    for i in list(df.columns):
        if i[0] not in dates and not i[0].startswith("Unnamed"):
            dates.append(i[0])
    
    extracted_dfs = []
    for i, val in enumerate(dates):
        globals()["df%s" %i] = df[[val]]
        extracted_dfs.append(globals()["df%s" %i])
    
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
        
    column_names = []
    for i in list(df.columns):
        if i[1] not in column_names and i[0].startswith("Unnamed"):
            column_names.append(i[1])

    df_first_columns = df.iloc[:,:3]
    df_flatten(df_first_columns)
    df_first_columns.columns = column_names
    
    dfs_to_concatenate = []
    for i, value in enumerate(reorganized_dfs):
        globals()["d%s" %i] = pd.concat([df_first_columns,reorganized_dfs[i]],1)
        dfs_to_concatenate.append(globals()["d%s" %i])
    df_final = pd.concat(dfs_to_concatenate,ignore_index=True)
    
    df_final = df_organize(df_final,3)
    df_final["date"] = pd.to_datetime(df_final["date"])
    df_final["date"] = df_final["date"].apply(lambda x: x.strftime("%b-%d"))
    
    return df_final