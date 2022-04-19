## REPLACEMENTS AMONG EXCEL LIST IN XML FILE

## Import
#############################################################
import lxml.etree as lxml
import xml.etree.ElementTree as et
import pandas as pd
import uuid


# ## Generating UUID
# #############################################################
# df = pd.read_excel('ReplaceList.xlsx')
# # print(df)
#
# ## Preparation of expressions to harmonize in search list
# searchList = pd.concat([df['GeolCode_alphanumeric']], axis=0, ignore_index=False)
# searchList = searchList.reset_index(drop=True)             # reset index from 0 .. i
# searchList = searchList.astype(str)
# # print(searchList)
#
# df['UUID'] = [[] for _ in range(df.shape[0])]              # creates a new column called 'UUID'
# for i in range(len(searchList)):
#     uuidList = uuid.uuid4()                                # creates uuid for each object
#     df.loc[i,'UUID'].append(uuidList)                      # appends uuid in column 'UUID'
# print(df)
# df.to_excel(r'C:\Projects\dataPrep\src\xmlPrep\ReplaceList_UUID.xlsx')

## Reading input files
#############################################################
## Read xml file
data = et.parse('GeologyModelLookUp_V3_0.xml')
root = data.getroot()

## Read excel list with (alpha-)numeric GeolCodes
df = pd.read_excel('ReplaceList_UUID.xlsx')
# print(df)


## Replace GeolCode: alphanumeric to numeric
#############################################################
df = df.set_index("GeolCode_alphanumeric")
for code in root.findall('.//GeolCode'):
    try:
        code.text = str(df.loc[code.text].GeolCode_numeric)
    except KeyError:
        pass
data.write('GeologyModelLookUp_V3.0_modified.xml')


## Replace TID: alphanumeric to UUID
#############################################################
data = lxml.parse('GeologyModelLookUp_V3.0_modified.xml')
root = data.getroot()

GeolCode = root.findall('.//GeolCode')
# print(GeolCode)
# print(len(GeolCode))

for i in range(len(GeolCode)):
    parent = GeolCode[i+0].getparent()
#     print(parent)
    try:
        parent.attrib['TID'] = df.loc[parent.attrib['TID']].UUID
    except KeyError:
        pass
data.write('GeologyModelLookUp_V3.0_modified.xml')


## Replace REF: alphanumeric to UUID
#############################################################
data = et.parse('GeologyModelLookUp_V3_0.xml')
root = data.getroot()
for element in root.findall('.//Parent'):
#    print('printing works')
    print(element.attrib)
    try:
        element.attrib['REF'] = df.loc[element.attrib['REF']].UUID
    except KeyError:
        pass
data.write('GeologyModelLookUp_V3.0_modified_b002_modified.xml')



