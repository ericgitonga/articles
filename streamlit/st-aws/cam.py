#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tuesday Sep 21 04:00:00 2021

@author: gitonga
"""

import streamlit as st
import cv2


def capture_image():
    opencam = cv2.VideoCapture(0)
    if not opencam.isOpened():
        st.write("Webcam inactive")

    frame_count = 0
    while(frame_count <= 2):
        frame_count += 1
        ret, frame = opencam.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        break

    opencam.release()
    cv2.destroyAllWindows()
    return image
