## Import libraries
from markdownify import markdownify

## Define in and output files
inFile = r"objc_LG_GeolAssets_V1.html"
outFile = r"MY_objc_LG_GeolAssets_V1.md"

## Define search- and insert-strings
match_string = "| Name | Kardinalität | Typ | Beschreibung |\n"
insert_string = "| --- | --- | --- | --- |\n"

## Define output list
myMdList = []

##Read input file
file = open(inFile, "r").read()

## set MD-Style: styles = ["ATX", "ATX_CLOSED", "SETEXT", "UNDERLINED"]
mdStyle = "ATX"

## Convert html to md
mdText = markdownify(file, heading_style=mdStyle)

## Convert Test to List
mdList = mdText.splitlines(keepends=2)


## Insert headerlines
for l in mdList:
	#print("o: ", repr(l))

	if match_string in l:
		print("-", repr(l))
		myMdList.append(l)
		print(">", repr(insert_string))
		myMdList.append(insert_string)
	else:
		print("-", repr(l))
		myMdList.append(l)

## Write results to file
with open(outFile, "w") as of:
	of.writelines(myMdList)
