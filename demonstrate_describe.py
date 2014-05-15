#-------------------------------------------------------------------------------
# Name:        demonstrate_describe.py
#
# Purpose:     Take a look at how to interact with the arcpy.describe
#              function.  This example is for a file geodatabase, but
#              you can use Describe to examine the properties of lots
#              of different kinds of ESRI objects, like feature classes,
#              tables, workspaces, etc. Each of these different objects
#              will have different describe properties.
#
# Author:      Hal Watson (hal.watson@state.mn.us)
#
# Created:     05/15/2014
#
# Requires:    arcpy
#
# Arguments:   <path_to_esri_file geodatabse>
# For example: D:/Temp/demo.gdb
#
#-------------------------------------------------------------------------------

def main():

    import sys
    import arcpy

    # ---------- Incoming Arguments/Parameters ----------

    # If no arguments were passed from command line, print the usage and exit
    if len(sys.argv[1:]) < 1:
        print "demonstrate_describe.py <path_to_object>"
        exit(1)

    # Get the incoming argument(s)  argv[0] is the script name by default
    #                               argv[1] is first real argument/parameter
    path_to_file_geodatabase = sys.argv[1]

    # ---------------------------------------------------


    # Test to see if the object we want to describe exists

    if not arcpy.Exists(path_to_file_geodatabase):
        print "I can't find " + path_to_file_geodatabase
        exit()
    else:
        print ("I found it")


        # And if it does, create a describe object

        desc = arcpy.Describe(path_to_file_geodatabase)

        # Now print some of the Describe object's properties
        # The syntax to reference an object's property is:
        #    object_name.property_name

        if hasattr(desc, "name"):
            print "Name:        " + desc.name
        if hasattr(desc, "dataType"):
            print "DataType:    " + desc.dataType
        if hasattr(desc, "catalogPath"):
            print "CatalogPath: " + desc.catalogPath


        # Let's see if there are any children (children is a property
        # that contains a list of the child objects).
        # We'll examine each child using a for loop, determine if it
        # is a featurclass, and if so, print the child name and shapeType

        print "Children:"
        for child in desc.children:
            if child.dataType == "FeatureClass":
                print "    " +  child.name + ", " + child.shapeType




if __name__ == '__main__':
    main()
