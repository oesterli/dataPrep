# Main Program

#################################
## IMPORTS
#################################
from IPython.display import display
import os
import gc
import datetime
import json
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from pyproj import Proj
import matplotlib as mpl
import matplotlib.pyplot as plt

import bhUtils


################################
## Load Configuration
################################
with open("/Users/oesterli/Documents/_temp/bhPrep/scr/config.json",) as file:
    conf = json.load(file)

## Specify variables
now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

source_file = conf["source_gpkg"]
data_folder = conf["data_path"]
ext = conf["file_ext"]

source_ch_peri = conf["source_CH-perimeter"]

out_dir = conf["out_dir"]
sel_cols = conf["sel_cols"]

raw_bh_fname = conf["raw_bh_fname"]
private_bh_fname = conf["private_bh_fname"]
public_bh_fname = conf["public_bh_fname"]

################################
## Load data
################################

## Load a single file
#out_data = testDataloader.singleDataLoader(source_file)
#print('> Data loaded')
#print("-------------------")

## Read multiple files
files, data = bhUtils.multiDataLoader(data_folder, ext)
#print("> Files loaded: ", files)
#print("-------------------")

## Log checkpoint
text = "> Files loaded: ", files
bhUtils.loggerX(out_dir, text)


################################
## Display data
################################
## Display all columns
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
#display(data.head(5))

## Display all columns and dtypes
#print(data.info(verbose=True))


################################
## Statistics
################################
## Create some simple statistics
num_bh = len(data['SHORTNAME'].unique())
num_layers = data.shape[0]

text = "> Number of individual borehole: ", num_bh
bhUtils.loggerX(out_dir, text)
text = "> Number of individual layers: ", num_layers
bhUtils.loggerX(out_dir, text)


## Calculate number of layers per borehole
layer_per_bh = data.groupby('SHORTNAME')['DEPTHFROM'].nunique()

text = "> Stats: ", layer_per_bh.describe()
bhUtils.loggerX(out_dir, text)
#("-------------------")


################################
# Plot RAW data
################################
fig1, axs = plt.subplots(2)
fig1.suptitle('x-/y-coordinates; TiefeMD')
axs[0].plot(data['XCOORD'], data['YCOORD'], '+', color='black')
axs[1].hist(data['TIEFEMD'], label='TIEFEMD', log=True, histtype='bar', edgecolor='black',  color='green')
plt.show()

pname = "bh_raw_" + now + ".jpg"
ppath = os.path.join(out_dir, pname)
fig1.savefig(ppath)
plt.close()

text = "> RAW data plotted"
bhUtils.loggerX(out_dir, text)
#print("-------------------")


################################
# Processing RAW data
################################
## Sort data by "SHORTNAME" and "DEPTHFROM"
data = data.sort_values(by=["SHORTNAME", "DEPTHFROM"])

## Create an index column
data['index'] = data.index

## Round data
data['XCOORD'] = data['XCOORD'].round(decimals=2)
data['YCOORD'] = data['YCOORD'].round(decimals=2)
data['ZCOORDB'] = data['ZCOORDB'].round(decimals=2)
data['TIEFEMD'] = data['TIEFEMD'].round(decimals=2)
data['DEPTHFROM'] = data['DEPTHFROM'].round(decimals=2)
data['DEPTHTO'] = data['DEPTHTO'].round(decimals=2)


################################
## Export RAW data
################################
## Export data to csv
bhUtils.exporter(out_dir, raw_bh_fname, data)
text = "> Raw data exported!"
bhUtils.loggerX(out_dir, text)
#print("-------------------")

################################
## Process PRIVATE data
################################
## Check for duplicates
## Copy all columns name to list "cols"
cols = data.columns.to_list()

## Create a list of columns except the index column, in order to use it as a subset for finding duplicate rows
cols = cols[0:-1]

# Find duplicate rows (checking duplicates based on all columns)
dup_rows = data[data.duplicated(subset=cols)]

text = "> Duplicate Rows except first occurrence based on all columns are :", dup_rows['LONGNAME'].count()
bhUtils.loggerX(out_dir, text)

#Show duplicate entries if exisiting
if len(dup_rows) > 0:
    text = "> Duplicate rows: "
    bhUtils.loggerX(out_dir, text)

    dup_rows.head()
else:
    pass

## Drop all duplicated rows and save result to "data"
if len(dup_rows) > 0:
    data = data.drop_duplicates(subset=cols)
    text = "> ", len(dup_rows), " rows dropped"
    bhUtils.loggerX(out_dir, text)
else:
    text = "> No rows dropped"
    bhUtils.loggerX(out_dir, text)

text = "> Check for duplicates finished!"
bhUtils.loggerX(out_dir, text)
#print("-------------------")

## Select only relevant columns
data = data[sel_cols]
text = "> Shape, only relevant columns", data.shape
bhUtils.loggerX(out_dir, text)


################################
## Convert DataFrame to GoeDataFrame
################################
# ## Convert dataframe to geodataframe "gdf" and set inital crs to epsg:2056
private_bh = bhUtils.makeGeospatial(data, 2056)
text = "> Geodataframe created"
bhUtils.loggerX(out_dir, text)
text = "> CRS set to : ", private_bh.crs
bhUtils.loggerX(out_dir, text)
#print("-------------------")

################################
## Plot PRIVATE data
################################

## Load swiss boundary from shapefile
ch_peri = gpd.read_file(source_ch_peri)

## Select only swiss perimeter
ch_peri = ch_peri[ch_peri['ICC'] == 'CH']

## Create buffer around CH-Perimeter
ch_peri_buf = ch_peri.buffer(20000)

## Plot GeoDataFrame together with swiss boundary
fig2, ax = plt.subplots()
fig2.suptitle('Geographic distribution of PRIVATE data')
ax.set_aspect('equal')
ch_peri.plot(ax=ax, color='white', edgecolor='black')
ch_peri_buf.plot(ax=ax, edgecolor='blue', facecolor='none')
private_bh.plot(ax=ax, color='red', markersize=5)
plt.show()

pname = "private_bh_" + now + ".jpg"
ppath = os.path.join(out_dir, pname)
fig2.savefig(ppath)
plt.close()

text = "> PRIVATE data plotted"
bhUtils.loggerX(out_dir, text)
#print("-------------------")

################################
## Clip and reproject
################################
## Clip the data using GeoPandas clip
private_bh = gpd.clip(private_bh, ch_peri)
text = "> Geodataframe clipped."
bhUtils.loggerX(out_dir, text)
#print("-------------------")

## Reproject Geodataframe and write re-projected coordinates into new column
private_bh = bhUtils.reprojecter(private_bh)
text = "> Reprojected CRS: ", private_bh.crs
bhUtils.loggerX(out_dir, text)
#print("-------------------")


################################
## Export PRIVATE data
################################
## Rename columns for export
private_bh.columns = conf["export_pri_cols"]


## Export data to csv
bhUtils.exporter(out_dir, private_bh_fname, private_bh)
text = "> Private data exported!"
bhUtils.loggerX(out_dir, text)
#print("-------------------")


text = "> Data processing finished!"
bhUtils.loggerX(out_dir, text)
print("===================")

################################
## Delete dataframe and free memory
################################
del(data)
gc.collect()