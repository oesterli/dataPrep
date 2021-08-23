import os
import sys
import datetime
import json

with open("/Users/oesterli/Documents/_temp/bhPrep/work/config.json",) as file:
    conf = json.load(file)

now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Define log_file path and name
fname = "log" + "_" + now + ".txt"
log_file = os.path.join(conf["out_dir"],fname)

def loggerX(logFile, text):
    with open(logFile, 'a') as f:
        print(now, text, sep=';', file=f)

    # print date, time and message to stdout
    print(now, text, log_file)
    return

loggerX(log_file, "MESSAGE")