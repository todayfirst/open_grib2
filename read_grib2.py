#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 19:17:23 2020

@author: ebrain
"""


import pygrib
from matplotlib import pyplot as plt
import numpy as np

lat = 35.139238
lon = 128.872537

grbs = pygrib.open('./data/l015v070erlounish000.2019070100.gb2')  
grb = grbs.read(1)[0]
grb
grbs.seek(0)

for grb in grbs:
    print(grb)
    
grb = grbs.select(name = 'Temperature')[0]

###val확인
#val = grb.data()[0]
#lat = grb.data()[1]
#lon = grb.data()[2]

data, lats, lons = grb.data(lat1=38,lat2=25,lon1=140,lon2=150)
val = grb.values
#val.shape
#val = np.transpose(val)
#val = np.rot90(val)

plt.imshow(val)
#%%
def find_i_j(grb, lat, lon):
    lats = grb.data()[1]
    lons = grb.data()[2]
    
    c_i = 0
    c_j = 0
    while(1):
        c_lat = lats[c_i][c_j]
        c_lon = lons[c_i][c_j]
        
        dis = (c_lat - lat)*(c_lat - lat) + (c_lon - lon)*(c_lon - lon)
        change = False
        for i in range(-1,2):
            if ( (c_i + i) >=lats.shape[0] or c_i + i <0):
                continue
            for j in range(-1,2):
                if (c_j + j) >= lats.shape[1] or c_j + j <0:
                    continue
                t_lat = lats[c_i + i][c_j + j]
                t_lon = lons[c_i + i][c_j + j]
                 
                t_dis = (t_lat - lat)*(t_lat - lat) + (t_lon - lon)*(t_lon - lon)
                if(dis>t_dis):
                    dis = t_dis
                    t_i = c_i + i
                    t_j = c_j + j
                    change = True

        
        if not change:

            return c_i, c_j
        c_i = t_i
        c_j = t_j

                 
        