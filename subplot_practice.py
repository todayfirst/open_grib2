# -*- coding: utf-8 -*-

#35.139238, 128.872537
import math as mt
import os
import pygrib
from matplotlib import pyplot as plt
import pvlib
import pandas as pd
import datetime as dt
from datetime import datetime
import numpy as np
DF = pd.DataFrame(columns = ("date","hour"))
lat = 35.139238
lon = 128.872537

startdate = "20190701"
enddate = "20190731"
starthour = 5
endhour = 19

during = endhour - starthour + 1

for i, date in enumerate(pd.date_range(startdate, enddate)):
    
   # print(date.strftime('%Y-%m-%d'))
    
    for j in range(during):
        
        DF = DF.append(pd.DataFrame([[date.strftime("%Y%m%d"), j+starthour]], columns = ['date', 'hour']), ignore_index = True)
#DF["hour"][i*during + j] = j+starthour
#df = df.append(pd.DataFrame([[idx, number]], columns=['idx', 'number']), ignore_index=True)

pv = pd.read_csv("./pv_data_busan.csv")
pv = pv[pv["tgt_time"]<20]
pv =  pv[pv["tgt_time"]>4]
pv = pv[pv["tgt_date"]>=20190701]
pv = pv[pv["tgt_date"]<=20190731]
pv.reset_index(inplace = True, drop = True)

DF["pv"] = np.empty(len(DF))
DF["pv"][:] = np.nan

for i in (range(len(DF))):
    try:
        date = int(DF.iloc[i]["date"])
        time = int(DF.iloc[i]["hour"])
        pv_1 = pv[(pv["tgt_time"] == time) & (pv["tgt_date"] == date)]
        DF["pv"][i] = pv_1["mesrg_elect_qnt"]
    except Exception as ex:
        print(ex)
#%%
dirname = "/Volumes/Samsung_T5/ldaps/201907"
#%% plot_line
def dot(a0,a1,a2,b0,b1,b2):
    return a0*b0+b1*a1+a2*b2

def sun_pan(s_a,s_e,p_a,p_e):
    a = [np.cos(np.radians(s_e))*np.cos(np.radians(s_a)), np.cos(np.radians(s_e))*np.sin(np.radians(s_a)) ,np.sin(np.radians(s_e))]
    b = [np.cos(np.radians(p_e))*np.cos(np.radians(p_a)), np.cos(np.radians(p_e))*np.sin(np.radians(p_a)) ,np.sin(np.radians(p_e))]
    return dot(a[0], a[1],a[2],b[0],b[1],b[2])    

p_a = 180
p_e = 45
grid_for_hours = {}
for i in range(5,20):
    grid_for_hours[i] = []
    for date in (pd.date_range(startdate, enddate)):
        dt1 = dt.timedelta(hours=8.5)
   
        grid_for_hours[i].append(pd.DatetimeIndex([date.strftime("%Y-%m-%d ")+str(i).zfill(2)])[0] - dt1)

grid_for_day = {}
for date in (pd.date_range(startdate, enddate)):
    i = int(date.strftime("%d"))
    grid_for_day[i] = []
    for j in range(5,20):
        dt1 = dt.timedelta(hours=8.5)
        grid_for_day[i].append(pd.DatetimeIndex([date.strftime("%Y-%m-%d ")+str(j).zfill(2)])[0] - dt1)
    
grid_for_hours_val = {}
for i in range(5,20):
    
    azimuth = pvlib.solarposition.get_solarposition(grid_for_hours[i], lat, lon)["azimuth"]
    azimuth = np.array(azimuth)
    elevation =  pvlib.solarposition.get_solarposition(grid_for_hours[i], lat, lon)["elevation"]
    elevation = np.array(elevation)
    grid_for_hours_val[i] = sun_pan(azimuth, elevation, p_a,p_e)
    grid_for_hours_val[i] = np.power(grid_for_hours_val[i], 1)
    #grid_for_hours_val[i] = np.sin(np.radians(elevation))+(np.cos(np.radians(elevation)) * np.cos(np.radians(azimuth)))

grid_for_day_val = {}
for date in (pd.date_range(startdate, enddate)):
    i = int(date.strftime("%d"))
    azimuth = pvlib.solarposition.get_solarposition(grid_for_day[i], lat, lon)["azimuth"]
    azimuth = np.array(azimuth)
    elevation =  pvlib.solarposition.get_solarposition(grid_for_day[i], lat, lon)["elevation"]
    elevation = np.array(elevation)
    grid_for_day_val[i] = sun_pan(azimuth, elevation, p_a,p_e)
    #grid_for_day_val[i] = np.sin(np.radians(elevation))+(np.cos(np.radians(elevation)) * np.cos(np.radians(azimuth)))
    grid_for_day_val[i]  = np.power(grid_for_day_val[i],1)
    
#%% 
for date in (pd.date_range(startdate, enddate)):
    fig = plt.figure(constrained_layout = True, figsize=(12,12))
    
    gs = fig.add_gridspec(8,8)
    ax1 = fig.add_subplot(gs[0:2,0:5])
    ax1_1 = ax1.twinx()
    
    for hour in range(5,20):
        a = []
        for i in grid_for_hours[hour]:
            a.append(hour)
        a = np.array(a)
        ax1.plot(a,grid_for_hours_val[hour],color = 'grey',linewidth =1)
    cnt = 0
    for date in (pd.date_range(startdate, enddate)):
        cnt = cnt+1
        if not cnt%10 == 1:
        
            continue
        
        a = []
        hour = 5
        
        for i in grid_for_day[1]:
            a.append(hour)
            hour = hour + 1
        a = np.array(a)
        ax1.plot(a,grid_for_day_val[int(date.strftime("%d"))],color = 'grey',linewidth =10)
       
    
    ax1.set_ylim(0,0.9)
    
    
    
    date = date.strftime("%Y%m%d")
    temp = DF[DF["date"] ==date]["pv"]
    ax1_1.plot(a, temp)
    ax1_1.set_ylim(0,600)
    
    
    ax2 = fig.add_subplot(gs[0:4,5:])
    
    
    ax3 = fig.add_subplot(gs[2:4,0:5])
    ax3.axix('off')
    ax4 = fig.add_subplot(gs[4:7,0:3],aspect = 'equal')
    ax4.axis('off')
    ax5 = fig.add_subplot(gs[4,3],aspect = 'equal')
    ax5.axis('off')
    ax6 = fig.add_subplot(gs[4:7,4:7],aspect = 'equal')
    ax6.axis('off')
    ax7 = fig.add_subplot(gs[4,7],aspect = 'equal')
    ax7.axis('off')
    
    plt.show()
    del fig

#%%
time_index = pd.date_range(startdate, enddate)
pvlib.solarposition

ax1 = plt.subplot(311)
ax2 = plt.subplot(323)
ax3 = plt.subplot(324)
ax4 = plt.subplot(325)
ax5 = plt.subplot(326)

'''
------------------------------------------
|                                         |
|                                         |
|                                         |
|                                         |
------------------------------------------

-------------------  ---------------------
|                  | |                    |
|                  | |                    |
|                  | |                    |
|                  | |                    |
-------------------  ---------------------

-------------------  ---------------------
|                  | |                    |
|                  | |                    |
|                  | |                    |
|                  | |                    |
-------------------  ---------------------

'''


#%%
fig = plt.figure(constrained_layout = True, figsize=(8,8))

gs = fig.add_gridspec(8,8)
ax1 = fig.add_subplot(gs[0:2,0:5])


ax2 = fig.add_subplot(gs[0:4,5:])
ax3 = fig.add_subplot(gs[2:4,0:5])
ax4 = fig.add_subplot(gs[4:7,0:3],aspect = 'equal')

ax5 = fig.add_subplot(gs[4,3],aspect = 'equal')

ax6 = fig.add_subplot(gs[4:7,4:7],aspect = 'equal')

ax7 = fig.add_subplot(gs[4,7],aspect = 'equal')


x = [1,2,3,4,5]
y1 = [1,2,3,2,1]
y2 = [20,20,20,20,20]

ax1.plot(x,y1, color = 'r',linewidth = 10, zorder = 1)
ax1_1 = ax1.twinx()
ax1_1.plot(x,y2,color = 'grey',linewidth = 10, zorder = -1)
ax1.set_zorder(1)
ax1_1.set_zorder(-1)
ax1.patch.set_visible(False)
plt.show()

