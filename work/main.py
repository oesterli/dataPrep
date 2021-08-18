# Main Program

import testDataloader

# define source
file = "../scr/data/input/bh/sf/bdms-export-20210818140036/swissforages.gpkg"
#file = "../scr/data/input/bh/sf/export-20210818141348/export-20210818141348.shp"
#file ="../scr/data/input/bh/sf/full-export-20210818140828.csv"

source_file = file

if source_file.lower().endswith('.gpkg'):
	print('This is a Geopackage')
	testDataloader.readGpkg(source_file)

elif source_file.lower().endswith('.shp'):
	print('This is a Shapefile')
	testDataloader.readShapefile(source_file)

elif source_file.lower().endswith('.csv'):
	print('This is a csv')
	testDataloader.readCsv(source_file)
else:
	print('Unknown file format')

print('DONE')
