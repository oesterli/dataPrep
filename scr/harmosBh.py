# Harmonization of bh data

import datetime
import glob
import json
#################################
## IMPORTS
#################################
import os

import pandas as pd

## Load Configuration
################################
with open(r"C:\Projects\bhPrep\scr\config.json", ) as file:
    conf = json.load(file)

sourceData = "C:\\Projects\\bhPrep\\scr\\data\\input\\bh"
sourceSearch = "C:\\Projects\\bhPrep\\scr\\data\\input"
outDir = "C:\\Projects\\bhPrep\\scr\\data\\output"
ext1 = "*.xlsx"
ext2 = ".csv"
enc = conf["file_encoding"]
nowExport = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

## Read File and create DataFrame based on input data
################################
multiData = pd.DataFrame()
files = glob.glob(os.path.join(sourceData, ext1))

for f in files:
    df = pd.read_excel(f)
#     multiData = multiData.append(df, ignore_index=True, sort='false')
# print(files, multiData)

## simple harmonization function
################################
## Searchlist
searchList = glob.glob(os.path.join(sourceSearch, ext1))
for s in searchList:
    sf = pd.read_excel(s)

searchList = pd.concat([sf['SEARCH_DE'], sf['SEARCH_FR'], sf['SEARCH_IT']], axis=0, ignore_index=False)
searchList = searchList.dropna()                          # delete empty cells
searchList = searchList.reset_index(drop=True)            # reset index from 0 .. i
# searchList = searchList.astype(str)
print(searchList)

## Create new column with empty list
df['myLitho'] = [[] for _ in range(df.shape[0])]
# print(searchList[0])

for i in range(len(searchList)):
    print('----', i)
    ## write indices of selected rows into list
    idx = df.loc[df['LAYERDESC'].str.contains(searchList[i], case=False, regex=False)].index.tolist()
    print('indices of ', searchList[i], ' : ', idx)

    ## Loop over list of indices of selected rows
    for j in idx:
        df.loc[j, 'myLitho'].append(searchList[i])

## Printing output
print(df)


## Save output as excel file
def exporter(outDir, outFname, expData, enc):
    outFile = os.path.join(outDir, '_'.join([outFname, str(nowExport).zfill(2), ]) + ext2)
    expData.to_csv(outFile, index=None, sep=';', encoding=enc)


exporter(outDir, 'sorted_table', df, enc)
