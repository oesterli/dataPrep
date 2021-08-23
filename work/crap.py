# # Oracle connection
# import cx_Oracle
# ip = 'XX.XX.X.XXX'
# port = YYYY
# SID = 'DW'
# dsn_tns = cx_Oracle.makedsn(ip, port, SID)
#
# connection = cx_Oracle.connect('BA', 'PASSWORD', dsn_tns)
#
# import cx_Oracle
# ip = 'XX.XX.X.XXX'
# port = YYYY
# SID = 'DW'
# dsn_tns = cx_Oracle.makedsn(ip, port, SID)
#
# connection = cx_Oracle.connect('BA', 'PASSWORD', dsn_tns)
#
# #df_ora = pd.read_sql('SELECT* FROM TRANSACTION WHERE DIA_DAT>=to_date('15.02.28 00:00:00',  'YY.MM.DD HH24:MI:SS') AND (locations <> 'PUERTO RICO' OR locations <> 'JAPAN') AND CITY='LONDON'', con=connection)
# df_ora = pd.read_sql('SELECT * FROM tableName WHERE search criterium' , con=connection)
#
#
#
# # Read geographic data
# https://github.com/Toblerity/Fiona
#
# https://gis.stackexchange.com/questions/342855/reading-geopackage-geometries-in-python
#
#
# import geopandas as gpd
# data = gpd.read_file("path.mygeopackage.gpkg")
# data.head()  # Prints the first 5 rows of the loaded data to see what it looks like.
#
#
# # READ JSON
# import json
# with open("/Users/oesterli/Documents/_temp/bhPrep/work/config.json",) as file:
#     conf = json.load(file)

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

data = pd.read_csv('/Users/oesterli/Documents/_temp/bhPrep/work/data/out/bh_raw_2021-08-23_08-26-51.csv', sep=';')
print(data.shape)

geom = [Point(xy) for xy in zip(data.XCOORD, data.YCOORD)]
private_bh = gpd.GeoDataFrame(data, crs=2056, geometry=geom)

#print(private_bh.shape)
print("Initial crs: ", private_bh.crs)
#print(private_bh["geometry"].head())

private_bh["geom2056"] = private_bh["geometry"]
private_bh = private_bh.to_crs('epsg:4326')

private_bh["x4326"] = private_bh["geometry"].apply(lambda p: p.x)
private_bh["y4326"] = private_bh["geometry"].apply(lambda p: p.y)

#print(private_bh[["geometry", "x4326", "y4326"]].head())

print("Updated crs: ", private_bh.crs)

#print(private_bh.info(verbose=True))

newCrsColumn = "geom" + private_bh.crs.to_string().split(':')[1]
print(newCrsColumn)

