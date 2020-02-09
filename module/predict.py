#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 22:22:33 2020

@author: matsumuratomiakira
"""

import numpy as np
from tensorflow.keras.models import load_model
import cv2
import os

#load image as rgb scale
def crop_resize(image_path):
    image = cv2.imread(image_path, 1)
    image = cv2.resize(image, (32, 32))
    img = np.array(image).astype("float32")
    img /= 255
    return img

#predict image
def predict_corn(image_path):
    image = [crop_resize(image_path)]
    image = np.asarray(image)
    
    model_path = os.getcwd() + "/corn_model_file.hdf5"
    #load model
    model = load_model(model_path)
    image_shape = (32, 32, 3)
    
    predicted = model.predict_classes(image)
    if predicted == 0:
        w  = "コーンフレークやな。"
    if predicted == 1:
        w = "トラやな。"
    if predicted == 2:
        w = "ほなコーンフレークとちゃうか〜"

    return w
