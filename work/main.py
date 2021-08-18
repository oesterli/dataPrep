# Main Program

from IPython.display import display
from IPython.core.display import HTML

from tabulate import tabulate
import testDataloader

# define source
#file = "../scr/data/input/bh/sf/bdms-export-20210818194918/swissforages.gpkg"
file = "../scr/data/input/bh/sf/export-20210818194900/export-20210818194900.shp"
#file ="../scr/data/input/bh/sf/full-export-20210818194900.csv"

source_file = file

if source_file.lower().endswith('.gpkg'):
	print('This is a Geopackage')
	testDataloader.readGpkg(source_file)

elif source_file.lower().endswith('.shp'):
	print('This is a Shapefile')
	rawData = testDataloader.readShapefile(source_file)

elif source_file.lower().endswith('.csv'):
	print('This is a csv')
	rawData = testDataloader.readCsv(source_file)
else:
	print('Unknown file format')

print('DONE')

print(rawData.columns)

for c in rawData["ORIGINAL_N"]:
	display(c)
#HTML(rawData.to_html())
#HTML(rawData.head(2).to_html())
#rawData.style
#print(tabulate(rawData, headers = 'keys', tablefmt = 'psql'))