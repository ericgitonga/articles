#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 07:29:23 2021

@author: Eric Gitonga
"""

import streamlit as st
import boto3
import uuid

image_file = st.sidebar.file_uploader("Upload image")

if image_file is not None:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("## Image From User")
        st.image(image_file)

    s3 = boto3.resource("s3")
    bucket = s3.Bucket("st-to-s3")
    out_file = str(uuid.uuid4().hex)
    obj = bucket.Object("images/" + out_file + ".jpg")

    obj.upload_fileobj(image_file, ExtraArgs={"ACL": "public-read"})

    s3_url = "https://st-to-s3.s3.eu-west-2.amazonaws.com/images/"
    with col2:
        st.markdown("## Image From S3")
        st.image(s3_url + out_file + ".jpg")
