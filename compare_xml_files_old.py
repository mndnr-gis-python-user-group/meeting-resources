#!/usr/bin/python
# -----------------------------------------------------------------------------
# Program: compare_xml_files.py
# Author: Zeb Thomas; zeb.thomas@state.mn.us
# Original Coding Date: 10/18/2011
#
# Descripton:   A python script that compares two xml files
#               and prints the differences
#
#  Example:
#
#      python compare_xml_files.py
#
#
# -----------------------------------------------------------------------------

import xml.etree.ElementTree as ET
import os, sys

def compareXMLfiles(file1,file2,output_location):
    # parse the xml files and extract a list of string representations of nodes for each xml file
    xml1 = ET.parse(file1)
    xml2 = ET.parse(file2)
    nodes1 = walk_xml(xml1.getroot())
    nodes2 = walk_xml(xml2.getroot())

    # compare the lists of nodes
    removed = set(nodes1) - set(nodes2)
    added = set(nodes2) - set(nodes1)
    results_string = ""

    # write the results
    if removed:
        results_string += "\nThe following elements were removed from the xml file:\n"
        for removed_item in removed:
            results_string += removed_item + "\n"
    if added:
        results_string += "\nThe following elements were added to the xml file:\n"
        for added_item in added:
            results_string += added_item + "\n"
    if not results_string:
        if compare_node_text:
            tag_text = ""
        else:
            tag_text = "tags in the"
        results_string += "\nThere is no difference between the " + tag_text + " old and new xml files\n"
    print results_string

    results_string += "\n" + file1 + " tags:\n"
    for node in nodes1:
        text_start = node.find("=")
        if text_start > 0:
            node = node[:text_start]
        results_string += node + "\n"
    results_string += "\n" + file2 + " tags:\n"
    for node in nodes2:
        text_start = node.find("=")
        if text_start > 0:
            node = node[:text_start]
        results_string += node + "\n"
    try:
        log_file = open(output_location,"w")
        log_file.write(results_string)
        log_file.close()
        print "Written to log file", output_location
    except:
        print "Invalid log file path provided.  No log file written."

# data structure = [path{attrib}=text]
# e.g. ["metadata/idinfo/citation/citeinfo/origin{}=Minnesota DNR - Division of Waters - Water Management Section"]

def walk_xml(node, path = ""):
    path = path + "/" + node.tag

    # initialize nodes list with root node
    node_string = path

    # add the attribute dictionary only if there are attributes to avoid clutter
    if node.attrib:
        node_string += str(node.attrib)

    # add the text only if there is nonblank text to avoid clutter
    if compare_node_text:
        node_text = node.text
        if node_text:
            node_text = node_text.replace(" ","").replace("\n","")
        if node_text: #if there is still text left after replacement
            node_string += "=" + node_text
    nodes = [node_string]

    # for each child node, append the nodes list from that child
    children = node.getchildren()
    if children:
        for child in children:
            nodes += walk_xml(child, path)

    return nodes

help_text = """
syntax: python compare_xml_files.py old_file.xml new_file.xml {compare_node_text = True {log_file_path}}

Setting compare_node_text to False will only check for differences between the xml tags and their attributes.

The default output location for the log file is the location of the new xml file with a .log extension.  Note that passing an invalid log file path will just prevent the log file from being written.
"""

# If arguments were passed from command line, process them
if len(sys.argv[0])==0:
    print __doc__
    exit()
else:
    if len (sys.argv[1:]) < 2:
        print "Function requires at least two arguments:"
        old_xml_file = raw_input("old XML file: ")
        new_xml_file = raw_input("new XML file: ")
    else:
        # first two arguments should be the paths for the xml files to compare
        old_xml_file = sys.argv[1]
        new_xml_file = sys.argv[2]

    if not os.path.exists(old_xml_file):
        print "Error: could not find", old_xml_file
        print help_text
        exit(1)
    if not os.path.exists(new_xml_file):
        print "Error: could not find", new_xml_file
        print help_text
        exit(1)
    if ".xml" not in old_xml_file or ".xml" not in new_xml_file:
        print "Warning: 1st two arguments should be xml files"
        print help_text

    # Argument 3 is optional. Default=True.
    # It gives the option to skip checking text differences and to focus on only the tags
    if len (sys.argv[1:]) > 2:
        arg3 = sys.argv[3]
        if arg3 in ["F","f","False","FALSE","false","n","N","NO","no","No"]:
            compare_node_text = False
        elif arg3 in ["T","t","True","TRUE","true","y","Y","YES","yes","Yes"]:
            compare_node_text = True
        else:
            print "Error: Could not decipher compare_node_text argument.  Should be boolean."
            print help_text
            exit(1)
    else:
        compare_node_text = True #default

    # Argument 4 is optional. Default=new xml file name with a .log extension.
    # This is the log file path.
    if len (sys.argv[1:]) > 3:
        output_location = sys.argv[4]
    else:
        output_location = new_xml_file.replace(".xml",".log") #default

    # Call comparison function
    compareXMLfiles(old_xml_file,new_xml_file,output_location)