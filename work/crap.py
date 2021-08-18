# Oracle connection
import cx_Oracle
ip = 'XX.XX.X.XXX'
port = YYYY
SID = 'DW'
dsn_tns = cx_Oracle.makedsn(ip, port, SID)

connection = cx_Oracle.connect('BA', 'PASSWORD', dsn_tns)

import cx_Oracle
ip = 'XX.XX.X.XXX'
port = YYYY
SID = 'DW'
dsn_tns = cx_Oracle.makedsn(ip, port, SID)

connection = cx_Oracle.connect('BA', 'PASSWORD', dsn_tns)

#df_ora = pd.read_sql('SELECT* FROM TRANSACTION WHERE DIA_DAT>=to_date('15.02.28 00:00:00',  'YY.MM.DD HH24:MI:SS') AND (locations <> 'PUERTO RICO' OR locations <> 'JAPAN') AND CITY='LONDON'', con=connection)
df_ora = pd.read_sql('SELECT * FROM tableName WHERE search criterium' , con=connection)



# Read geographic data
https://github.com/Toblerity/Fiona

https://gis.stackexchange.com/questions/342855/reading-geopackage-geometries-in-python


import geopandas as gpd
data = gpd.read_file("path.mygeopackage.gpkg")
data.head()  # Prints the first 5 rows of the loaded data to see what it looks like.
