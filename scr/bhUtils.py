import geopandas as gpd
import fiona
import os
import datetime
import glob
import pandas as pd
from shapely.geometry import Point


now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Load several files of the same format
def multiDataLoader(sourceFolder, extention):
    """

    :param sourceFolder:
    :param extention:
    :return:
    """
    files = glob.glob(os.path.join(sourceFolder, extention))
    multiData = pd.DataFrame()

    for f in files:
        df = pd.read_excel(f, engine='openpyxl')
        multiData = multiData.append(df, ignore_index=True, sort='false')

    return files, multiData

def singleDataLoader(sourceFile):
    """

    :param sourceFile:
    :return:
    """
    if sourceFile.lower().endswith('.gpkg'):

        # works only in IPython Jupyter Notebook
        #data = gpdread_file(sourceFile)

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

def exporter(outDir, outFname, expData):
    """

    :param outDir:
    :param outFname:
    :param expData:
    """
    outFile = os.path.join(outDir, '_'.join([outFname, str(now).zfill(2), ]) + '.csv')
    expData.to_csv(outFile, index=None, sep=';')

def makeGeospatial(df, inCrs):
    """

    :param df:
    :param inCrs:
    :return:
    """
    ## Convert dataframe to geodataframe "gdf" and set inital crs to epsg:2056
    geom = [Point(xy) for xy in zip(df.XCOORD, df.YCOORD)]
    gdf = gpd.GeoDataFrame(df, crs=inCrs, geometry=geom)
    return gdf

def reprojecter(gdf):
    """

    :param gdf:
    :return:
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

    :param outdir:
    :param text:
    :return:
    """
    fname = "log" + "_" + now + ".txt"
    logFile = os.path.join(outdir, fname)

    with open(logFile, 'a') as f:
        print(now, text, sep=';', file=f)

    # print date, time and message to stdout
    print(now, text)
    print("-------------------")
    return
