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
    while(True):
        ret, frame = opencam.read()
        frame_count += 1
        if frame_count == 25:
            output_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            break

    opencam.release()
    cv2.destroyAllWindows()
    return output_image
