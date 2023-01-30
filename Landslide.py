import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
from osgeo import gdal
import sys
import os
#### We did not use the GIS_functions!
#sys.path.append('/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection')
#import GIS_functions as gf
import datetime
'''
For more information about this code, visit: 
https://docs.google.com/document/d/1to7S2V4dlP5mlKjHOEfCVJyhnO_VQ9gxlhlQTnUQncI/edit?usp=sharing

'''
"""CDataDir = '/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/Data/Clipped_images'
FDataDir = '/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/Data/Full_images'
SaveOutput = '/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/Data/Ali'
"""
CDataDir = str(input("please provide the path to clipped image data:"))
FDataDir = str(input("please provide the path to Full image data:"))
SaveOutput = str(input("please provide desired output path:"))

# folder path
dir_path = CDataDir
dir_pathF = FDataDir

# list to store files
res = []
resF = []

for path in os.listdir(dir_path):
    # checking Tiff files
    if str(path).split(".")[-1] == "tif" and os.path.isfile(os.path.join(dir_path, path)):
        res.append(path)

for path in os.listdir(dir_pathF):
    # checking Tiff files
    if str(path).split(".")[-1] == "tif" and os.path.isfile(os.path.join(dir_pathF, path)):
        resF.append(path)


def Index(filename, datatype):
    if datatype == "Clipped":
        index = filename.split("_")[1]
    elif datatype == "Full":
        index_split = filename.split("_")[3]
        index = index_split.split(".")[0]
    return index

"""The function derives the index name out of the file name 
filename : str
datarype: str Full or Clipped
"""

def Date(filename, datatype):
    if datatype == "Clipped":
        Day = filename.split(".")[0][-2:]
        Month = filename.split(".")[0][-4:-2]
        Year = filename.split(".")[0][-8:-4]
    else:
        Day = filename.split("_")[2][-2:]
        Month = filename.split("_")[2][-4:-2]
        Year = filename.split("_")[2][0:4]
    date = str(datetime.date(int(Year), int(Month), int(Day)))
    return date
"""The function derives the date out of the file name 
filename : str
datarype: str Full or Clipped
"""

def Average_Index_Value(filename, datatype):
    if datatype == "Clipped":
        ds = gdal.Open(CDataDir + '/' + filename)
        band = ds.GetRasterBand(1)
        no_data = band.GetNoDataValue()
        array = band.ReadAsArray()
        mean = np.mean(array[array > no_data])
    else:
        ds = gdal.Open(FDataDir + '/' + filename)
        band = ds.GetRasterBand(1)
        no_data = band.GetNoDataValue()
        array = band.ReadAsArray()
        mean = np.mean(array[array != no_data])
    return mean

"""The function derives a single average value : float for a given raster file
filename : str
datarype: str Full or Clipped
"""

def No_Data_Value(filename, datatype):
    if datatype == "Clipped":
        ds = gdal.Open(CDataDir + '/' + filename)
        band = ds.GetRasterBand(1)
        no_data = band.GetNoDataValue()
    else:
        ds = gdal.Open(FDataDir + '/' + filename)
        band = ds.GetRasterBand(1)
        no_data = band.GetNoDataValue()
    return no_data
"""The function derives no data values for a given raster file
filename : str
datarype: str Full or Clipped
"""


def Event_pointer(my_list):
    Derivative = list()  # We create here the list where all the derivatives will be stored
    for i in range(0, (len(my_list) - 1)):
        difference = abs(my_list[i + 1][1] - my_list[i][1])
        Derivative.append(difference)
    index_in_dict = max(Derivative)
    Event = Derivative.index(index_in_dict) + 1
    Event_Average = my_list[Event][0]
    return Event_Average

"the function returns the average value of the event:landslide file for each given index list "

def Avg_event_image(index, df):
    # Two arrays with the same shape as our rasters for pre and post events
    Sum_pre = np.zeros((210, 529))
    Sum_post = np.zeros((210, 529))

    # counter
    j = 0
    k = 0
    for i in range(0, len(CSVF) - 2):
        if df.Index[i] == index and df.Event[i] == "Pre-Event":
            ds = gdal.Open(FDataDir + '/' + df.filename[i])
            band = ds.GetRasterBand(1)
            array = band.ReadAsArray()
            No_nan_Val = np.nan_to_num(array, nan=0)
            Sum_pre += No_nan_Val
            j += 1
        elif df.Index[i] == index:
            ds = gdal.Open(FDataDir + '/' + df.filename[i])
            band = ds.GetRasterBand(1)
            array = band.ReadAsArray()
            No_nan_Val = np.nan_to_num(array, nan=0)
            k += 1
            Sum_post += No_nan_Val
    avg_pre = Sum_pre / (j)
    avg_post = Sum_post / (k)
    result = (avg_post - avg_pre)

    return np.array(result)


def Avg_post_image(index, df):
    ## The function creates an average image of all the pre events for a given index
    Sum_pre = np.zeros((210, 529))
    Sum_post = np.zeros((210, 529))
    # counter
    j = 0
    k=0
    for i in range(0, len(CSVF) - 2):
        if df.Index[i] == index and df.Event[i] == "Pre-Event":
            ds = gdal.Open(FDataDir + '/' + df.filename[i])
            band = ds.GetRasterBand(1)
            array = band.ReadAsArray()
            No_nan_Val = np.nan_to_num(array, nan=0)
            Sum_pre += No_nan_Val
            j += 1
        elif df.Index[i] == index:
            ds = gdal.Open(FDataDir + '/' + df.filename[i])
            band = ds.GetRasterBand(1)
            array = band.ReadAsArray()
            No_nan_Val = np.nan_to_num(array, nan=0)
            k += 1
            Sum_post += No_nan_Val
    avg_post = Sum_post / (k)
    return np.array(avg_post)


def Avg_pre_image(index, df):
    ## The function creates an average image of all the pre events for a given index
    Sum_pre = np.zeros((210, 529))
    Sum_post = np.zeros((210, 529))
    # counter
    j = 0
    k=0
    for i in range(0, len(CSVF) - 2):
        if df.Index[i] == index and df.Event[i] == "Pre-Event":
            ds = gdal.Open(FDataDir + '/' + df.filename[i])
            band = ds.GetRasterBand(1)
            array = band.ReadAsArray()
            No_nan_Val = np.nan_to_num(array, nan=0)
            Sum_pre += No_nan_Val
            j += 1
        elif df.Index[i] == index:
            ds = gdal.Open(FDataDir + '/' + df.filename[i])
            band = ds.GetRasterBand(1)
            array = band.ReadAsArray()
            No_nan_Val = np.nan_to_num(array, nan=0)
            k += 1
            Sum_post += No_nan_Val
    avg_pre = Sum_pre / (j)
    return np.array(avg_pre)

def plotimg(var, xlable,barlabel,namesave ):
    plot.figure(figsize=(16, 6), dpi=600)
    plot.xlabel(xlable, fontsize=20)
    im = plot.imshow(var, )
    plot.colorbar(im, label = barlabel)
    plot.savefig(SaveOutput + "/" + namesave + '.jpg',dpi=600)
    return

li2 = [i for i in range(len(res))]
li3 = [i for i in range(len(resF))]

CSV = pd.DataFrame(index=li2,
                   columns=["filename", "Index", "Date", "NoDataValue", "Average", "Event"])
for i in range(0, len(res)):
    filename = res[i]
    CSV.filename[i] = filename
    CSV.Index[i] = Index(filename, "Clipped")
    CSV.Date[i] = Date(filename, "Clipped")
    CSV.NoDataValue[i] = No_Data_Value(filename, "Clipped")
    CSV.Average[i] = Average_Index_Value(filename, "Clipped")
# here we are creating the dataframe, we need a separte function for the averaged images.

##Tuples for BI
bikeys = (CSV[CSV.Index == "BI"]["Date"])
bivalues = CSV[CSV.Index == "BI"]["Average"]

BI_Average = list(zip(bikeys, bivalues))
BI_Average = list(sorted(BI_Average))
BI_Average

##Tuples for NNDMI

ndmikeys = (CSV[CSV.Index == "NDMI"]["Date"])
ndmivalues = CSV[CSV.Index == "NDMI"]["Average"]

NDMI_Average = list(zip(ndmikeys, ndmivalues))
NDMI_Average = list(sorted(NDMI_Average))
NDMI_Average

##Tuples for NDVI
ndvikeys = (CSV[CSV.Index == "NDVI"]["Date"])
ndvivalues = CSV[CSV.Index == "NDVI"]["Average"]

NDVI_Average = list(zip(ndvikeys, ndvivalues))
NDVI_Average = list(sorted(NDVI_Average))


LS_DateBI = Event_pointer(BI_Average)
LS_DateNDVI = Event_pointer(NDVI_Average)
LS_DateNDMI = Event_pointer(NDMI_Average)

print("the date for significant change in the indexes for BI, NDVI, and NDMI are: ")
print("BI", LS_DateBI)
print("NDVI", LS_DateNDVI)
print("NDMI", LS_DateNDMI)


if LS_DateBI == LS_DateNDMI and LS_DateNDVI == LS_DateNDMI:
    LS_Date = LS_DateNDMI
    print("Similar dates were obtained by different indexes.")
else:
    print("No Similar dates were obtained by different indexes.")

CSVF = pd.DataFrame(index=li3,
                    columns=["filename", "Index", "Date", "NoDataValue", "Event"])
for i in range(0, len(resF) - 1):
    filename = resF[i]
    CSVF.filename[i] = filename
    CSVF.Index[i] = Index(filename, "Full")
    CSVF.Date[i] = Date(filename, "Full")
    CSVF.NoDataValue[i] = No_Data_Value(filename, "Full")

for i in range(0, len(li3) - 1):
    Dateformat = (pd.to_datetime(CSVF.Date[i]))
    if (Dateformat < pd.to_datetime(LS_Date)):
        CSVF.Event[i] = "Pre-Event"
    elif Dateformat == pd.to_datetime(LS_Date):
        CSVF.Event[i] = "Event period"
    else:
        CSVF.Event[i] = "Post-Event"

CSV.sort_values("Date")
CSV = CSV.reset_index()
CSVF.sort_values("Date")
CSVF = CSVF.reset_index()

CSV.to_csv( str(SaveOutput) + "/" + "Clipped_data.csv")
CSVF.to_csv(SaveOutput + "/" + "Full_data.csv")
print("The CSV files are available in your output folder")



dBI = Avg_event_image("BI", CSVF)
dNDMI = Avg_event_image("NDMI", CSVF)
dNDVI = Avg_event_image("NDVI", CSVF)



## plotting d_Index images

plot.figure(figsize=(16, 6), dpi=600)
plot.xlabel("dNDVI", fontsize=20)
im = plot.imshow(dNDVI)
plot.colorbar(im, label = "dNDVI values")
plot.savefig(SaveOutput + "/dNDVI" + '.jpg', dpi=600)

plot.figure(figsize=(16, 6), dpi=600)
plot.xlabel("dNDMI", fontsize=20)
im = plot.imshow(dNDMI)
plot.colorbar(im, label = "dNDMI values")
plot.savefig(SaveOutput + "/dNDMI" + '.jpg', dpi=600)

plot.figure(figsize=(16, 6), dpi=600)
plot.xlabel("dBI", fontsize=20)
im = plot.imshow(dBI)
plot.colorbar(im, label = "dBI values")
plot.savefig(SaveOutput + "/dBI" + '.jpg', dpi=600)

print("the dNDVI, dNDMI, and dBI images are stored in your output folder!")
# In[86]:


# Plotting BI
sorted = CSV.sort_values("Date")
plot.figure(figsize=(16, 6), dpi=600)
plot.plot(sorted.Date[CSV.Index == "BI"], sorted.Average[CSV.Index == "BI"], label="BI", color='black')
plot.axvline(x=LS_Date, color='r', label='LS event')
plot.legend(prop={'size': 20})
plot.xlabel("Dates", fontsize=20)
plot.ylabel("Index Value", fontsize=20)
plot.savefig(SaveOutput + "/BI" + '_timeseries.jpg', dpi=600)

# Plotting NDMI

plot.figure(figsize=(16, 6), dpi=600)
plot.plot(sorted.Date[CSV.Index == "NDMI"], sorted.Average[CSV.Index == "NDMI"], label="NDMI", color='black')
plot.axvline(x=LS_Date, color='r', label='LS event')
plot.legend(prop={'size': 20})
plot.xlabel("Dates", fontsize=20)
plot.ylabel("Index Value", fontsize=20)
plot.savefig(SaveOutput + "/NDMI" + '_timeseries.jpg', dpi=600)

# Plotting NDVI

plot.figure(figsize=(16, 6), dpi=600)
plot.plot(sorted.Date[CSV.Index == "NDVI"], sorted.Average[CSV.Index == "BI"], label="NDVI", color='black')
plot.axvline(x=LS_Date, color='r', label='LS event')
plot.legend(prop={'size': 20})
plot.xlabel("Dates", fontsize=20)
plot.ylabel("Index Value", fontsize=20)
plot.savefig(SaveOutput + "/NDVI" + '_timeseries.jpg', dpi=600)

print("the NDVI, NDMI, and BI timeseries images are stored in your output folder!")

# open the TIFF file
dataset = gdal.Open(FDataDir + "/" + resF[2])
wkt = dataset.GetProjection()
gt = dataset.GetGeoTransform()
def to_tiff(index_array,index_type):
    # Get the TIFF driver
    driver = gdal.GetDriverByName("GTiff")
    # Create a new TIFF file
    file_name = SaveOutput + '/' + index_type + '.tif'
    width, height = index_array.shape[1], index_array.shape[0]
    dataset = driver.Create(file_name, width, height, 1, gdal.GDT_Float32)
    # Write the data array to the TIFF file
    dataset.SetGeoTransform(gt)
    dataset.SetProjection(wkt)
    dataset.GetRasterBand(1).WriteArray(index_array)
    # Close the dataset
    dataset = None

to_tiff(dBI,'BI')
to_tiff(dNDMI, 'NDMI')
to_tiff(dNDVI, 'NDVI')

print("the tif files are stored in your output path")

def dindex_clipped(index):
    temp_dataframe = CSV[CSV.Index == index]
    pre_event_avg = (temp_dataframe.Average[temp_dataframe.Date < LS_Date]).tolist()
    x = (sum(pre_event_avg))/len(pre_event_avg)
    temp_dataframe = CSV[CSV.Index == index]
    post_event_avg = (temp_dataframe.Average[temp_dataframe.Date > LS_Date]).tolist()
    y  = (sum(post_event_avg))/len(post_event_avg)
    dindex = y - x
    return dindex

thresholdbi = dindex_clipped("BI") #above this is landslide
thresholdndmi = dindex_clipped("NDMI") #below this is landslide
thresholdndvi = dindex_clipped("NDVI") #below this is landslidd

print("to asess the values of dNDMI and dNDVI, we used the average post-pre values of the CLipped data at landslide loca"
      "tion. The values for NDVI, BI, and NDMI are:")

print(thresholdndvi)
print(thresholdbi)
print(thresholdndmi)


NDVI_class = np.where(dNDVI <= thresholdndvi,1, dNDVI)
NDMI_class = np.where(dNDMI <= thresholdndmi,1, dNDMI)

plot.figure(figsize=(16, 6), dpi=600)
plot.xlabel("possible locations of LS according to NDMI average post-pre event ", fontsize=20)
im = plot.imshow(NDMI_class)
plot.savefig(SaveOutput + "/classNDMI" + '.jpg', dpi=600)

plot.figure(figsize=(16, 6), dpi=600)
plot.xlabel("possible locations of LS according to NDVI average post-pre event ", fontsize=20)
im = plot.imshow(NDVI_class)
plot.savefig(SaveOutput + "/classNDVI" + '.jpg', dpi=600)


pre_BI=Avg_pre_image("BI", CSVF)
pre_NDMI=Avg_pre_image("NDMI", CSVF)
pre_NDVI=Avg_pre_image("NDVI", CSVF)



plotimg(pre_BI,"pre_BI Average","pre_BI avg values","pre_BI")
plotimg(pre_NDMI,"pre_NDMI Average","pre_NDMI avg values","pre_NDMI")
plotimg(pre_NDVI,"pre_NDVI Average","pre_NDVI avg values","pre_NDVI")


post_BI=Avg_post_image("BI", CSVF)
post_NDMI=Avg_post_image("NDMI", CSVF)
post_NDVI=Avg_post_image("NDVI", CSVF)

plotimg(post_BI,"post_BI Average","post_BI avg values","post_BI")
plotimg(pre_NDMI,"post_NDMI Average","post_NDMI avg values","post_NDMI")
plotimg(post_NDVI,"post_NDVI Average","post_NDVI avg values","post_NDVI")

print("All output files are available in the output folder!")