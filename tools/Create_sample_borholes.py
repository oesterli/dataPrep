#!/usr/bin/env python
# coding: utf-8

# Import libraries
import pandas as pd

# Load data
#sampleBH = pd.read_csv('<<PATH_TO_YOUR_BORHOLES>>.csv', parse_dates=['<<YOUR_DATE_COLUMN_NAME>>'], infer_datetime_format=True, sep=';')
sampleBH = pd.read_csv('/Volumes/ONNAS_Space/Nils/03_IT/__MyWorkspaces/python_space/bh_prep/data/output/run_20210201_00/bh_open_20210201_00.csv', parse_dates=['bh_pub_BOHREDAT'], infer_datetime_format=True, sep=';')

# Check dtypes
sampleBH.shape
sampleBH.dtypes

# Define list of boreholes to be selected
#bh_list = ['<<YOUR_BORHOLE_1>>', '<<YOUR_BORHOLE_2>>', '<<YOUR_BORHOLE_x>>']
bh_list = ['I95RV03900', 'AUE4GYC800', '4VE4GYC800', 'UVE4GYC800', 'LWE4GYC800', 'DXE4GYC800', '5YE4GYC800']

bh_list.sort()
bh_list

# Check SHORTNAMES
#sampleBH[['<<YOUR_BORHOLE_ID>>', '<<YOUR_BOREHOLE_NAME>>','<<YOUR_BOREHOLE_DEPTH>>']].loc[sampleBH['<<YOUR_BORHOLE_ID>>'].isin(bh_list)]['<<YOUR_BORHOLE_ID>>'].unique()
sampleBH[['bh_pub_SHORTNAME', 'bh_pub_ORIGNAME','bh_pub_TIEFEMD']].loc[sampleBH['bh_pub_SHORTNAME'].isin(bh_list)]['bh_pub_SHORTNAME'].unique()

# Write selected boreholes to export DataFrame
#sampleBH_export = sampleBH.loc[sampleBH['<<YOUR_BORHOLE_ID>>'].isin(bh_list)]
sampleBH[['bh_pub_SHORTNAME', 'bh_pub_ORIGNAME', 'bh_pub_NAMEPUB', 'bh_pub_RESTRICTIO']]

# Export DataFrame to csv
# Write selected boreholes to export DataFrame
#sampleBH_export = sampleBH.loc[sampleBH['<<YOUR_BORHOLE_ID>>'].isin(bh_list)]
sampleBH_export = sampleBH.loc[sampleBH['bh_pub_SHORTNAME'].isin(bh_list)]

#sampleBH_export.to_csv('<<YOUR_PATH/>>sampleBH.csv',index=None, sep=';')
sampleBH_export.to_csv('/Users/oesterli/Documents/_temp/bhPrep/scr/data/input/bh/sampleBH.csv',index=None, sep=';')

# Make 2D data set
#sampleBH2D = sampleBH_export.drop_duplicates('<<YOUR_BORHOLE_ID>>', keep='first')
sampleBH2D = sampleBH_export.drop_duplicates('bh_pub_SHORTNAME', keep='first')

sampleBH2D.shape

# Show 2D data set
sampleBH2D

# Export 2D data set to csv
#sampleBH2D.to_csv('<<YOUR_PATH/>>sampleBH_2D.csv',index=None, sep=';')
sampleBH2D.to_csv('/Users/oesterli/Documents/_temp/bhPrep/scr/data/input/bh/sampleBH_2D.csv',index=None, sep=';')
