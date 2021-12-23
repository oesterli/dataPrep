import datetime
import glob
import os

import fiona
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point

nowExport = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


# Load several files of the same format
def multiDataLoader(sourceFolder, extension):
    """
    :param sourceFolder: Folder with multiple files to load
    :param extension: .xlsx
    :return: all data from multiple files are loaded in "multiData" and got an index number
    """
    files = glob.glob(os.path.join(sourceFolder, extension))
    multiData = pd.DataFrame()

    for f in files:
        df = pd.read_excel(f)
        multiData = multiData.append(df, ignore_index=True, sort='false')

    return files, multiData

def singleDataLoader(sourceFile):
    """

    :param sourceFile: Single File with specific extension
    :param extension: ".gpkg", ".shp" or ".csv"
    :return: Dataframe named "rawData" with data from loaded file and displayed dimensionality of data (nb of rows and columns)
    """
    if sourceFile.lower().endswith('.gpkg'):

        # works only in IPython Jupyter Notebook
        # data = gpdread_file(sourceFile)

        with fiona.Env(OGR_GPKG_FOREIGN_KEY_CHECK='NO'):
            data = fiona.open(sourceFile)
        rawData = pd.DataFrame(data)
        print('Geopackage read')
        print('Rows: ', rawData.shape[0])
        print('Columns: ', rawData.shape[1])
        print("-------------------")

    elif sourceFile.lower().endswith('.shp'):
        rawData = gpd.read_file(sourceFile)
        print('Shapefile read')
        print('Rows: ', rawData.shape[0])
        print('Columns: ', rawData.shape[1])
        print("-------------------")

    elif sourceFile.lower().endswith('.csv'):
        rawData = gpd.read_file(sourceFile)
        print('CSV read')
        print('Rows: ', rawData.shape[0])
        print('Columns: ', rawData.shape[1])
        print("-------------------")

    else:
        print('Unknown file format')
        print("-------------------")

    return rawData


def exporter(outDir, outFname, expData, enc):
    """

    :param outDir: path to folder where output file is saved
    :param outFname: name of the output file
    :param expData: dataframe which will be exported
    :param enc: translation of output language
    """
    outFile = os.path.join(outDir, '_'.join([outFname, str(nowExport).zfill(2), ]) + '.csv')
    expData.to_csv(outFile, index=None, sep=';', encoding=enc)


def exporterX(outDir, outFname, expData, enc):
    """

    :param outDir: path to folder where output file is saved
    :param outFname: name of the output file,
    :param expData: dataframe which will be exported
    :param ext: file extension in the form ".csv", ".jpg", ".txt", ".xlsx"
    """

    if ext == ".csv":
        outFile = os.path.join(outDir, '_'.join([outFname, str(nowExport).zfill(2), ]) + ext)
        expData.to_csv(outFile, index=None, sep=';', encoding=enc)
    elif ext == ".jpg":
        # print("Not yet implemented!")
        pname = "private_bh_" + nowExport + ext
        ppath = os.path.join(out_dir, pname)
        expData.savefig(ppath)
        plt.close()
    else:
        print("File extension: ", ext, " unknown!")


def makeGeospatial(df, inCrs):
    """

    :param df: panda dataframe (pd.dataFrame, df) for georeferencing
    :param inCrs: crs code for needed projection
    :return: georeferenced geodataframe of df set to Swiss CH1903+ / LV95
    """
    ## Convert dataframe to geodataframe "gdf" and set inital crs to epsg:2056
    geom = [Point(xy) for xy in zip(df.XCOORD, df.YCOORD)]
    gdf = gpd.GeoDataFrame(df, crs=inCrs, geometry=geom)
    return gdf


def reprojecter(gdf):
    """

    :param gdf: georeferenced geodataframe
    :return: gdf of epsg:2056 reprojected on epsg:4326 and split into 2 columns x and y
    """
    reproGeom = "geom" + gdf.crs.to_string().split(':')[1]
    gdf[reproGeom] = gdf["geometry"]

    gdf = gdf.to_crs('epsg:4326')

    reproX = "x" + gdf.crs.to_string().split(':')[1]
    reproY = "y" + gdf.crs.to_string().split(':')[1]

    gdf[reproX] = gdf["geometry"].apply(lambda p: p.x)
    gdf[reproY] = gdf["geometry"].apply(lambda p: p.y)

    return gdf


def loggerX(outdir, text):
    """

    :param outdir: path to folder where output file is saved
    :param text: text which will be write down in the log file
    :return: log file which records pre-defined steps to confirm their successful execution
    """

    fname = "log" + "_" + now + ".txt"
    logFile = os.path.join(outdir, fname)

    with open(logFile, 'a') as f:
        print(now, text, sep=';', file=f)

    # print date, time and message to stdout
    print(now, text)
    print("-------------------")
    return
