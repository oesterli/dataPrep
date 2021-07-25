#!/usr/bin/env python
# coding: utf-8

# ## Data preparation swissgeol.ch and map.geo.admin.ch
# 
# # Borehole data
# 
# #### Editor: ON; Date: 10.11.2020

# ### Background
# Borehole data from borehole database have to be integrated nto map.geo.admin.ch and swissgeol.ch simultaniously.
# Data preparation is performed using this skript.
# 
# #### Prodecdure
# 1. Export data on layer basis from GeODin (not part of this skript)
# 2. Import data to DataFrame
# 3. Convert DataFrame to GeoDataFrame
# 4. Check for duplicated rows and delete them
# 5. Check for spatial outline (data not located in CH) and clip to Swiss boundary
# 6. Sort data according to Borehole identifier and Depth of layers
# 7. Select relevant attributes
# 8. ...
# 
#  
# #### Output:
# * 2D dataset containing all boreholes as 2D point geometry and selected attributes
# * public 3D dataset containg all boreholes on a layer basis; individual layers of restricted boreholes are combined to one single layer (*DEPTHTO* = *LENGTH*)
# * private 3D dataset containg all boreholes on a layer basis; individual layers of restricted boreholes are preserved
# 
# #### Directory structure:
# * **Root:**
#     * Directory named as you like, e.g.: `Dataprepration`, all magic is going on inside here!
# * **Input:** 
#     * Borehole data: `./data/input/bh/`
#     * Helper files: `./data/input/helper/`
#     
# * **Output:**    
#     * All output of specific run at a given date, e.g.: `./data/output/run_20201110_01` following the Template `_TEMPLATE_run_YYYYMMDD_00`
#     * Log file of the given run: `log_run_20201110_01`
# 
# 
# #### User Input
# 
# User input is marked by <h3><font color='red'>red</font> text</h3>
# 
# User input is required for:
# * Number of run. Spefify the number of the current run
# * Root directory. The Root path, the location where all input and output data is stored, may be defined by the user. By default the present working direktory, i.e. the directory where this notebook is located, is defined as root directory 
# * Inspecting data
# * [Exporting data](#linkxy)

# In[1]:


# Import libraries
import os
import datetime
import pandas as pd
import numpy as np
import glob
import geopandas as gpd
from shapely.geometry import Point
import matplotlib as mpl 
import matplotlib.pyplot as plt

# Import 'little helpers' for convenience
import onUtils


# <font color=red><h1>
# User Input >>>>></h1></font>

# In[2]:


# USER input required
# >>>>
#run_num = input("Enter run number (0-99):")
run_num = 0

# Root directory
root_dir = get_ipython().run_line_magic('pwd', '')

# >>>>
#root_dir = '/Users/oesterli/Desktop/python_space/'


# <a id="linkConfig"></a>
# <font color=blue><h1>
#     Configuration >>>>></h1></font> 

# In[3]:


# input
## input directory for borhole data
in_dir_bh = os.path.join(root_dir, 'data/input/bh')

## input directory for helper files
in_dir_hp = os.path.join(root_dir,'data/input/helper')
in_dir_hp

# output
## timestamp for out_dir
now = datetime.datetime.now().strftime('%Y%m%d')

## Convert number of run (run_num) to two digit str
run_dir = '_'.join(['run',now,str(run_num).zfill(2)])

## Define output directory path
out_dir_run = os.path.join(root_dir,'data/output',run_dir)

## check if out_dir already exists
if os.path.isdir(out_dir_run):
    print('ok! Out directory already exists.')
else:
    print('Output directory not existing, directory will de created')
    os.mkdir(out_dir_run)
    
# Define name of log-file
log_name = 'test_log'

# Define columns to select
sel_cols = ["index", "XCOORD","YCOORD","ZCOORDB","ORIGNAME","NAMEPUB",
            "SHORTNAME", 'BOHREDAT',"BOHRTYP", 'GRUND',"RESTRICTIO",
            "TIEFEMD","DEPTHFROM","DEPTHTO",'LAYERDESC','ORIGGEOL',"LITHOLOGY", 
            "LITHOSTRAT", 'CHRONOSTR', 'TECTO', 'USCS1', 'USCS2', 'USCS3']

sel_cols_2 = ["XCOORD","YCOORD","ZCOORDB","ORIGNAME","NAMEPUB","SHORTNAME", 
              'BOHREDAT','GRUND',"RESTRICTIO","TIEFEMD","DEPTHFROM","DEPTHTO",'LAYERDESC']

# Original column names for 3D
cols_pub = ['index', 'XCOORD', 'YCOORD', 'ZCOORDB', 'ORIGNAME', 'NAMEPUB',
       'SHORTNAME', 'BOHREDAT', 'BOHRTYP', 'GRUND', 'RESTRICTIO', 'TIEFEMD',
       'DEPTHFROM', 'DEPTHTO', 'LAYERDESC', 'ORIGGEOL', 'LITHOLOGY',
       'LITHOSTRAT', 'CHRONOSTR', 'TECTO', 'USCS1', 'USCS2', 'USCS3',
       'geometry','geom4326', 'x4326', 'y4326']

# Columns names for 3D export
export_pub_cols = ["bh_pub_index", "bh_pub_XCOORD","bh_pub_YCOORD","bh_pub_ZCOORDB",
                   "bh_pub_ORIGNAME","bh_pub_NAMEPUB","bh_pub_SHORTNAME", 
                   'bh_pub_BOHREDAT',"bh_pub_BOHRTYP", 'bh_pub_GRUND',"bh_pub_RESTRICTIO",
                   "bh_pub_TIEFEMD","bh_pub_DEPTHFROM","bh_pub_DEPTHTO",'bh_pub_LAYERDESC',
                   'bh_pub_ORIGGEOL',"bh_pub_LITHOLOGY", "bh_pub_LITHOSTRAT", 
                   'bh_pub_CHRONOSTR', 'bh_pub_TECTO', 'bh_pub_USCS1', 'bh_pub_USCS2', 
                   'bh_pub_USCS3','bh_pub_geometry', 'bh_pub_geom4326', 'bh_pub_x4326', 
                   'bh_pub_y4326']

export_pri_cols = ["bh_pri_index", "bh_pri_XCOORD","bh_pri_YCOORD","bh_pri_ZCOORDB",
                   "bh_pri_ORIGNAME","bh_pri_NAMEPUB","bh_pri_SHORTNAME", 
                   'bh_pri_BOHREDAT',"bh_pri_BOHRTYP", 'bh_pri_GRUND',"bh_pri_RESTRICTIO",
                   "bh_pri_TIEFEMD","bh_pri_DEPTHFROM","bh_pri_DEPTHTO",'bh_pri_LAYERDESC',
                   'bh_pri_ORIGGEOL',"bh_pri_LITHOLOGY", "bh_pri_LITHOSTRAT", 
                   'bh_pri_CHRONOSTR', 'bh_pri_TECTO', 'bh_pri_USCS1', 'bh_pri_USCS2', 
                   'bh_pri_USCS3','bh_pri_geometry', 'bh_pri_geom4326', 'bh_pri_x4326', 
                   'bh_pri_y4326']

# Column names for 2D export
cols_2D = ["index","XCOORD","YCOORD","x4326", "y4326", "ZCOORDB","ORIGNAME","NAMEPUB",
           "SHORTNAME", 'BOHREDAT',"BOHRTYP", 'GRUND',"RESTRICTIO","TIEFEMD"]

# checkpoint
onUtils.logger_3(out_dir_run, fname=log_name, fpath=out_dir_run)
# ### Import data exported from GeODin 

# In[4]:


# Read all .xlsx-Files from source directory
in_data = glob.glob(os.path.join(in_dir_bh,'*.xlsx'))

# checkpoint
check_txt = 'Number of inputfiles detected: ' + str(len(in_data)) + str(in_data)
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# In[6]:


# Read all data and combine it into one file. Continuos index will be created 
all_data = pd.DataFrame()

for f in in_data:
    #df = pd.read_excel(f)
    df = pd.read_excel(f, date_parser=False, dtype={'BOHREDAT':str}) # IMPORTANT: deactive date paser und set BOHREDAT = str
    all_data = all_data.append(df,ignore_index=True)


# <font color=red><h1>
#     Inspect imported data >>>>></h1></font>

# In[7]:


#Check dtypes of columns
all_data[sel_cols_2].dtypes


# In[8]:


# Check individual types of BOHREDAT
bohredatTypes = all_data['BOHREDAT'].apply(type).unique()

# Check max, min of dates 
for i in bohredatTypes:

    print('Max: ', i, all_data['BOHREDAT'].loc[all_data['BOHREDAT'].apply(type) == i].unique().max())
    print('Min: ', i, all_data['BOHREDAT'].loc[all_data['BOHREDAT'].apply(type) == i].unique().min())


# In[9]:


# Define valide date range
startD = '1700-01-01'
endD = '2200-01-01'


# In[10]:


# Replace wrong values and values out of bound
all_data['BOHREDAT_1'] = all_data['BOHREDAT'].apply(lambda x: '1968-06-17' if str(x) == '17.06.1668' else ('1700-01-01' if str(x) < startD else ('2200-01-01' if str(x) > endD else x)))


# In[11]:


# Check max and min values
all_data[['BOHREDAT', 'BOHREDAT_1']].loc[(all_data['BOHREDAT'] > '9000') |(all_data['BOHREDAT'] < '1700')].sort_values(by='BOHREDAT')


# In[12]:


# convert column to datetime
all_data['BOHREDAT_1'] = pd.to_datetime(all_data['BOHREDAT_1'], infer_datetime_format=True, dayfirst=True, errors='raise')


# In[13]:


# overwrite column
all_data['BOHREDAT'] = all_data['BOHREDAT_1']


# In[14]:


all_data[sel_cols_2].dtypes

# checkpoint
check_txt = 'all_data: ', all_data.shape
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# In[15]:


# Plot x-coordnates vs. y-coordinates 
get_ipython().run_line_magic('matplotlib', 'inline')

x = all_data['XCOORD']
y = all_data['YCOORD']

plt.plot(x, y, '+', color='black');


# In[16]:


# Plot depth distribution of boreholes 
plt.hist(all_data['TIEFEMD'], label='TIEFEMD', log=True, histtype='bar', edgecolor='black',  color='green')


# # Statistics
# ### Count unique boreholes and layers
# 

# In[17]:


# Create some simple statistics
num_bh = len(all_data['SHORTNAME'].unique())
num_layers = all_data.shape[0]
print('Number of individual borehole: ', num_bh)
print('Number of individual layers: ', num_layers)

# calculate number of layers per borehole
layer_per_bh = all_data.groupby('SHORTNAME')['DEPTHFROM'].nunique()
print(layer_per_bh.describe())

# checkpoint
check_txt = 'Number of individual borehole: ', num_bh, '; Number of individual layers: ', num_layers
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# # Preprocessing raw data
# ### Sort data

# In[18]:


# Sort data by "SHORTNAME" and "DEPTHFROM"
all_data_sorted = all_data.sort_values(by=["SHORTNAME", "DEPTHFROM"])
print('Shape of data set: ', all_data_sorted.shape)
all_data_sorted[["SHORTNAME","RESTRICTIO", "DEPTHFROM", "DEPTHTO", "TIEFEMD"]].head(20)

# checkpoint
check_txt = 'all_data_sorted: ', all_data_sorted.shape
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# ### Create index

# In[19]:


# Create an index column
all_data_sorted['index'] = all_data_sorted.index
print('Shape of data set: ', all_data_sorted.shape)
all_data_sorted[["index", "SHORTNAME","RESTRICTIO", "DEPTHFROM", "DEPTHTO", "TIEFEMD"]].head(20)

# checkpoint
check_txt = 'all_data_sorted with index: ', all_data_sorted.shape
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# ### Clean columns

# In[20]:


# Round data
#df['DataFrame column'].round(decimals=number of decimal places needed)
all_data_sorted['XCOORD'] = all_data_sorted['XCOORD'].round(decimals=2)
all_data_sorted['YCOORD'] = all_data_sorted['YCOORD'].round(decimals=2)
all_data_sorted['ZCOORDB'] = all_data_sorted['ZCOORDB'].round(decimals=2)
all_data_sorted['TIEFEMD'] = all_data_sorted['TIEFEMD'].round(decimals=2)
all_data_sorted['DEPTHFROM'] = all_data_sorted['DEPTHFROM'].round(decimals=2)
all_data_sorted['DEPTHTO'] = all_data_sorted['DEPTHTO'].round(decimals=2)


# In[21]:


# Check rounding
all_data_sorted[sel_cols].select_dtypes(include=['float64'])


# In[22]:


all_data_sorted.head()


# <font color=red><h1>
#     Export raw data to file >>>>><a id="linkxy"></a></h1></font>

# In[23]:


# Export all data to csv

bh_raw_file = '_'.join(['bh_raw', str(now), str(run_num).zfill(2),]) +'.csv'
bh_raw_path = os.path.join(out_dir_run,bh_raw_file)
all_data_sorted.to_csv(bh_raw_path,index=None, sep=';')

# checkpoint
check_txt = 'all_data_sorted exported to: ', bh_raw_path
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# # Preprocessing PRIVATE data

# ### Catch all columns and column numbers in dict
# This shall help to easily see which cloumn is mentioned in warnings

# In[ ]:


#10,13,17,18,20,71,100


# In[24]:


# copy all columns name to list "cols"
cols = all_data_sorted.columns.to_list()

# Create a dictionry of column names and locations
col_dicts = {}

keys = len(cols)
values = cols

for i in range(keys):
        col_dicts[i] = values[i]

print(col_dicts)


# In[25]:


# Check the shape (rows, columns) of the combined files
all_data_sorted.shape


# ### Checking for duplicated rows  and eliminate them

# In[26]:


# Create a list of columns except the index column, in order to use it as a subset for finding duplicate rows
cols_2 = cols[0:-1]


# In[27]:


# Find duplicate rows (checking duplicates based on all columns)
dup_rows = all_data_sorted[all_data_sorted.duplicated(subset=cols_2)]
print("Duplicate Rows except first occurrence based on all columns are :", dup_rows['LONGNAME'].count())

#Show duplicate entries if exisiting
if len(dup_rows) > 0:
    dup_rows.head()
else:
    pass

# checkpoint
check_txt = "Duplicate Rows except first occurrence based on all columns are :", dup_rows['LONGNAME'].count()
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# In[28]:


# Drop all duplicated rows and save result to "all_data_unique"
if len(dup_rows) > 0:
    all_data_unique = all_data_sorted.drop_duplicates(subset=cols_2)
    print(len(dup_rows), " dropped")
    print("shape all_data_unipue: ", all_data_unique.shape)
    print("shape all_data_sorted: ", all_data_sorted.shape)
else:
    all_data_unique = all_data_sorted
    print("No rows dropped")
    #print("shape all_data_unipue: ", all_data_unique.shape)
    print("shape all_data_sorted: ", all_data_sorted.shape)

# checkpoint
check_txt = dup_rows['LONGNAME'].count(), "rows dropped"
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# ### Select relevant columns
# Columns are defined in section ["Configuration"](#linkConfig)

# In[29]:


# Select only relevant columns and save into "all_data_unique_sel"
all_data_unique_sel = all_data_unique[sel_cols]

# For entire data set with all columns: Save all into "all_data_unique_sel"
#all_data_unique_sel = all_data_unique


# In[30]:


all_data_unique_sel.head(5)

# checkpoint
check_txt =  "Columns selected: ", sel_cols
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# In[ ]:





# # <font color='red'> > Create GDF for all data PRIVATE data</font>

# In[31]:


# Convert dataframe "all_data_unique_sel" to geodataframe "gdf" and set inital crs to epsg:2056 
geom = [Point(xy) for xy in zip(all_data_unique_sel.XCOORD, all_data_unique_sel.YCOORD)]
crs = {"init" : "epsg:2056"}
private_bh = gpd.GeoDataFrame(all_data_unique_sel, crs=crs, geometry=geom)


# In[32]:


# Check gdf
private_bh.head()
#private_bh.shape

# checkpoint
check_txt =  "GDF create for PRIVATE BH with shape: ", private_bh.shape
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# # Plot GDF

# In[33]:


# Load swiss boundary from shapefile
ch_perimeter = gpd.read_file('./data/input/helper/swissBOUNDARIES3D_1_3_TLM_LANDESGEBIET.shp')


# In[34]:


# Select only swiss perimeter
ch_perimeter = ch_perimeter[ch_perimeter['ICC'] == 'CH']
ch_perimeter


# In[35]:


# Create buffer around CH-Perimeter
ch_peri_buf_10km = ch_perimeter.buffer(20000) # 20km


# In[36]:


# Plot GeoDataFrame together with swiss boundary 
base = ch_perimeter.plot(color='white', edgecolor='black')
lyr_1 = ch_peri_buf_10km.plot(ax=base, edgecolor='blue', facecolor='none')
private_bh.plot(ax=lyr_1, color='red', markersize=5);


# ### CLIP GDF to swiss boundary

# In[ ]:


# Clip the data using GeoPandas clip
gdf_clip = gpd.clip(gdf, ch_perimeter)

# checkpoint
check_txt =  "GDF clipped to swiss boundary"
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# ### Reproject EPSG:2056 to EPSG:4326

# In[37]:


#Write re-projected coordinates into new column
#gdf_trans = gdf
private_bh["geom4326"] = private_bh["geometry"].to_crs("epsg:4326")

private_bh["x4326"] = private_bh["geom4326"].apply(lambda p: p.x)
private_bh["y4326"] = private_bh["geom4326"].apply(lambda p: p.y)

private_bh.shape


# In[38]:


private_bh.head()

# checkpoint
check_txt =  "GDF re-projected: ", 
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# In[39]:


private_bh.shape


# In[40]:


# Rename columns according to conventions
private_bh.columns = export_pri_cols
private_bh.head()


# ### Use private_bh as basis for creating OPEN data set and 2D data set

# # <font color='red'> Export PRIVATE data to file >>>>> </font>

# In[41]:


# Export PRIVATE data to csv
#all_data_sorted.to_csv("./data/output/Schichtdaten/bh_raw_201109.csv",index=None)
bh_private_file = '_'.join(['bh_private', str(now), str(run_num).zfill(2),]) +'.csv'
bh_private_path = os.path.join(out_dir_run,bh_private_file)
private_bh.to_csv(bh_private_path,index=None, sep=';')

# checkpoint
check_txt = 'PRIVATE boreholes exported to: ', bh_private_path
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# # Preprocessing data for OPEN dataset
# ### Introduce columns "start" and "end" to to store start and end depth of entire borehole to each row 

# In[42]:


# Reset columns names to original
private_bh.columns = cols_pub
private_bh.head()


# In[43]:


private_bh.shape


# In[44]:


# create new columns "start" and "end" and fill it with start and end depth
private_bh['start'] = private_bh.groupby('SHORTNAME')['DEPTHFROM'].transform('min')
private_bh['end'] = private_bh.groupby('SHORTNAME')['DEPTHTO'].transform('max')

# show head
private_bh.sort_values(by=["SHORTNAME", "DEPTHFROM"]).head(10)

# checkpoint
check_txt = 'Columns "start" and "end" added.', private_bh.columns
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# ### Split layer based on restriction level
# Restriction level:
# * g = restricted
# * b = restricted until date specified
# * f = free, not restricted

# In[45]:


# Select row which have "RESTRICTIO" == "g"
# Select row which have "RESTRICTIO" == "f"
# Select row which have "RESTRICTIO" == "b"

df_g = private_bh.loc[private_bh["RESTRICTIO"] == "g"].sort_values(by=["SHORTNAME", "DEPTHFROM"])
df_f = private_bh.loc[private_bh["RESTRICTIO"] == "f"].sort_values(by=["SHORTNAME", "DEPTHFROM"])
df_b = private_bh.loc[private_bh["RESTRICTIO"] == "b"].sort_values(by=["SHORTNAME", "DEPTHFROM"])

# Sum of all rows from df_g, df_b, df_f
df_sum = df_g.shape[0] + df_b.shape[0] + df_f.shape[0]

print("All unique data: ",private_bh.shape)
print("Restricted unique data: ", df_g.shape)
print("Restricted until unique data: ", df_b.shape)
print("Non-restricted unique data: ", df_f.shape)
print("Restricted + restircted until + Non-restricted data: ", df_sum)
print("Difference between all unique data and restriceted + Non-restricted: ", private_bh.shape[0] - df_sum)


# In[46]:


# delete duplicates in df_g
df_g_unique = private_bh.loc[private_bh["RESTRICTIO"] == "g"].sort_values(by=["SHORTNAME", "DEPTHFROM"]).drop_duplicates("SHORTNAME")
print('df_g_unique: ', df_g_unique.shape)

# delete duplicates in df_b
df_b_unique = private_bh.loc[private_bh["RESTRICTIO"] == "b"].sort_values(by=["SHORTNAME", "DEPTHFROM"]).drop_duplicates("SHORTNAME")
print('df_b_unique: ', df_b_unique.shape)


# In[47]:


df_g_unique.head()

# checkpoint
check_txt = "All unique data: ",private_bh.shape, '; "g" unique data: ', df_g.shape, '; "b" unique data: ', df_b.shape, '; "f" unique data: ', df_f.shape, '; Difference: ', private_bh.shape[0] - df_sum 
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# In[48]:


# Append df_b to df_g, so that all restriced data are in one dataframe
df_g_unique = df_g_unique.append(df_b_unique)

# checkpoint
check_txt = "All restricted unique data combined: ",private_bh.shape, '; "g" unique data: ', df_g.shape, '; "b" unique data: ', df_b.shape, '; "f" unique data: ', df_f.shape, '; Difference: ', private_bh.shape[0] - df_sum 
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# In[49]:


df_g_unique.shape


# ### Replace layer details with undefined values

# In[50]:


# Overwrite "DEPTHFROM" and "DEPTHTO" with "start" and "end", respectively
df_g_unique["DEPTHFROM"] = df_g_unique["start"]
df_g_unique["DEPTHTO"] = df_g_unique["end"]

# Overwrite "LAYERDESC" of restricted boreholes ("RESTRICTIO = "g) with "Undefined"
df_g_unique[["LAYERDESC", "ORIGGEOL", "ORIGNAME", "BOHRTYP", "CHRONOSTR", "LITHOLOGY", "LITHOSTRAT"]] = "Undefined"

# checkpoint
check_txt = "Layer details replaced with undefined values " 
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# ### Combine free and restricted data into one

# In[51]:


# Combine the two dataframe df_g and df_f
frames = [df_g_unique, df_f]
open_bh = pd.concat(frames)

# Drop the columns "start" and "end"
open_bh = open_bh.drop(["start", "end"], axis=1)


# In[52]:


# Sort dataset by unique-ID "SHORTNAME" and "DEPTHFROM"
open_bh = open_bh.sort_values(by=["SHORTNAME", "DEPTHFROM"])

# checkpoint
check_txt = "Data sets re-combined, rows sorted by 'SHORTNAME' and 'DEPTHFROM'." 
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# In[53]:


open_bh.shape


# In[54]:


open_bh['SHORTNAME'].nunique()

# checkpoint
check_txt = "Open data created: ", open_bh['SHORTNAME'].nunique()
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# In[55]:


open_bh.columns = export_pub_cols
open_bh.head()


# # <font color='red'> Export OPEN data </font>

# In[56]:


# Export PRIVATE data to csv
#all_data_sorted.to_csv("./data/output/Schichtdaten/bh_raw_201109.csv",index=None)
bh_open_file = '_'.join(['bh_open', str(now), str(run_num).zfill(2),]) +'.csv'
bh_open_path = os.path.join(out_dir_run,bh_open_file)
open_bh.to_csv(bh_open_path,index=None, sep=';')

# checkpoint
check_txt = 'OPEN boreholes exported to: ', bh_open_path
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# # Prepocessing 2D Data
# ### Create 2D data set by aggregating records by "SHORTNAME", each record becomes one borehole

# In[57]:


# Reset columns names to orginal
open_bh.columns = cols_pub
open_bh.head()


# In[58]:


# Drop all duplicated record based on unique-ID "SHORTNAME" apart from first record

bh_2d = open_bh.drop_duplicates(subset=["SHORTNAME"], keep="first")


# In[59]:


bh_2d.shape


# In[60]:


bh_2d.head()

# checkpoint
check_txt = 'All duplicated rows with same "SHORTNAME" deleted: '
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# ### Select only relevant columns for 2D dataset

# In[61]:


# Select only relvant columns and save it back into "df_all_unique"
#df_all_unique = df_all_unique[["index","XCOORD","YCOORD","ZCOORDB","ORIGNAME","NAMEPUB","SHORTNAME", 'BOHREDAT',"BOHRTYP", 'GRUND',"RESTRICTIO","TIEFEMD"]]
bh_2d = bh_2d[cols_2D]

# checkpoint
check_txt = 'Relevant columns for 2D-data selected', bh_2d.columns
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# ### Create new Atribute for Link to swissgeol

# In[62]:


#Define parameter 
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
#df_all_unique['link'] = baseURL + layer_key + layer_value + para_sep + layer_vis + layer_vis_value + para_sep + layer_trans + layer_trans_value + para_sep + link_key + df_all_unique['x4326'].map(str) + link_sep + df_all_unique['y4326'].map(str) +  link_sep + df_all_unique['ZCOORDB'].map(str)
bh_2d['link'] = baseURL + layer_key + layer_value + para_sep + layer_vis + layer_vis_value + para_sep + layer_trans + layer_trans_value + para_sep + link_key + bh_2d['x4326'].map(str) + link_sep + bh_2d['y4326'].map(str) +  link_sep + '0'

bh_2d.head(5)

# checkpoint
check_txt = 'Link to 3D-object created'
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# In[63]:


print(bh_2d['link'][0])


# In[64]:


#sort how many unique record are in the dataset

bh_2d = bh_2d.sort_values(by=["SHORTNAME"])
bh_2d.shape


# # <font color='red'> Export 2D data </font>

# In[65]:


# Export PRIVATE data to csv

bh_2d_file = '_'.join(['bh_2D', str(now), str(run_num).zfill(2),]) +'.csv'
bh_2d_path = os.path.join(out_dir_run,bh_2d_file)
bh_2d.to_csv(bh_2d_path,index=None)

# checkpoint
check_txt = '2D-data exported \n ------------------------'
onUtils.logger_3(check_txt, fname=log_name, fpath=out_dir_run)
# In[ ]:




