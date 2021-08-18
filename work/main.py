# Main Program

import testDataloader

# define source
#file = "../scr/data/input/bh/sf/bdms-export-20210818194918/swissforages.gpkg"
#file = "../scr/data/input/bh/sf/export-20210818194900/export-20210818194900.shp"
file ="../scr/data/input/bh/sf/full-export-20210818194900.csv"

source_file = file

if source_file.lower().endswith('.gpkg'):
	print('This is a Geopackage')
	testDataloader.readGpkg(source_file)

elif source_file.lower().endswith('.shp'):
	print('This is a Shapefile')
	testDataloader.readShapefile(source_file)

elif source_file.lower().endswith('.csv'):
	print('This is a csv')
	rawData = testDataloader.readCsv(source_file)
else:
	print('Unknown file format')

print('DONE')

