from geopandas import read_file
import fiona

def readGpkg(source):
	#data = read_file(source)

	with fiona.Env(OGR_GPKG_FOREIGN_KEY_CHECK='NO'):
		data = fiona.open(source)

	print('Geopackage read')
	print('Rows: ', data.shape[0])
	print('Columns: ', data.shape[1])

def readShapefile(source):
	data = read_file(source)
	print('Shapefile read')
	print('Rows: ', data.shape[0])
	print('Columns: ', data.shape[1])

def readCsv(source):
	data = read_file(source)
	print('CSV read')
	print('Rows: ', data.shape[0])
	print('Columns: ', data.shape[1])

	return data
