'''Builds script for class that will pull a record from a feature class or a
table and pass the entire record as an object. Update the dataset variable to
your path, run, copy the output to your module, give it a try. Change properties
as needed.

Using an object makes writing scripts that have to use values in a lot of places
and that may change frequently easier because the field is always accessible
using type ahead. No need for cumbersome field lists, cursors, and indexes.
Just pass a key (globalid in this version) when instantiating the class to get
the record, then get values using <objectvariablename>.<fieldname>'''

import arcpy

# dataset to build record level class for (must be in a geodatabase)
dataset = r'D:\yourgeodatabase.gdb\yourfeatureclassortable'

# fields to skip - built for postgres - would need to update this for file gdb
skipList = ['objectid', 'shape', 'st_area(shape)', 'st_length(shape)']

# get the fields to add
fieldList = arcpy.ListFields(dataset)

# describe the dataset object
datasetDesc = arcpy.Describe(dataset)

# handle differently if it is a table
isTable = False
if datasetDesc.dataType == 'Table':
    isTable = True

# get the name of the dataset to use for the class name
datasetShortName = datasetDesc.baseName[14:]

# make it pretty for the comment
datasetFormalName = ' '.join(datasetShortName.split("_")).title()

# start class
classScript = ''
if isTable:
    classScript += "class cls_{0}:\n".format(datasetShortName)
else:
    classScript += "class cls_{0}:\n".format(datasetShortName[:-1])
classScript += "    '''{0} record.'''\n".format(datasetFormalName)
classScript += "    def __init__(self, globalId = ''):\n"
classScript += "        self.globalIdExists = False\n"
if isTable:
    classScript += "        self.path = os.path.join(db, tbPref+'{0}')\n".format(datasetShortName)
else:
    classScript += "        self.path = os.path.join(db, fd, tbPref+'{0}')\n".format(datasetShortName)
classScript += "        self.where = \"globalid = '\"+globalId+\"'\"\n"
classScript += "        self.fieldList = [\n"

# build self.fieldList
for field in fieldList:
    if field.baseName not in skipList:
        classScript += "            '{0}',\n".format(field.baseName)

# add shape if feature class
if isTable:
    # drop the last comma and add a line return
    classScript = classScript[:-2]
    classScript += "\n"
else:
    # add shape
    classScript += "            'SHAPE@'\n"

# close braces on the field list
classScript +=  "             ]\n"

# build each property
for field in fieldList:
    if field.baseName not in skipList:
        if field.baseName[-4:] == "date":
            classScript += "        self.{0} = datetime.datetime(1900,1,1,0,0,0)\n".format(field.baseName)
        elif field.baseName == "globalid":
            classScript += "        self.{0} = ''\n".format(field.baseName)
        elif field.type in ["Double", "SmallInteger"]:
            classScript += "        self.{0} = 0\n".format(field.baseName)
        else:
            classScript += "        self.{0} = ''\n".format(field.baseName)

if isTable:
    pass
else:
    classScript += "        self.shape = None\n"

classScript += "        with arcpy.da.SearchCursor(self.path, self.fieldList, self.where) as scur:\n"
classScript += "            for srow in scur:\n"
classScript += "                self.globalIdExists = True\n"

# build each property
index = 0
for field in fieldList:
    if field.baseName not in skipList:
        classScript += "                self.{0} = jmr_helpers.passNull(srow[{1}], self.{0})\n".format(field.baseName, str(index))
        index += 1

if isTable:
    pass
else:
    classScript += "                self.shape = srow[{0}]".format(str(index))

print classScript


