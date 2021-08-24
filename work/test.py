import pandas as pd
import json
import bhUtils

with open("/Users/oesterli/Documents/_temp/bhPrep/scr/config.json",) as file:
    conf = json.load(file)
source_file = conf["source_gpkg"]
out_data = bhUtils.singleDataLoader(source_file)

print(out_data.head(5))

print(out_data.info(verbose=True))

test = str(out_data.info(verbose=True))

print(test)