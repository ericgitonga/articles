#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 07:29:23 2021

@author: Eric Gitonga
"""

import streamlit as st
import streamlit_analytics
import boto3
import uuid
from cam import capture_image
import io
from PIL import Image
import imghdr

with streamlit_analytics.track():
    image_file = st.sidebar.file_uploader("Upload image")


    if st.sidebar.button("Capture webcam image"):
        read_image = capture_image()
        buffer_image = io.BytesIO()
        Image.fromarray(read_image).save(buffer_image, format="JPEG")
        image_file = io.BytesIO(buffer_image.getvalue())

    if image_file is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("## Image From User")
            st.image(image_file)

        s3 = boto3.resource("s3")
        bucket = s3.Bucket("eric-gitonga-articles")
        out_file = str(uuid.uuid4().hex) + "." + imghdr.what(image_file)
        obj = bucket.Object("images/" + out_file)
        obj.upload_fileobj(image_file, ExtraArgs={"ACL": "public-read"})

        s3_url = "https://eric-gitonga-articles.s3.eu-west-2.amazonaws.com/images/"
        with col2:
            st.markdown("## Image From S3")
            st.image(s3_url + out_file)
