#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 07:29:23 2021

@author: Eric Gitonga
"""

import streamlit as st
import s3fs

fs = s3fs.S3FileSystem(anon=False)


@st.cache(ttl=600)
def read_file(filename):
    with fs.open(filename) as f:
        return f.read().decode("utf-8")


# content = read_file("eric-gitonga-articles/text/test.csv")
content = read_file("st-to-s3/text/test.csv")

# Print results.
for line in content.strip().split("\n"):
    name, pet = line.split(",")
    st.write(f"{name} has a :{pet}:")
