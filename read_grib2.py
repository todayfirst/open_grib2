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

###val확인
val = grb.data()[0]
lat = grb.data()[1]
lon = grb.data()[2]

data, lats, lons = grb.data(lat1=38,lat2=25,lon1=140,lon2=150)
val = grb.values
#val.shape
#val = np.transpose(val)
#val = np.rot90(val)

plt.imshow(val)


