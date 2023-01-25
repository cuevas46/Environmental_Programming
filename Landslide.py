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
# resF = list()

# Iterate directories
for item in os.listdir(dir_path):
    # Accessing item by adding directory path and checking if current item is a file
    if os.path.isfile(os.path.join(dir_path, item)):
        res.append(item)
# print(res)

# for item in os.listdir(dir_pathF):
#     # Accessing item by adding directory path and checking if current item is a file
#     if os.path.isfile(os.path.join(dir_pathF, item)):
#         resF.append(item)

def Index( filename , datatype ): #You have to select wether the file is clipped or full
    if datatype == "Clipped":
        index = filename.split("_")[1] #Index is wether is NDMI, BI or NDVI
    else:
        index = filename.split("_")[3].split(".")[0] #Index is wether is NDMI, BI or NDVI and here we take the figure format out
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
# li3 = [i for i in range(len(resF))]

CSV = pd.DataFrame( index = li2,
                   columns = ["filename" , "Index", "Date", "NoDataValue", "Average","Event"])
for i in range (0, len(res)):
    filename = res[i]
    CSV.filename[i] = filename
    CSV.Index[i] = Index(filename, "Clipped")
    CSV.Date[i] = Date(filename, "Clipped")
    CSV.NoDataValue[i] = No_Data_Value(filename, "Clipped")
    CSV.Average[i] = Average_Index_Value(filename, "Clipped")

# CSV.sort_values("Date")
# print(CSV)

def Event_pointer(Listname):
    Derivative = list() #We create here the list where all the derivatives will be stored
    for i in range (0,(len(Listname) - 1)):
        Mean_Distance = abs(Listname[i+1] - Listname[i])
        Derivative.append(Mean_Distance)
    index_in_list = max(Derivative)
    Event = Derivative.index(index_in_list) +1
    Event_Average = Listname[Event]
    Date_of_Event = CSV.Date[CSV.Average == Event_Average]
    return Date_of_Event

BI_Average =(CSV.Average[CSV.Index == "BI"]).tolist()
NDMI_Average =(CSV.Average[CSV.Index == "NDMI"]).tolist()
NDVI_Average =(CSV.Average[CSV.Index == "NDVI"]).tolist()
Dates =(CSV.Date[0:12]).tolist()

print(Event_pointer(BI_Average))
print(Event_pointer(NDVI_Average))
print(Event_pointer(NDMI_Average))

# PLotting
plt.rcParams["figure.figsize"] = (20,10)
plt.figure()
plt.plot(Dates, BI_Average)
plt.xlabel("Dates")
plt.ylabel("Average BI")
plt.savefig('/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/BI_timeseries.jpg', dpi = 600)
plt.figure()
plt.plot(Dates, NDMI_Average)
plt.xlabel("Dates")
plt.ylabel("Average NDMI")
plt.savefig('/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/NDMI_timeseries.jpg', dpi = 600)
plt.figure()
plt.plot(Dates, NDVI_Average)
plt.xlabel("Dates")
plt.ylabel("Average NDVI")
plt.savefig('/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/NDVI_timeseries.jpg', dpi = 600)

#Exporting
CSV.to_excel("/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/TimeSeries.xlsx")