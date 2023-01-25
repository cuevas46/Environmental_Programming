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

#Listing Filenames

# folder path
dir_path = CDataDir
dir_pathF = FDataDir

# lists to store files
res = list()
resF = list()

# Iterate directories
for item in os.listdir(dir_path):
    # Accessing item by adding directory path and checking if current item is a file
    if os.path.isfile(os.path.join(dir_path, item)):
        res.append(item)
for item in os.listdir(dir_pathF):
    # Accessing item by adding directory path and checking if current item is a file
    if os.path.isfile(os.path.join(dir_pathF, item)):
        resF.append(item)

def Index( filename , datatype ):
    if datatype == "Clipped":
        index = filename.split("_")[1]
    else:
        index = filename.split("_")[3].split(".")[0]
    return index

def Date(filename, datatype ):
    if datatype == "Clipped":
        Day = filename.split(".")[0][-2:]
        Month = filename.split(".")[0][-4:-2]
        Year = filename.split(".")[0][-8:-4]
    else:
        Day = filename.split("_")[2][-2:]
        Month = filename.split("_")[2][-4:-2]
        Year = filename.split("_")[2][0:4]
    date = str(datetime.date(int(Year),int(Month),int(Day)))
    return date

def Average_Index_Value(filename, datatype):
    if datatype == "Clipped":
        ds = gdal.Open(CDataDir+'/'+filename)
        band = ds.GetRasterBand(1)
        no_data = band.GetNoDataValue()
        array = band.ReadAsArray()
        mean = np.mean(array[array > no_data])
    else:
        ds = gdal.Open(FDataDir+'/'+filename)
        band = ds.GetRasterBand(1)
        no_data = band.GetNoDataValue()
        array = band.ReadAsArray()
        mean = np.mean(array[array != no_data])
    return mean

def No_Data_Value(filename, datatype):
    if datatype == "Clipped":
        ds = gdal.Open(CDataDir+'/'+filename)
        band = ds.GetRasterBand(1)
        no_data = band.GetNoDataValue()
    else:
        ds = gdal.Open(FDataDir+'/'+filename)
        band = ds.GetRasterBand(1)
        no_data = band.GetNoDataValue()
    return no_data

li2 = [i for i in range(len(res))]
li3 = [i for i in range(len(resF))]

CSV = pd.DataFrame( index = li2,
                   columns = ["filename" , "Index", "Date", "NoDataValue", "Average","Event"])
for i in range (0, len(res)-1):
    filename = res[i]
    CSV.filename[i] = filename
    CSV.Index[i] = Index(filename, "Clipped")
    CSV.Date[i] = Date(filename, "Clipped")
    CSV.Average[i] = Average_Index_Value(filename, "Clipped")
    CSV.NoDataValue[i] = No_Data_Value(filename,"Clipped")

CSV.sort_values("Date")
print(CSV)