#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import tkinter as tk
from tkinter import filedialog as fd

def prepare_excel():
    root = tk.Tk()
    file = fd.askopenfile()
    root.destroy()

    if file:
        sheetname = input("Please enter the sheet name to use: ")
        df = pd.read_excel(file.name, sheet_name = sheetname, header=[0, 1])
        column_labels = []
        for label in df.columns:
            if label[0] not in column_labels:
                column_labels.append(label[0])

        df_to_concatenate = []
        for date in column_labels[1:]:
            df_temp = pd.concat([df[column_labels[0]], df[date]], axis="columns")
            df_temp.insert(0, "Date", date)
            df_to_concatenate.append(df_temp)

        df_concatenated = pd.concat(df_to_concatenate, ignore_index=True)

        df_concatenated["Date"] = pd.to_datetime(df_concatenated["Date"])
        df_concatenated["Date"] = df_concatenated["Date"].apply(lambda x: x.strftime("%b-%d"))

        return df_concatenated

def save_file():
    root = tk.Tk()
    file = fd.asksaveasfile(mode='w', initialfile = 'Untitled.csv',
                            defaultextension=".csv", filetypes=[("CSV", "*.csv")])
    root.destroy()

    if file:
        df.to_csv(file, index=False)
        file.close()

df = prepare_excel()
save_file()