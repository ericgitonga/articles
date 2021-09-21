#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tuesday Sep 21 04:00:00 2021

@author: gitonga
"""

import streamlit as st
import cv2

st.title("Capture image using webcam")

opencam = cv2.VideoCapture(0)
if not opencam.isOpened():
    print("Webcam inactive")

frame_count = 0
while(True):
    ret, frame = opencam.read()
    frame_count += 1
#    print(frame_count)
    if frame_count == 10:
        output_image = frame
        break
#    cv2.imshow("preview", frame)
#    if cv2.waitKey(1) & 0xFF == ord("q"):
#        break

opencam.release()
cv2.destroyAllWindows()

st.image(output_image)