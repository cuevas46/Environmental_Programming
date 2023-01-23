import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
from osgeo import gdal
import sys
import os
sys.path.append('/Users/alismac/Documents/Environmental_Programming/Project/A3_Landslide_detection')
import GIS_functions as gf
import datetime

CDataDir = '/Users/alismac/Documents/Environmental_Programming/Project/A3_Landslide_detection/Data/Clipped_images'
FDataDir = '/Users/alismac/Documents/Environmental_Programming/Project/A3_Landslide_detection/Data/Full_image'

# folder path
dir_path = CDataDir

# list to store files
res = []

# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        res.append(path)

print(res)

BI = list()
NDMI = list()
NDVI = list()
BI_Date = list()
NDMI_Date =list()
NDVI_Date = list()
for i in range (0, len(res)):
    temp_list = res[i].split('_')
    if temp_list[1] == 'BI':
        BI.append(res[i])
        BI_Date.append((temp_list[2].split("."))[0])
    elif temp_list[1] == 'NDMI':
        NDMI.append(res[i])
        NDMI_Date.append(temp_list[2].split(".")[0])
    elif temp_list[1] == 'NDVI':
        NDVI.append(res[i])
        NDVI_Date.append(temp_list[2].split(".")[0])
print(NDMI_Date)
print(BI_Date)
print(NDVI_Date)

year =
month

avg_bi = list()
for i in range (0,len(BI)):
    ds = gdal.Open(CDataDir+'/'+BI[i])
    band = ds.GetRasterBand(1)
    no_data = band.GetNoDataValue()
    array = band.ReadAsArray()
    mean = np.mean(array[array > no_data])
    avg_bi.append(mean)

print(avg_bi)

avg_ndmi = list()
for i in range (0,len(NDMI)):
    ds1 = gdal.Open(CDataDir+'/'+NDMI[i])
    band1 = ds1.GetRasterBand(1)
    no_data1 = band1.GetNoDataValue()
    array1 = band1.ReadAsArray()
    mean1 = np.mean(array1[array1 > no_data])
    avg_ndmi.append(mean1)

print(avg_ndmi)

avg_ndvi = list()
for i in range (0,len(NDVI)):
    ds = gdal.Open(CDataDir+'/'+NDVI[i])
    band = ds.GetRasterBand(1)
    no_data = band.GetNoDataValue()
    array = band.ReadAsArray()
    mean = np.mean(array[array > no_data])
    avg_ndvi.append(mean)

print(avg_ndvi)

dates = BI_Date + NDMI_Date + NDVI_Date
dates
Day =list()
Month =list()
Year =list()
for i in range (0, (len(dates)-1)):
    Year.append(dates[i][0:4])
    Month.append(dates[i][4:6])
    Day.append(dates[i][6:8])

date_form = list()
for i in range (0,len(dates)-1):
    date = str(datetime.date(int(Year[i]),int(Month[i]),int(Day[i])))
    date_form.append(date)

date_form

pd.dataframe