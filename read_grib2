#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 19:17:23 2020

@author: ebrain
"""


import pygrib
from matplotlib import pyplot as plt
import numpy as np

grbs = pygrib.open('./data/l015v070erlounish000.2019070100.gb2')  
grb = grbs.read(1)[0]
grb
grbs.seek(0)

for grb in grbs:
    print(grb)
    
grb = grbs.select(name = 'Temperature')[0]
val = grb.values
val.shape
val = np.transpose(val)
val = np.rot90(val)

plt.imshow(val)
