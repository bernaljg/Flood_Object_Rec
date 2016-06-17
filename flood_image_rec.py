"""
Created by: Bernal Jimenez
6/17/2016

Script uses tensorflow to recognize objects in photographs using ImageNet
"""

import classify_image
import glob

image_dict = {}
for filename in glob.glob('images/*'):
    run_inference(filename)


def run_inference(filename):



