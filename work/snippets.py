# Oracle connection
import cx_Oracle
ip = 'XX.XX.X.XXX'
port = YYYY
SID = 'DW'
dsn_tns = cx_Oracle.makedsn(ip, port, SID)

connection = cx_Oracle.connect('BA', 'PASSWORD', dsn_tns)

#df_ora = pd.read_sql('SELECT* FROM TRANSACTION WHERE DIA_DAT>=to_date('15.02.28 00:00:00',  'YY.MM.DD HH24:MI:SS') AND (locations <> 'PUERTO RICO' OR locations <> 'JAPAN') AND CITY='LONDON'', con=connection)
df_ora = pd.read_sql('SELECT * FROM tableName WHERE search criterium' , con=connection)



# Read geographic data
#https://github.com/Toblerity/Fiona
#https://gis.stackexchange.com/questions/342855/reading-geopackage-geometries-in-python


################################
## Load Configuration
################################
with open("/Users/oesterli/Documents/_temp/bhPrep/work/conf_test.json",) as file:
    conf = json.load(file)

## Specify variables
now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

print(conf["bsp_key"])
print(conf["test_data"]["index"]["meta"])


for (k, v) in conf.items():
   print("Key: " + k)
   print("Value: " + str(v))

# for (k, v) in conf.items():
#     if k == "test_data":
#         print("Key: " + k)
#     else:
#         print("key not found")
#



