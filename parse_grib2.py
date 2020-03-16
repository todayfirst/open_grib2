#!/usr/bin/env python3import osimport pygribdef search(dirname):    #try:        filenames = os.listdir(dirname)        for filename in filenames:            full_filename = os.path.join(dirname, filename)            if os.path.isdir(full_filename):                search(full_filename)            else:                ext = os.path.splitext(full_filename)[-1]                if ext == '.grib2':                                                             grbs = pygrib.open(full_filename)                                          grbs.seek(0)                                        for grb in grbs:                        print(grb)                                            grb = grbs.select(name = 'Temperature')[0]                                        ###val확인                    val = grb.data()[0]                    lat = grb.data()[1]                    lon = grb.data()[2]                                        data, lats, lons = grb.data(lat1=38,lat2=25,lon1=140,lon2=150)                    val = grb.values                    #val.shape                    #val = np.transpose(val)                    #val = np.rot90(val)                                        grbs.close()                                        print(full_filename)   # except PermissionError:    #    passsearch("/Volumes/Samsung_T5/ldaps")#%%import osimport pygribimport pandas as pdimport numpy as npimport matplotlib.pyplot as plt#pv = np.array([*range(0,136)])#pv_in = np.array([0,3,7,14,15,20,25,26,28,111,112,113,114])#pv_use = pv in pv_indirname = "/Volumes/Samsung_T5/ldaps/201907"def image_save(grbs,filename):    image_dir = os.path.join("/Users/ebrain/Desktop/grib_api-1.28.0-Source/image", filename )    if not os.path.isdir(image_dir):                os.makedirs(image_dir)        cnt = 1    for grb in grbs:        val = grb.data()[0]        lat = grb.data()[1]        lon = grb.data()[2]        val = np.transpose(val)        val = np.rot90(val)        m = val.min()        x = val.max()        val = (val-m)/(x-m)        image_path = os.path.join(image_dir, str(cnt)+'_'+grb.name + '.png')        plt.imshow(val)        plt.savefig(image_path,dpi=50 )        plt.close()        print(grb)        cnt = cnt+1                def hist_save(grbs,filename):            hist_dir = os.path.join("/Users/ebrain/Desktop/grib_api-1.28.0-Source/hist", filename )    if not os.path.isdir(hist_dir):        os.makedirs(hist_dir)    list_hist = []    for i in range(0,60):        list_hist.append(1/59*i)    cnt = 1    for grb in grbs:        val = grb.data()[0]        m = val.min()        x = val.max()        val = (val-m)/(x-m)        hist_path = os.path.join(hist_dir, str(cnt)+'_'+grb.name + '.png')        for_hist = np.ravel(val)        plt.hist(for_hist, list_hist)        plt.savefig(hist_path,dpi=50 )        plt.close()        print(grb)        cnt = cnt+1        filenames = os.listdir(dirname)for filename in filenames:        full_filename = os.path.join(dirname, filename)    if os.path.isdir(full_filename):        continue        else:        ext = os.path.splitext(full_filename)[-1]        ext2 = os.path.splitext(full_filename)[-2]        hours = int(ext2[-2:])        ext3 = ext2.split('.')[-2]        predict_hours = int(ext3[-2:])        if not (hours ==0 or hours == 6):            continue                print("predcit : %d, hours : %d" %(predict_hours, hours))        if ext == '.gb2' and ((hours == 0 and predict_hours >16) or                               (hours == 6 and predict_hours >9 and predict_hours <46 )):                                                 grbs = pygrib.open(full_filename)                        grbs.seek(0)                      #  image_save(grbs,filename)         #   hist_save(grbs, filename)            raise Exception('stop')            continue            cor_dir = "/Users/ebrain/Desktop/grib_api-1.28.0-Source/cor"             if not os.path.isdir(cor_dir):                        os.makedirs(cor_dir)            cnt = 1            for_cor =[]            for grb in grbs:                val = grb.data()[0]                #m = val.min()                #x = val.max()                #val = (val-m)/(x-m)                                val = val[grbs[13].data()[0].mask == False]                for_cor.append(np.ravel(val))                print(grb)                cnt = cnt+1                                        for_cor = np.array(for_cor)            for_cor_use = for_cor[[pv_in],:]            cor_use = np.ma.corrcoef(for_cor_use[0])            cor = np.ma.corrcoef(for_cor)            for_cor_hist = []            for i in range(len(cor)):                for j in range(i+1,len(cor)):                    ele = [i,j,cor[i,j]]                    for_cor_hist.append(ele)            for_cor_hist = np.asarray(for_cor_hist)            list_hist = []            for i in range(0,100):                list_hist.append(1/99*i)            plt.hist(abs(np.hsplit(for_cor_hist,3)[-1]),list_hist)            plt.show()            find_hist = sorted(for_cor_hist, key = lambda a : abs(a[2]))            ###val확인            val = grb.data()[0]            lat = grb.data()[1]            lon = grb.data()[2]                        data, lats, lons = grb.data(lat1=38,lat2=25,lon1=140,lon2=150)            val = grb.values            val.shape                        grbs.close()                                 print(full_filename)  