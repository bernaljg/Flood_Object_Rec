"""
Created by: Bernal Jimenez
6/17/2016

Script uses tensorflow to recognize specific objects in photographs using ImageNet
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path
import re
import sys
import tarfile
import glob
import pickle
from PIL import Image

import numpy as np
from six.moves import urllib
import classify_image as ci
import tensorflow as tf

def run_inference():
    """Runs inference function defined in the tensorflow imagenet to find objects in flooding images folder images/"""
    label_dict = {}
    
    for filename in glob.glob('images/*'):
        image = Image.open(filename)
        array_image = np.array(image)
        objects = find_objects(array_image,3)
        for obj in objects:
            if obj in label_dict:
                label_dict[obj].append(filename[7:])
            else:
                label_dict[obj] = [filename[7:]]
                    
    pickle.dump(label_dict, open("labels.p","wb"))

def find_objects(image,num_crops):
    """Function that does finer grained object recognition by cropping the image into several sections"""
    r_step, c_step = image.shape[0]//num_crops, image.shape[1]//num_crops
    object_list = []
    for i in range(num_crops):
        for j in range(num_crops):
            tf.reset_default_graph()
            cropped_image = image[i*r_step:(i+1)*r_step,j*c_step:(j+1)*c_step,:]
            inf_list = ci.run_inference_on_image(cropped_image)
            if inf_list != []:
                object_list.extend(inf_list)
    return object_list

run_inference()
