import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
import sys
import os
import GIS_functions as gf
import datetime

##Functions

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
        mean = np.nanmean(array)
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

def Event_pointer(Listname, df):
    Derivative = list() #We create here the list where all the derivatives will be stored
    for i in range (0,(len(Listname) - 1)):
        Mean_Distance = abs(Listname[i+1] - Listname[i])
        Derivative.append(Mean_Distance)
    index_in_list = max(Derivative)
    Event = Derivative.index(index_in_list)+1
    Event_Average = Listname[Event]
    #Date_of_Event = CSV.Date[CSV.Average == Event_Average]
    Index = df[df['Average'] == Event_Average].index.values
    df.loc[Index, 'Event'] = 'LS'
    Date_of_Event = df['Date'].values[Index]
    CSVF.loc[CSVF['Date'] == df['Date'].loc[df.index[Index[0]]], 'Event'] = 'LS'
    return Date_of_Event

def Generate_post_minus_pre_images(filetype):
    df = pd.DataFrame(columns = ["filename", "Date","Event"])
    df.filename = CSVF.filename[CSVF.Index == filetype]
    df.Date = CSVF.Date[CSVF.Index == filetype]
    df.Event = CSVF.Event[CSVF.Index == filetype]
    df.reset_index(inplace = True)
    Index = df[df['Event'] == 'LS'].index.values
    i=0
    j=Index[0]
    if i < Index[0]:
        ds = gdal.Open(FDataDir+'/'+df.filename[i])
        band = ds.GetRasterBand(1)
        array = band.ReadAsArray()
        array[np.isnan(array)] = 0,
        array += array
        i += 1
    array = array/i
    k=0
    if j <= len(df):
        ds2 = gdal.Open(FDataDir + '/' + df.filename[j])
        band2 = ds2.GetRasterBand(1)
        post_array = band2.ReadAsArray()
        post_array[np.isnan(post_array)] = 0,
        post_array += post_array
        j += 1
        k += 1
    post_array = post_array/k
    return post_array, array


#Reading of images
CDataDir = '/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/Data/Clipped_images'
FDataDir = '/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/Data/Full_image'
DataDir = '/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/Data/'

clipped_images = []
full_images = []

for path in os.listdir(CDataDir):
    # check if current path is a file
    if str(path).split(".")[-1] == "tif" and os.path.isfile(os.path.join(CDataDir, path)):
        clipped_images.append(path)

for path in os.listdir(FDataDir):
    # check if current path is a file
    if str(path).split(".")[-1] == "tif" and os.path.isfile(os.path.join(FDataDir, path)):
        full_images.append(path)

li2 = [i for i in range(len(clipped_images))]
li3 = [i for i in range(len(full_images))]

CSV = pd.DataFrame( index = li2,
                   columns = ["filename" , "Index", "Date", "NoDataValue", "Average","Event"])
CSVF = pd.DataFrame( index = li3,
                   columns = ["filename" , "Index", "Date","Event"])

for i in range (0, len(clipped_images)):
    filename = clipped_images[i]
    CSV.filename[i] = filename
    CSV.Index[i] = Index(filename, "Clipped")
    CSV.Date[i] = Date(filename, "Clipped")
    CSV.NoDataValue[i] = No_Data_Value(filename, "Clipped")
    CSV.Average[i] = Average_Index_Value(filename, "Clipped")
for i in range (0, len(full_images)):
    filename = full_images[i]
    CSVF.filename[i] = filename
    CSVF.Index[i] = Index(filename, "Full")
    CSVF.Date[i] = Date(filename, "Full")

BI_Average =(CSV.Average[CSV.Index == "BI"]).tolist()
NDMI_Average =(CSV.Average[CSV.Index == "NDMI"]).tolist()
NDVI_Average =(CSV.Average[CSV.Index == "NDVI"]).tolist()
Dates =(CSV.Date[0:12]).tolist()

if Event_pointer(BI_Average, CSV)[0] == Event_pointer(NDMI_Average, CSV) == Event_pointer(NDVI_Average, CSV):
    Date_of_LS = Event_pointer(BI_Average, CSV)[0]

pre_array_BI = Generate_post_minus_pre_images('BI')[1]
post_array_BI = Generate_post_minus_pre_images('BI')[0]
pre_array_NDMI = Generate_post_minus_pre_images('NDMI')[1]
post_array_NDMI = Generate_post_minus_pre_images('NDMI')[0]
pre_array_NDVI = Generate_post_minus_pre_images('NDVI')[1]
post_array_NDVI = Generate_post_minus_pre_images('NDVI')[0]

dBI = post_array_BI - pre_array_BI
dNDMI = post_array_NDMI - pre_array_NDMI
dNDVI = post_array_NDMI - pre_array_NDVI

x=gf.get_geoinfo(FDataDir+'/'+ 'LC08_173060_20190204_BI.tif',subdataset=0)
gf.create_geotiff(DataDir+'BI.tif', dBI, x[0] , x[1] , x[2],x[3], x[4], x[5],compress=None)
gf.create_geotiff(DataDir+'NDMI.tif', dNDMI, x[0] , x[1] , x[2],x[3], x[4], x[5],compress=None)
gf.create_geotiff(DataDir+'NDVI.tif', dNDVI, x[0] , x[1] , x[2],x[3], x[4], x[5],compress=None)

# PLotting
plt.rcParams["figure.figsize"] = (20,10)
plt.figure()
plt.plot(Dates, BI_Average/max(BI_Average),label = 'BI', color = 'green')
plt.plot(Dates, NDMI_Average,label = 'NDMI', color = 'blue')
plt.plot(Dates, NDVI_Average,label = 'NDVI', color = 'black')
plt.legend(prop={'size': 20})
plt.xlabel("Dates", fontsize=20)
plt.ylabel("Arbitrary Units", fontsize=20)
plt.axvline(x = Date_of_LS, color = 'r', label = 'axvline - full height')
plt.savefig(DataDir + 'BI_timeseries.jpg', dpi = 600)
plt.show()

# #Exporting
CSV.to_excel(DataDir + 'TimeSeriesC.xlsx')
