#!/usr/bin/env python
# coding: utf-8

#from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

prediction_label = {0: "Healthy", 1: "Red Spider Mite", 2: "Rust"}

def make_prediction(file_path, model):
    image = load_img(file_path, target_size=(224, 224))
    x = img_to_array(image)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    pred_classes = model.predict(images, batch_size=10)
    classes = pred_classes.argmax(axis=-1)
    return prediction_label.get(classes[0], 'Not sure.')

