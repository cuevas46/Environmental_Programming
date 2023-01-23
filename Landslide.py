import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
import sys
import os
import GIS_functions as gf
import datetime

CDataDir = '/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/Data/Clipped_images'
FDataDir = '/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/Data/Full_image'

##Listing Filenames

# folder path
dir_path = CDataDir

# list to store files
res = list()

# Iterate directory
for item in os.listdir(dir_path):
    # Accessing item by adding directory path and checking if current item is a file
    if os.path.isfile(os.path.join(dir_path, item)):
        res.append(item)

# print(res)

#Sorting independent picture into lists
BI = list()
NDMI = list()
NDVI = list()
BI_Date = list()
NDMI_Date = list()
NDVI_Date = list()
for i in range (0, len(res)):
    temp_list = res[i].split('_')
    if temp_list[1] == 'BI':
        BI.append(res[i])
        BI_Date.append((temp_list[2].split("."))[0]) #Here you split and take index 0, which is the date.
        #This is the same thing that was done for the temp_list, but just in one line
    elif temp_list[1] == 'NDMI':
        NDMI.append(res[i])
        NDMI_Date.append(temp_list[2].split(".")[0])
    elif temp_list[1] == 'NDVI':
        NDVI.append(res[i])
        NDVI_Date.append(temp_list[2].split(".")[0])
# print(BI_Date)
# print(NDMI_Date)
# print(NDVI_Date)

#BI is the list with all the Bi files
#This can be transform into a function
avg_bi = list()
for i in range (0,len(BI)):
    ds = gdal.Open(CDataDir+'/'+BI[i]) #We are openning all the Bi files in the directory
    band = ds.GetRasterBand(1) #to access the information store in our data set
    no_data = band.GetNoDataValue()
    array = band.ReadAsArray() #We will read the band object into this array
    # plt.imshow(array)
    # plt.show()
    #print(array[array>no_data])
    mean_bi = np.mean(array[array > no_data])
    avg_bi.append(mean_bi)
print(avg_bi)

avg_ndmi = list()
for i in range (0,len(NDMI)):
    ds1 = gdal.Open(CDataDir+'/'+NDMI[i])
    band1 = ds1.GetRasterBand(1)
    no_data1 = band1.GetNoDataValue()
    array1 = band1.ReadAsArray()
    mean_ndmi = np.mean(array1[array1 > no_data])
    avg_ndmi.append(mean_ndmi)

# print(avg_ndmi)

avg_ndvi = list()
for i in range (0,len(NDVI)):
    ds = gdal.Open(CDataDir+'/'+NDVI[i])
    band = ds.GetRasterBand(1)
    no_data = band.GetNoDataValue()
    array = band.ReadAsArray()
    mean_ndvi = np.mean(array[array > no_data])
    avg_ndvi.append(mean_ndvi)

# print(avg_ndvi)
#
dates = BI_Date
dates
Day =list()
Month =list()
Year =list()
for i in range (0, (len(dates))):
    Year.append(dates[i][0:4])
    Month.append(dates[i][4:6])
    Day.append(dates[i][6:8])

date_form = list()
for i in range (0,len(dates)):
    date = str(datetime.date(int(Year[i]),int(Month[i]),int(Day[i])))
    date_form.append(date)

print(date_form)
# plt.imshow(array)
# plt.show()
plt.plot(date_form, avg_bi)
plt.show()

#Point 6 onwards
full_images = gf.list_files_in_folder(FDataDir, extension='tif')
