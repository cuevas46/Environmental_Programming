# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from osgeo import gdal
# import sys
# import os
# import GIS_functions as gf
# import datetime
#
# CDataDir = '/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/Data/Clipped_images'
# FDataDir = '/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/Data/Full_image'
# #
# # ##Listing Filenames
# #
# # # folder path
# dir_path = CDataDir
# dir_pathF = FDataDir
# #
# # # list to store files
# res = list()
# resF = list()
# #
# # Iterate directory
# for item in os.listdir(dir_path):
#     # Accessing item by adding directory path and checking if current item is a file
#     if os.path.isfile(os.path.join(dir_path, item)):
#         res.append(item)
# for item in os.listdir(dir_pathF):
#     # Accessing item by adding directory path and checking if current item is a file
#     if os.path.isfile(os.path.join(dir_pathF, item)):
#         resF.append(item)
# #
# #print(res)
# #
# # #Sorting independent picture into lists
# BI = list()
# NDMI = list()
# NDVI = list()
# BI_Date = list()
# NDMI_Date = list()
# NDVI_Date = list()
# for i in range (0, len(res)):
#     temp_list = res[i].split('_')
#     if temp_list[1] == 'BI':
#         BI.append(res[i])
#         BI_Date.append((temp_list[2].split("."))[0]) #Here you split and take index 0, which is the date.
#         #This is the same thing that was done for the temp_list, but just in one line
#     elif temp_list[1] == 'NDMI':
#         NDMI.append(res[i])
#         NDMI_Date.append(temp_list[2].split(".")[0])
#     elif temp_list[1] == 'NDVI':
#         NDVI.append(res[i])
#         NDVI_Date.append(temp_list[2].split(".")[0])
# print(BI_Date)
# print(NDMI_Date)
# print(NDVI_Date)
#
# #BI is the list with all the Bi files
# #This can be transform into a function
# avg_bi = list()
# for i in range (0,len(BI)):
#     ds = gdal.Open(CDataDir+'/'+BI[i]) #We are openning all the Bi files in the directory
#     band = ds.GetRasterBand(1) #to access the information store in our data set
#     no_data = band.GetNoDataValue()
#     array = band.ReadAsArray() #We will read the band object into this array
#     # plt.imshow(array)
#     # plt.show()
#     #print(array[array>no_data])
#     mean_bi = np.mean(array[array > no_data])
#     avg_bi.append(mean_bi)
# # print(avg_bi)
#
# avg_ndmi = list()
# for i in range (0,len(NDMI)):
#     ds1 = gdal.Open(CDataDir+'/'+NDMI[i])
#     band1 = ds1.GetRasterBand(1)
#     no_data1 = band1.GetNoDataValue()
#     array1 = band1.ReadAsArray()
#     mean_ndmi = np.mean(array1[array1 > no_data])
#     avg_ndmi.append(mean_ndmi)
#
# # print(avg_ndmi)
#
# avg_ndvi = list()
# for i in range (0,len(NDVI)):
#     ds = gdal.Open(CDataDir+'/'+NDVI[i])
#     band = ds.GetRasterBand(1)
#     no_data = band.GetNoDataValue()
#     array = band.ReadAsArray()
#     mean_ndvi = np.mean(array[array > no_data])
#     avg_ndvi.append(mean_ndvi)
#
# # print(avg_ndvi)
#
# dates = BI_Date + NDMI_Date + NDVI_Date
# # dates
# Day =list()
# Month =list()
# Year =list()
# for i in range (0, (len(dates))): #Ali has a -1
#     Year.append(dates[i][0:4])
#     Month.append(dates[i][4:6])
#     Day.append(dates[i][6:8])
#
# date_form = list()
# for i in range (0,len(dates)): #Ali has a -1
#     date = str(datetime.date(int(Year[i]),int(Month[i]),int(Day[i])))
#     date_form.append(date)
# #
# date_form1= date_form.sort() #To sort in order the dates
# print(date_form)
# plt.imshow(array)
# plt.show()
# plt.figure()
# plt.plot(date_form, avg_bi/max((avg_bi)), label='Avergae BI') #normalized BI
# plt.plot(date_form,avg_ndvi, label='Avergae ndvi')
# plt.plot(date_form,avg_ndmi, label='Avergae ndmi')
# plt.legend(loc='best')
# plt.show()
#
# #Point 6 onwards
# # full_images = gf.list_files_in_folder(FDataDir, extension='tif')
#
# ###More Scrap ####################
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from osgeo import gdal
# import sys
# import os
# import GIS_functions as gf
# import datetime
#
# CDataDir = '/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/Data/Clipped_images'
# FDataDir = '/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/Data/Full_image'
#
# #Listing Filenames
#
# # folder path
# dir_path = CDataDir
# dir_pathF = FDataDir
#
# # lists to store files
# res = list()
# resF = list()
#
# # Iterate directories
# for item in os.listdir(dir_path):
#     # Accessing item by adding directory path and checking if current item is a file
#     if os.path.isfile(os.path.join(dir_path, item)):
#         res.append(item)
# # print(res)
#
# for item in os.listdir(dir_pathF):
#     # Accessing item by adding directory path and checking if current item is a file
#     if os.path.isfile(os.path.join(dir_pathF, item)):
#         resF.append(item)
#
# # print(resF)
#
# def Index( filename , datatype ): #You have to select wether the file is clipped or full
#     if datatype == "Clipped":
#         index = filename.split("_")[1] #Index is wether is NDMI, BI or NDVI
#     else:
#         index = filename.split("_")[3].split(".")[0] #Index is wether is NDMI, BI or NDVI and here we take the figure format out
#     return index
#
# def Date(filename, datatype ):
#     if datatype == "Clipped":
#         Day = filename.split(".")[0][-2:]
#         Month = filename.split(".")[0][-4:-2]
#         Year = filename.split(".")[0][-8:-4]
#     else:
#         Day = filename.split("_")[2][-2:]
#         Month = filename.split("_")[2][-4:-2]
#         Year = filename.split("_")[2][0:4]
#     date = str(datetime.date(int(Year),int(Month),int(Day)))
#     return date
#
# def Average_Index_Value(filename, datatype):
#     if datatype == "Clipped":
#         ds = gdal.Open(CDataDir+'/'+filename)
#         band = ds.GetRasterBand(1)
#         no_data = band.GetNoDataValue()
#         array = band.ReadAsArray()
#         mean = np.mean(array[array > no_data])
#     else:
#         ds = gdal.Open(FDataDir+'/'+filename)
#         band = ds.GetRasterBand(1)
#         no_data = band.GetNoDataValue()
#         array = band.ReadAsArray()
#         mean = np.nanmean(array[array != no_data])
#     return mean
#
# def No_Data_Value(filename, datatype):
#     if datatype == "Clipped":
#         ds = gdal.Open(CDataDir+'/'+filename)
#         band = ds.GetRasterBand(1)
#         no_data = band.GetNoDataValue()
#     else:
#         ds = gdal.Open(FDataDir+'/'+filename)
#         band = ds.GetRasterBand(1)
#         no_data = band.GetNoDataValue()
#     return no_data
#
# li2 = [i for i in range(len(res))]
# li3 = [i for i in range(len(resF))]
#
# CSV = pd.DataFrame( index = li2,
#                    columns = ["filename" , "Index", "Date", "NoDataValue", "Average","Event"])
# CSVF = pd.DataFrame( index = li3,
#                    columns = ["filename" , "Index", "Date", "NoDataValue", "Average","Event"])
# for i in range (0, len(res)):
#     filename = res[i]
#     CSV.filename[i] = filename
#     CSV.Index[i] = Index(filename, "Clipped")
#     CSV.Date[i] = Date(filename, "Clipped")
#     CSV.NoDataValue[i] = No_Data_Value(filename, "Clipped")
#     CSV.Average[i] = Average_Index_Value(filename, "Clipped")
# #here we are creating the dataframe, we need a separte function for the averaged images.
# for i in range (0, len(resF)):
#     filename = resF[i]
#     CSVF.filename[i] = filename
#     CSVF.Index[i] = Index(filename, "Full")
#     CSVF.Date[i] = Date(filename, "Full")
#     CSVF.NoDataValue[i] = No_Data_Value(filename, "Full")
#     CSVF.Average[i] = Average_Index_Value(filename, "Full")
#
# #We want the same dat only, so we just have to place the date on the dataframe of the full images.
#
# # print(CSVF)
# # print(CSV)
# def Event_pointer(Listname, df):
#     Derivative = list() #We create here the list where all the derivatives will be stored
#     for i in range (0,(len(Listname) - 1)):
#         Mean_Distance = abs(Listname[i+1] - Listname[i])
#         Derivative.append(Mean_Distance)
#     index_in_list = max(Derivative)
#     Event = Derivative.index(index_in_list) + 1
#     Event_Average = Listname[Event]
#     Date_of_Event = df.Date[df.Average == Event_Average]
#     Index = df[df['Average'] == Event_Average].index.values
#     df.loc[Index, 'Event'] = 'LS'
#     return Date_of_Event
# #Basados en el event de las clipped images, debo rellenar el dataframe de las full images
# #pero primero debo dividir
#
# BI_Average =(CSV.Average[CSV.Index == "BI"]).tolist()
# NDMI_Average =(CSV.Average[CSV.Index == "NDMI"]).tolist()
# NDVI_Average =(CSV.Average[CSV.Index == "NDVI"]).tolist()
#
# F_BI_Average =(CSVF.Average[CSVF.Index == "BI"]).tolist()
# F_NDMI_Average =(CSVF.Average[CSVF.Index == "NDMI"]).tolist()
# F_NDVI_Average =(CSVF.Average[CSVF.Index == "NDVI"]).tolist()
# # Dates =(CSV.Date[0:12]).tolist()
# # DatesF =(CSVF.Date[0:16]).tolist()
# # PLotting
# # plt.rcParams["figure.figsize"] = (20,10)
# # plt.figure()
# # plt.plot(DatesF, F_BI_Average)
# # plt.plot(Dates, BI_Average)
# # plt.xlabel("Dates")
# # plt.ylabel("Average BI")
# # plt.show()
# #Like open all the files in the carpet that have the name of the string before Event = event
# #First we need to load the event into the dataframe
#
# # print(Event_pointer(BI_Average, CSV))
# # print(Event_pointer(NDVI_Average, CSV))
# # print(Event_pointer(NDMI_Average, CSV))
# #
# # print(Event_pointer(F_BI_Average, CSVF))
# # print(Event_pointer(F_NDMI_Average, CSVF))
# # print(Event_pointer(F_NDVI_Average, CSVF))
#
#
# # I need all the files previous to the date to be in one part, I need to assign an index to the event based on the list
# #Is it possible to access the files from the data frame?
#
# ##
# # for i in resF:
# #     ds = gdal.Open(FDataDir+'/'+ i)
# #     band = ds.GetRasterBand(1)
# #     no_data = band.GetNoDataValue()
# #     array = band.ReadAsArray()
# #     array[np.isnan(array)] = 0
# #     array +=array
# # final_image = array/len(resF)
# # plt.imshow(final_image)
# # plt.show()
# ##
#
# # # PLotting
# # plt.rcParams["figure.figsize"] = (20,10)
# # plt.figure()
# # plt.plot(Dates, BI_Average)
# # plt.xlabel("Dates")
# # plt.ylabel("Average BI")
# # plt.savefig('/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/BI_timeseries.jpg', dpi = 600)
# # plt.figure()
# # plt.plot(Dates, NDMI_Average)
# # plt.xlabel("Dates")
# # plt.ylabel("Average NDMI")
# # plt.savefig('/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/NDMI_timeseries.jpg', dpi = 600)
# # plt.figure()
# # plt.plot(Dates, NDVI_Average)
# # plt.xlabel("Dates")
# # plt.ylabel("Average NDVI")
# # plt.savefig('/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/NDVI_timeseries.jpg', dpi = 600)
# #
# # #Exporting
# CSV.to_excel("/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/TimeSeriesC.xlsx")
# CSVF.to_excel("/Users/cuevas46/Documents/Environmental_Programming/Project/A3_Landslide_detection/TimeSeriesF.xlsx")
#
# for i in range(0, (len(Listname) - 1)):
#     Mean_Distance = abs(Listname[i + 1] - Listname[i])
#     Derivative.append(Mean_Distance)
# index_in_list = max(Derivative)
# Event = Derivative.index(index_in_list) + 1
# Event_Average = Listname[Event]
# print(Event_Average)
# Date_of_Event = CSV.Date[CSV.Average == Event_Average]
# Index = CSV[CSV['Average'] == Event_Average].index.values
# Date_of_Event = CSV['Date'].values[Index])
# Date_of_EvenF = CSVF.Date[CSVF.Date == Date_of_Event]
# # print(Date_of_EvenF)
# # IndexF = CSVF[CSVF['Date'] == CSV.loc[Index, 'Date']].index.values
# # CSVF.loc[IndexF, 'Event'] = 'LS'
# return Date_of_Event
