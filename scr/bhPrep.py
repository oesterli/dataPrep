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

# Functions for processing
import bhUtils


################################
## Load Configuration
################################
with open("/Users/oesterli/Documents/_temp/bhPrep/scr/config.json",) as file:
    conf = json.load(file)

## Specify variables
now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

source_file = conf["source_csv"]
data_folder = conf["data_path"]
ext = conf["file_ext"]

source_ch_peri = conf["source_CH-perimeter"]

out_dir = conf["out_dir"]
sel_cols = conf["sel_cols"]

raw_bh_fname = conf["raw_bh_fname"]
private_bh_fname = conf["private_bh_fname"]
public_bh_fname = conf["public_bh_fname"]
bh_2d_fname = conf["bh_2d_fname"]

################################
## Load data
################################

## Load a single file
#data = bhUtils.singleDataLoader(source_file)

## Log checkpoint
#text = "> SingleDataLoader: ", source_file, " loaded!"
#bhUtils.loggerX(out_dir, text)
##print("-------------------")

## Read multiple files
files, data = bhUtils.multiDataLoader(data_folder, ext)

## Log checkpoint
text = "> MultiDataLaoder. Files loaded: ", files
bhUtils.loggerX(out_dir, text)
##print("-------------------")


################################
## Display data
################################
## Display all columns
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
#display(data.head(5))

## Display all columns and dtypes
## Log checkpoint
text = data.info(verbose=True)
bhUtils.loggerX(out_dir, text)
##print("-------------------")


################################
## Statistics
################################
## Create some simple statistics
num_bh = len(data['SHORTNAME'].unique())
num_layers = data.shape[0]

## Log checkpoint
text = "> Number of individual borehole: ", num_bh, "\n", "> Number of individual layers: ", num_layers
bhUtils.loggerX(out_dir, text)
##print("-------------------")


## Calculate number of layers per borehole
layer_per_bh = data.groupby('SHORTNAME')['DEPTHFROM'].nunique()

## Log checkpoint
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
#plt.show()

pname = "bh_raw_" + now + ".jpg"
ppath = os.path.join(out_dir, pname)
fig1.savefig(ppath)
plt.close()

## Log checkpoint
text = "> RAW data plotted"
bhUtils.loggerX(out_dir, text)
##print("-------------------")


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

## Log checkpoint
text = "> Raw data exported!"
bhUtils.loggerX(out_dir, text)
##print("-------------------")

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

## Log checkpoint
text = "> Duplicate Rows except first occurrence based on all columns are :", dup_rows['LONGNAME'].count()
bhUtils.loggerX(out_dir, text)

#Show duplicate entries if exisiting
if len(dup_rows) > 0:
    ## Log checkpoint
    text = "> Duplicate rows: "
    bhUtils.loggerX(out_dir, text)

    dup_rows.head()
else:
    pass

## Drop all duplicated rows and save result to "data"
if len(dup_rows) > 0:
    data = data.drop_duplicates(subset=cols)

    ## Log checkpoint
    text = "> ", len(dup_rows), " rows dropped"
    bhUtils.loggerX(out_dir, text)
else:
    ## Log checkpoint
    text = "> No rows dropped"
    bhUtils.loggerX(out_dir, text)

## Log checkpoint
text = "> Check for duplicates finished!"
bhUtils.loggerX(out_dir, text)
##print("-------------------")

## Select only relevant columns
data = data[sel_cols]

## Log checkpoint
text = "> Shape, only relevant columns", data.shape
bhUtils.loggerX(out_dir, text)


################################
## Convert DataFrame to GoeDataFrame
################################
# ## Convert dataframe to geodataframe "gdf" and set inital crs to epsg:2056
private_bh = bhUtils.makeGeospatial(data, 2056)

## Log checkpoint
text = "> Geodataframe created", "\n", "> CRS set to : ", private_bh.crs
bhUtils.loggerX(out_dir, text)
##print("-------------------")


################################
## Delete dataframe and free memory
################################
del(data)
gc.collect()


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
#plt.show()

pname = "private_bh_" + now + ".jpg"
ppath = os.path.join(out_dir, pname)
fig2.savefig(ppath)
plt.close()

## Log checkpoint
text = "> PRIVATE data plotted"
bhUtils.loggerX(out_dir, text)
##print("-------------------")

## Check Columns
## Log checkpoint
text = private_bh.info(verbose=True)
bhUtils.loggerX(out_dir, text)

################################
## Clip and reproject
################################
## Clip the data using GeoPandas clip
private_bh = gpd.clip(private_bh, ch_peri)

## Log checkpoint
text = "> Geodataframe clipped."
bhUtils.loggerX(out_dir, text)
##print("-------------------")

## Reproject Geodataframe and write re-projected coordinates into new column
private_bh = bhUtils.reprojecter(private_bh)

## Log checkpoint
text = "> Reprojected CRS: ", private_bh.crs
bhUtils.loggerX(out_dir, text)
##print("-------------------")


################################
## Export PRIVATE data
################################
## Rename columns for export
private_bh.columns = conf["export_pri_cols"]


## Export data to csv
bhUtils.exporter(out_dir, private_bh_fname, private_bh)

## Log checkpoint
text = "> Private data exported!"
bhUtils.loggerX(out_dir, text)
##print("-------------------")

## Log checkpoint
text = "> Data processing finished!"
bhUtils.loggerX(out_dir, text)
print("===================")

################################
## Process PUBLIC data
################################

## Check Columns
## Log checkpoint
text = "Info PRIVATE data", private_bh.info(verbose=True)
bhUtils.loggerX(out_dir, text)

private_bh.columns = conf["cols_pub"]
public_bh = private_bh

################################
## Delete dataframe and free memory
################################
del(private_bh)
gc.collect()

## Check Columns
text = "Info PUBLIC data before processing", public_bh.info(verbose=True)
bhUtils.loggerX(out_dir, text)

## Create new columns "start" and "end" and fill it with start and end depth
public_bh['start'] = public_bh.groupby('SHORTNAME')['DEPTHFROM'].transform('min')
public_bh['end'] = public_bh.groupby('SHORTNAME')['DEPTHTO'].transform('max')

## Split layer based on restriction level
# Select row which have "RESTRICTIO" == "g"
# Select row which have "RESTRICTIO" == "f"
# Select row which have "RESTRICTIO" == "b"

df_g = public_bh.loc[public_bh["RESTRICTIO"] == "g"].sort_values(by=["SHORTNAME", "DEPTHFROM"])
df_f = public_bh.loc[public_bh["RESTRICTIO"] == "f"].sort_values(by=["SHORTNAME", "DEPTHFROM"])
df_b = public_bh.loc[public_bh["RESTRICTIO"] == "b"].sort_values(by=["SHORTNAME", "DEPTHFROM"])

# Some stats ...
df_sum = df_g.shape[0] + df_b.shape[0] + df_f.shape[0]

## Log checkpoint
text = "All unique data: ",public_bh.shape, "\n", "Restricted unique data: ", df_g.shape, "\n", "Restricted until unique data: ", df_b.shape, "\n", "Non-restricted unique data: ", df_f.shape, "\n", "Restricted + restircted until + Non-restricted data: ", df_sum, "\n", "Difference between all unique data and restriceted + Non-restricted: ", public_bh.shape[0] - df_sum
bhUtils.loggerX(out_dir, text)

## delete duplicates in df_g
df_g_unique = public_bh.loc[public_bh["RESTRICTIO"] == "g"].sort_values(by=["SHORTNAME", "DEPTHFROM"]).drop_duplicates("SHORTNAME")
print('df_g_unique: ', df_g_unique.shape)

## delete duplicates in df_b
df_b_unique = public_bh.loc[public_bh["RESTRICTIO"] == "b"].sort_values(by=["SHORTNAME", "DEPTHFROM"]).drop_duplicates("SHORTNAME")
print('df_b_unique: ', df_b_unique.shape)

## Append df_b to df_g, so that all restriced data are in one dataframe
df_g_unique = df_g_unique.append(df_b_unique)

##Replace layer details with undefined values
## Overwrite "DEPTHFROM" and "DEPTHTO" with "start" and "end", respectively
df_g_unique["DEPTHFROM"] = df_g_unique["start"]
df_g_unique["DEPTHTO"] = df_g_unique["end"]

## Overwrite "LAYERDESC" of restricted boreholes ("RESTRICTIO = "g) with "Undefined"
df_g_unique[["LAYERDESC", "ORIGGEOL", "ORIGNAME", "BOHRTYP", "CHRONOSTR", "LITHOLOGY", "LITHOSTRAT"]] = "Undefined"

##Combine free and restricted data into one
# Combine the two dataframe df_g and df_f
frames = [df_g_unique, df_f]
public_bh = pd.concat(frames)

# Drop the columns "start" and "end"
public_bh = public_bh.drop(["start", "end"], axis=1)

# Sort dataset by unique-ID "SHORTNAME" and "DEPTHFROM"
public_bh = public_bh.sort_values(by=["SHORTNAME", "DEPTHFROM"])

## Log checkpoint
text = "Info PUBLIC data after processing", public_bh.info(verbose=True)
bhUtils.loggerX(out_dir, text)

################################
## Export PUBLIC data
################################
## Rename columns for export
public_bh.columns = conf["export_pub_cols"]

## Export data to csv
bhUtils.exporter(out_dir, public_bh_fname, public_bh)

## Log checkpoint
text = "> Public data exported!"
bhUtils.loggerX(out_dir, text)
##print("-------------------")


################################
## Process 2D data
################################
## Reset columns names to orginal
public_bh.columns = conf["cols_pub"]

# Drop all duplicated record based on unique-ID "SHORTNAME" apart from first record
bh_2d = public_bh.drop_duplicates(subset=["SHORTNAME"], keep="first")

# Select only relvant columns and save it back into "df_all_unique"
bh_2d = bh_2d[conf["cols_2D"]]

## Create new Attribute for Link to swissgeol
# Define parameters
baseURL = 'https://swissgeol.ch/?'
para_sep = '&'
layer_key = 'layers='
layer_value = 'boreholes'
layer_vis = 'layers_visibility='
layer_vis_value = 'true'
layer_trans = 'layers_transparency='
layer_trans_value = '0'
link_key = 'zoom_to='
link_sep = ','

# create Link
bh_2d['link'] = baseURL + layer_key + layer_value + para_sep + layer_vis + layer_vis_value + para_sep + layer_trans + layer_trans_value + para_sep + link_key + bh_2d['x4326'].map(str) + link_sep + bh_2d['y4326'].map(str) + link_sep + '0'

## Log checkpoint
text = "Info 2D data", bh_2d.info(verbose=True)
bhUtils.loggerX(out_dir, text)

################################
## Export 2D data
################################
## Rename columns for export
public_bh.columns = conf["export_pub_cols"]

## Export data to csv
bhUtils.exporter(out_dir, bh_2d_fname, bh_2d)

## Log checkpoint
text = "> 2D data exported!"
bhUtils.loggerX(out_dir, text)
##print("-------------------")

print("===================")
print(">>> Data processing terminated!")
print("=================== S T O P ")