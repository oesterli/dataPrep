# Mapping swissforage.ch export file


#################################
## IMPORTS
#################################
import os
import datetime
import glob
import json
import geopandas as gpd
import pandas as pd

## Load Configuration
################################
my_directory = r"C:\Projects\dataPrep"

sourceFolder = os.path.join(my_directory, r"scr\swissforagePrep\data\input")
print(sourceFolder)
outDir = os.path.join(my_directory, r"scr\bhPrep\data\input")
extension = "*.csv"
enc = "utf-8"

## Read File
################################
multiData = pd.DataFrame()
files = glob.glob(os.path.join(sourceFolder, extension))
print(files)
for f in files:
    df = gpd.read_file(f)
    multiData = multiData.append(df, ignore_index=True, sort='false')


## Rename columns
################################
df = df.rename(columns={'Koordinate E': 'XCOORD', 'Koordinate N': 'YCOORD', 'Ansatzhöhe Z [müM]': 'ZCOORDB',
                                'Originalname': 'ORIGNAME', 'Name öffentlich': 'NAMEPUB', 'id': 'SHORTNAME',
                                'Bohrende Datum': 'BOHREDAT', 'Bohrtyp': 'BOHRTYP', 'Bohrzweck': 'GRUND',
                                'Restriktion': 'RESTRICTIO', 'Tiefe (MD) [m]': 'TIEFEMD', 'depth_from': 'DEPTHFROM',
                                'depth_to': 'DEPTHTO', 'description': 'LAYERDESC', 'geology': 'ORIGGEOL',
                                'lithology': 'LITHOLOGY', 'lithostratigraphy': 'LITHOSTRAT',
                                'chronostratigraphy': 'CHRONOSTR','tectonic_unit': 'TECTO',
                                'uscs_1': 'USCS1', 'uscs_2': 'USCS2', 'uscs_3': 'USCS3'})


## Rename content
################################
df['RESTRICTIO'] = df['RESTRICTIO'].replace({'20111001': "g", '20111002': "f",'20111003': "b"})
df['BOHRTYP'] = df['BOHRTYP'].replace({'20101001': "B", '20101002': "RS",'20101003': "SS", '20101004': "a"})
df['GRUND'] = df['GRUND'].replace({'22103001': "Gtec", '22103002': "Gthe",'22103003': "belS",
    '22103004': "Hyd", '22103005': "Min", '22103006': "Roh", '22103007': "KWS", '22103008': "Nat",
    '22103009': "F", '22103010': "a", '22103011': "kA"})
df['SHORTNAME'] = "SF-" + df['SHORTNAME']


## Export data
################################
nowExport = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
outFile = os.path.join(outDir, '_'.join(["SF_mapped", str(nowExport).zfill(2), ]) + '.xlsx')
print("outfile", outFile)
df_out = pd.ExcelWriter(outFile)
df.to_excel(outFile, index=None, encoding=enc)

