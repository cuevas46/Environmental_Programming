import os
import datetime
import calendar
import collections
import subprocess
import csv
from osgeo import gdal, osr
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import numpy as np

gdal.UseExceptions()

def get_gdalwarp_info(fih, subdataset=0):
    """
    Get information in string format from a geotiff or HDF4 file for use by GDALWARP.

    Parameters
    ----------
    fih : str
        Filehandle pointing to a geotiff or HDF4 file.
    subdataset = int, optional
        Value indicating a subdataset (in case of HDF4), default is 0.

    Returns
    -------
    srs : str
        The projection of the fih.
    clipped_images : str
        Resolution of the fih.
    bbox : str
        Bounding box (xmin, ymin, xmax, ymax) of the fih.
    ndv : str
        No-Data-Value of the fih.
    """
    dataset = gdal.Open(fih, gdal.GA_ReadOnly)
    tpe = dataset.GetDriver().ShortName
    if tpe == 'HDF4':
        dataset = gdal.Open(dataset.GetSubDatasets()[subdataset][0])
    ndv = str(dataset.GetRasterBand(1).GetNoDataValue())
    if ndv == 'None':
        ndv = 'nan'
    srs = dataset.GetProjectionRef()
    if not srs:
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(4326).ExportToPrettyWkt()
        print("srs not defined, using EPSG4326.")
    xsize = dataset.RasterXSize
    ysize = dataset.RasterYSize
    res = ' '.join([str(xsize), str(ysize)])
    geot = dataset.GetGeoTransform()
    xmin = geot[0]
    ymin = geot[3] + geot[5] * ysize
    xmax = geot[0] + geot[1] * xsize
    ymax = geot[3]
    bbox = ' '.join([str(xmin), str(ymin), str(xmax), str(ymax)])
    return srs, res, bbox, ndv
    
def moving_average(date, filehandles, filedates,
                   moving_avg_length=5, method='tail'):
    """
    Compute a moving (tail) average from a series of maps.

    Parameters
    ----------
    date : object
        Datetime.date object for which the average should be computed
    filehandles : ndarray
        Filehandles of the maps.
    filedates : ndarray
        Datetime.date objects corresponding to filehandles
    moving_average_length : int, optional
        Length of the tail, default is 3.
    method : str, optional
        Select wether to calculate the 'tail' average or 'central' average.

    Returns
    -------
    summed_data : ndarray
        The averaged data.
    """
    indice = np.where(filedates == date)[0][0]
    if method == 'tail':
        assert (indice + 1) >= moving_avg_length, "Not enough data available to calculate average of length {0}".format(moving_avg_length)
        to_open = filehandles[indice-(moving_avg_length-1):(indice+1)]
    elif method == 'central':
        assert (moving_avg_length % 2 != 0), "Please provide an uneven moving_avg_length"
        assert indice >= (moving_avg_length - 1) / 2, "Not enough data available to calculate central average of length {0}".format(moving_avg_length)
        assert indice < len(filedates) - (moving_avg_length - 1) / 2, "Not enough data available to calculate central average of length {0}".format(moving_avg_length)
        to_open = filehandles[indice-(moving_avg_length-1)/2:indice+(moving_avg_length-1)/2+1]
    summed_data = open_as_array(filehandles[indice]) * 0
    for fih in to_open:
        data = open_as_array(fih)
        summed_data += data
    summed_data /= len(to_open)
    return summed_data
    
def sort_files(input_dir, year_position, month_position=None,
               day_position=None, doy_position=None, extension='tif'):
    r"""
    Substract metadata from multiple filenames.

    Parameters
    ----------
    input_dir : str
        Folder containing files.
    year_position : list
        The indices where the year is positioned in the filenames, see example.
    month_position : list, optional
        The indices where the month is positioned in the filenames, see example.
    day_position : list, optional
        The indices where the day is positioned in the filenames, see example.
    doy_position : list, optional
        The indices where the doy is positioned in the filenames, see example.
    extension : str
        Extension of the files to look for in the input_dir.

    Returns
    -------
    filehandles : ndarray
        The files with extension in input_dir.
    dates : ndarray
        The dates corresponding to the filehandles.
    years : ndarray
        The years corresponding to the filehandles.
    months : ndarray
        The years corresponding to the filehandles.
    days :ndarray
        The years corresponding to the filehandles.
    """
    dates = np.array([])
    years = np.array([])
    months = np.array([])
    days = np.array([])
    filehandles = np.array([])
    files = list_files_in_folder(input_dir, extension=extension)
    for fil in files:
        filehandles = np.append(filehandles, fil)
        year = int(fil[year_position[0]:year_position[1]])
        month = 1
        if month_position is not None:
            month = int(fil[month_position[0]:month_position[1]])
        day = 1
        if day_position is not None:
            day = int(fil[day_position[0]:day_position[1]])
        if doy_position is not None:
            date = datetime.date(year, 1, 1) + datetime.timedelta(int(fil[doy_position[0]:doy_position[1]]) - 1)
            month = date.month
            day = date.day
        else:
            date = datetime.date(year, month, day)
        years = np.append(years, year)
        months = np.append(months, month)
        days = np.append(days, day)
        dates = np.append(dates, date)
    return filehandles, dates, years, months, days
    
def common_dates(dates_list):
    """
    Checks for common dates between multiple lists of datetime.date objects.

    Parameters
    ----------
    dates_list : list
        Contains lists with datetime.date objects.

    Returns
    -------
    com_dates : ndarray
        Array with datetime.date objects for common dates.
    """
    com_dates = dates_list[0]
    for date_list in dates_list[1:]:
        com_dates = np.sort(list(set(com_dates).intersection(date_list)))
    return com_dates
    
def assert_missing_dates(dates, timescale='months', quantity=1):
    """
    Checks if a list of dates is continuous, i.e. are there temporal gaps in the dates.

    Parameters
    ----------
    dates : ndarray
        Array of datetime.date objects.
    timescale : str, optional
        Timescale to look for, default is 'months'.
    """
    current_date = dates[0]
    enddate = dates[-1]
    if timescale == 'months':
        while current_date <= enddate:
            assert current_date in dates, "{0} is missing in the dataset".format(current_date)
            current_date = current_date + relativedelta(months=quantity)


def match_proj_res_ndv(source_file, target_fihs, output_dir, dtype='Float32'):
    """
    Matches the projection, resolution and no-data-value of a list of target-files
    with a source-file and saves the new maps in output_dir.

    Parameters
    ----------
    source_file : str
        The file to match the projection, resolution and ndv with.
    target_fihs : list
        The files to be reprojected.
    output_dir : str
        Folder to store the output.
    resample : str, optional
        Resampling method to use, default is 'near' (nearest neighbour).
    dtype : str, optional
        Datatype of output, default is 'float32'.
    scale : int, optional
        Multiple all maps with this value, default is None.

    Returns
    -------
    output_files : ndarray
        Filehandles of the created files.
    """
    ndv, xsize, ysize, geot, projection = get_geoinfo(source_file)[1:]
    type_dict = {gdal.GetDataTypeName(i): i for i in range(1, 12)}
    output_files = np.array([])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for target_file in target_fihs:
        filename = os.path.split(target_file)[1]
        output_file = os.path.join(output_dir, filename)
        options = gdal.WarpOptions(width=xsize,
                                   height=ysize,
                                   outputBounds=(geot[0], geot[3] + ysize * geot[5],
                                                 geot[0] + xsize * geot[1], geot[3]),
                                   outputBoundsSRS=projection,
                                   dstSRS=projection,
                                   dstNodata=ndv,
                                   outputType=type_dict[dtype])
        gdal.Warp(output_file, target_file, options=options)
        output_files = np.append(output_files, output_file)
    return output_files
    
def get_geoinfo(fih, subdataset=0):
    """
    Substract metadata from a geotiff, HDF4 or netCDF file.

    Parameters
    ----------
    fih : str
        Filehandle to file to be scrutinized.
    subdataset : int, optional
        Layer to be used in case of HDF4 or netCDF format, default is 0.

    Returns
    -------
    driver : str
        Driver of the fih.
    ndv : float
        No-data-value of the fih.
    xsize : int
        Amount of pixels in x direction.
    ysize : int
        Amount of pixels in y direction.
    geot : list
        List with geotransform values.
    Projection : str
        Projection of fih.
    """
    sourceds = gdal.Open(fih, gdal.GA_ReadOnly)
    tpe = sourceds.GetDriver().ShortName
    if tpe == 'HDF4' or tpe == 'netCDF':
        sourceds = gdal.Open(sourceds.GetSubDatasets()[subdataset][0])
    ndv = sourceds.GetRasterBand(1).GetNoDataValue()
    xsize = sourceds.RasterXSize
    ysize = sourceds.RasterYSize
    geot = sourceds.GetGeoTransform()
    projection = osr.SpatialReference()
    projection.ImportFromWkt(sourceds.GetProjectionRef())
    driver = gdal.GetDriverByName(tpe)
    return driver, ndv, xsize, ysize, geot, projection

def list_files_in_folder(folder, extension='tif'):
    """
    List the files in a folder with a specified extension.

    Parameters
    ----------
    folder : str
        Folder to be scrutinized.
    extension : str, optional
        Type of files to look for in folder, default is 'tif'.

    Returns
    -------
    list_of_files : list
        List with filehandles of the files found in folder with extension.
    """
    list_of_files = [os.path.join(folder, fn) for fn in next(os.walk(folder))[2] if fn.split('.')[-1] == extension]
    return list_of_files
    
def open_as_array(fih, bandnumber=1, nan_values=True):
    #astype('float32')
    """
    Open a map as an numpy array.

    Parameters
    ----------
    fih: str
        Filehandle to map to open.
    bandnumber : int, optional
        Band or layer to open as array, default is 1.
    dtype : str, optional
        Datatype of output array, default is 'float32'.
    nan_values : boolean, optional
        Convert he no-data-values into np.nan values, note that dtype needs to
        be a float if True. Default is False.

    Returns
    -------
    array : ndarray
        array with the pixel values.
    """
    dataset = gdal.Open(fih, gdal.GA_ReadOnly)
    tpe = dataset.GetDriver().ShortName
    if tpe == 'HDF4':
        subdataset = gdal.Open(dataset.GetSubDatasets()[bandnumber][0])
        ndv = int(subdataset.GetMetadata()['_FillValue'])
    else:
        subdataset = dataset.GetRasterBand(bandnumber)
        ndv = subdataset.GetNoDataValue()
    array = subdataset.ReadAsArray()
    if nan_values:
        if len(array[array == ndv]) >0:
            array[array == ndv] = np.nan
    return array

def create_geotiff(fih, array, driver, ndv, xsize, ysize, geot, projection, compress=None):
    """
    Creates a geotiff from a numpy array.

    Parameters
    ----------
    fih : str
        Filehandle for output.
    array: ndarray
        array to convert to geotiff.
    driver : str
        Driver of the fih.
    ndv : float
        No-data-value of the fih.
    xsize : int
        Amount of pixels in x direction.
    ysize : int
        Amount of pixels in y direction.
    geot : list
        List with geotransform values.
    Projection : str
        Projection of fih.
    """
    datatypes = {gdal.GetDataTypeName(i).lower() : i for i in range(1, 12)}
    if compress != None:
        dataset = driver.Create(fih, xsize, ysize, 1, datatypes[array.dtype.name], ['COMPRESS={0}'.format(compress)])
    else:
        dataset = driver.Create(fih, xsize, ysize, 1, datatypes[array.dtype.name])
    if ndv is None:
        ndv = -9999
    array[np.isnan(array)] = ndv
    dataset.GetRasterBand(1).SetNoDataValue(ndv)
    dataset.SetGeoTransform(geot)
    dataset.SetProjection(projection.ExportToWkt())
    dataset.GetRasterBand(1).WriteArray(array)
    dataset = None
    if "nt" not in array.dtype.name:
        array[array == ndv] = np.nan

def pixel_coordinates(lon, lat, fih):
    """
    Find the corresponding pixel to a latitude and longitude.

    Parameters
    ----------
    lon : float or int
        Longitude to find.
    lat : float or int
        Latitude to find.
    fih : str
        Filehandle pointing to the file to be searched.

    Returns
    -------
    xpixel : int
        The index of the longitude.
    ypixel : int
        The index of the latitude.
    """
    sourceds = gdal.Open(fih, gdal.GA_ReadOnly)
    xsize = sourceds.RasterXSize
    ysize = sourceds.RasterYSize
    geot = sourceds.GetGeoTransform()
    assert (lon >= geot[0]) & (lon <= geot[0] + xsize * geot[1]), 'longitude is not on the map'
    assert (lat <= geot[3]) & (lat >= geot[3] + ysize * geot[5]), 'latitude is not on the map'
    location = geot[0]
    xpixel = -1
    while location <= lon:
        location += geot[1]
        xpixel += 1
    location = geot[3]
    ypixel = -1
    while location >= lat:
        location += geot[5]
        ypixel += 1
    return xpixel, ypixel   

def assert_proj_res_ndv(list_of_filehandle_lists, check_ndv=True):
    """
    Check if the projection, resolution and no-data-value of all provided filehandles are the same.

    Parameters
    ----------
    list_of_filehandle_lists : list
        List with different ndarray containing filehandles to compare.
    check_ndv : boolean, optional
        Check or ignore the no-data-values, default is True.

    Examples
    --------
    >>> assert_proj_res_ndv([et_fihs, ndm_fihs, p_fihs], check_ndv = True)
    """
    longlist = np.array([])
    for fih_list in list_of_filehandle_lists:
        if isinstance(fih_list, list):
            longlist = np.append(longlist, np.array(fih_list))
        if isinstance(fih_list, np.ndarray):
            longlist = np.append(longlist, fih_list)
        if isinstance(fih_list, str):
            longlist = np.append(longlist, np.array(fih_list))
    t_srs, t_ts, t_te, t_ndv = get_gdalwarp_info(longlist[0])
    for fih in longlist[1:]:
        s_srs, s_ts, s_te, s_ndv = get_gdalwarp_info(fih)
        if check_ndv:
            assert np.all([s_ts == t_ts, s_te == t_te, s_srs == t_srs, s_ndv == t_ndv]), "{0} does not have the same Proj/Res/ndv as {1}".format(longlist[0], fih)
        else:
            assert np.all([s_ts == t_ts, s_te == t_te, s_srs == t_srs]), "{0} does not have the same Proj/Res as {1}".format(longlist[0], fih)
    
    
def map_pixel_area_km(fih, approximate_lengths=False):
    """
    Calculate the area of the pixels in a geotiff.

    Parameters
    ----------
    fih : str
        Filehandle pointing to a geotiff.
    approximate_lengths : boolean, optional
        Give the approximate length per degree [km/deg] instead of the area [km2], default is False.

    Returns
    -------
    map_area : ndarray
        The area per cell.
    """
    xsize, ysize, geot = get_geoinfo(fih)[2:-1]
    area_column = np.zeros((ysize, 1))
    for y_pixel in range(ysize):
        pnt1 = (geot[3] + y_pixel*geot[5], geot[0])
        pnt2 = (pnt1[0], pnt1[1] + geot[1])
        pnt3 = (pnt1[0] - geot[1],  pnt1[1])
        pnt4 = (pnt1[0] - geot[1], pnt1[1] + geot[1])
        u = distance.distance(pnt1, pnt2).km
        l = distance.distance(pnt3, pnt4).km
        h = distance.distance(pnt1, pnt3).km
        area_column[y_pixel, 0] = (u+l)/2*h
    map_area = np.repeat(area_column, xsize, axis=1)
    if approximate_lengths:
        pixel_approximation = np.sqrt(abs(geot[1]) * abs(geot[5]))
        map_area = np.sqrt(map_area) / pixel_approximation
    return map_area


#ClippedDataFiles = gf.list_files_in_folder(CDataDir, extension='tif')

###Another Checkpoint

