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
DataDir = '/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/Data/'

# Folder path
dir_path = CDataDir
dir_pathF = FDataDir

# lists to store files
res = []
resF = []

# Iterate directories
for path in os.listdir(dir_path):
    # check if current path is a file
    if str(path).split(".")[-1] == "tif" and os.path.isfile(os.path.join(dir_path, path)):
        res.append(path)

for path in os.listdir(dir_pathF):
    # check if current path is a file
    if str(path).split(".")[-1] == "tif" and os.path.isfile(os.path.join(dir_pathF, path)):
        resF.append(path)

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

li2 = [i for i in range(len(res))]
li3 = [i for i in range(len(resF))]

CSV = pd.DataFrame( index = li2,
                   columns = ["filename" , "Index", "Date", "NoDataValue", "Average","Event"])
CSVF = pd.DataFrame( index = li3,
                   columns = ["filename" , "Index", "Date","NoDataValue",'Average',"Event"])
for i in range (0, len(res)):
    filename = res[i]
    CSV.filename[i] = filename
    CSV.Index[i] = Index(filename, "Clipped")
    CSV.Date[i] = Date(filename, "Clipped")
    CSV.NoDataValue[i] = No_Data_Value(filename, "Clipped")
    CSV.Average[i] = Average_Index_Value(filename, "Clipped")
#here we are creating the dataframe, we need a separte function for the averaged images.
for i in range (0, len(resF)):
    filename = resF[i]
    CSVF.filename[i] = filename
    CSVF.Index[i] = Index(filename, "Full")
    CSVF.Date[i] = Date(filename, "Full")
    CSVF.NoDataValue[i] = No_Data_Value(filename, "Full")
    CSVF.Average[i] = Average_Index_Value(filename, "Full")


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


BI_Average =(CSV.Average[CSV.Index == "BI"]).tolist()
NDMI_Average =(CSV.Average[CSV.Index == "NDMI"]).tolist()
NDVI_Average =(CSV.Average[CSV.Index == "NDVI"]).tolist()
# Dates =(CSV.Date[0:12]).tolist()

Date_of_LS = Event_pointer(BI_Average, CSV)
# print(Event_pointer(NDMI_Average, CSV))
# print(Event_pointer(NDVI_Average, CSV))

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


array = Generate_post_minus_pre_images('BI')[1]
post_array = Generate_post_minus_pre_images('BI')[0]
print(array)
plt.imshow(array)
plt.show()
print(post_array)
plt.imshow(post_array)
plt.show()

pre_image_BI = array
post_image_BI = post_array

# Up to here

dBI = post_image_BI - pre_image_BI
plt.imshow(dBI)
plt.show()

x=gf.get_geoinfo(FDataDir+'/'+ 'LC08_173060_20190204_BI.tif',subdataset=0)
gf.create_geotiff(DataDir+'BI2.tif', dBI, x[0] , x[1] , x[2],x[3], x[4], x[5],compress=None)


# BI_F =(CSV.[CSV.Index == "BI"]).tolist()
# NDMI_F =(CSV[CSV.Index == "NDMI"]).tolist()
# NDVI_F =(CSV[CSV.Index == "NDVI"]).tolist()


# # PLotting
# plt.rcParams["figure.figsize"] = (20,10)
# plt.figure()
# plt.plot(Dates, BI_Average)
# plt.xlabel("Dates")
# plt.ylabel("Average BI")
# plt.savefig('/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/BI_timeseries.jpg', dpi = 600)
# plt.figure()
# plt.plot(Dates, NDMI_Average)
# plt.xlabel("Dates")
# plt.ylabel("Average NDMI")
# plt.savefig('/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/NDMI_timeseries.jpg', dpi = 600)
# plt.figure()
# plt.plot(Dates, NDVI_Average)
# plt.xlabel("Dates")
# plt.ylabel("Average NDVI")
# plt.savefig('/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/NDVI_timeseries.jpg', dpi = 600)
#
# #Exporting
# CSV.to_excel("/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/TimeSeriesC.xlsx")
# CSVF.to_excel("/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/TimeSeriesF.xlsx")

