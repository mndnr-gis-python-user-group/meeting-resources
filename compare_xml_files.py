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
#      python compare_xml_files.py before.xml after.xml . False "results.log"
#
#
# -----------------------------------------------------------------------------

import xml.etree.ElementTree as ET
import os, sys

def walk_xml(node, path = ""):
    # Recursively adds each node to a node list as a string representation of the path, tag, attributes, and text
    # Each call of walk_xml create exactly one element in this list
    # data structure = [path{attrib}=text]
    # e.g. ["metadata/idinfo/citation/citeinfo/origin{}=Minnesota DNR - Division of Waters - Water Management Section"]

    path = path + "/" + node.tag

    node_string = path

    # add the attribute dictionary only if there are attributes to avoid empty {} clutter
    if node.attrib:
        node_string += str(node.attrib)

    # add the text only if there is nonblank text to avoid =None clutter
    if compare_node_text:
        node_text = node.text
        if node_text:
            node_text = node_text.strip()
        if node_text: #if there is still text left after strip
            node_string += "=" + node_text.replace("\n","").replace("  "," ")

    nodes = [node_string]

    # for each child node, append the nodes list from that child
    #children = node.getchildren() changed to be Python 2.7+ compatible
    children = list(node)
    for child in children:
        nodes += walk_xml(child, path)

    return nodes

def compareXMLfiles(file1,file2,output_location):
    # parse the xml files and extract a list of string representations of nodes for each xml file
    xml1 = ET.parse(file1)
    xml2 = ET.parse(file2)
    nodes1 = walk_xml(xml1.getroot())
    nodes2 = walk_xml(xml2.getroot())

    # compare the lists of nodes
    removed = set(nodes1) - set(nodes2)
    added = set(nodes2) - set(nodes1)

    # If we checked for node text value differences, recheck without value differences and
    # mark anything that was only a value difference as modified instead of removed and added.
    modified_file1 = {}
    modified_file2 = {}
    global compare_node_text # Required to modify global variable to recheck without values
    if compare_node_text:
        compare_node_text = False
        nodes1_no_text = walk_xml(xml1.getroot())
        nodes2_no_text = walk_xml(xml2.getroot())
        # Remove below block to keep changes in two categories (added and removed)
        removed_for_iteration = sorted(list(removed))
        added_for_iteration = sorted(list(added))
        for removed_item in removed_for_iteration:
            text_start = removed_item.find("=")
            if text_start > 0: # Found text
                tag = removed_item[:text_start]
                element_text = removed_item[text_start+1:]
            else: # No text found
                tag = removed_item
                element_text = ""
            # if there was only 1 instance of this tag in each file, we can assume this was
            # a modification and not an add/remove
            if nodes1_no_text.count(tag) == 1 and nodes2_no_text.count(tag) == 1:
                removed.remove(removed_item)
                modified_file1[tag] = element_text
            #else:
                #attributes_start = removed_item.find("{")
                #if attribute_start > 0:
        for added_item in added_for_iteration:
            text_start = added_item.find("=")
            if text_start > 0:
                tag = added_item[:text_start]
                element_text = added_item[text_start+1:]
            else:
                tag = added_item
                element_text = ""
            # if there was only 1 instance of this tag in each file, we can assume this was
            # a modification and not an add/remove
            if nodes1_no_text.count(tag) == 1 and nodes2_no_text.count(tag) == 1:
                added.remove(added_item)
                modified_file2[tag] = element_text
        # End Remove Block
    else: #for writing all tags to log file
        nodes1_no_text = nodes1
        nodes2_no_text = nodes2


    # write the results
    if added or removed or modified_file1:
        changes = "\nCHANGES\n-------\n"
        if modified_file1:
            file1_name = os.path.basename(file1)
            file2_name = os.path.basename(file2)
            change_string = "\nThe following " + str(len(modified_file1)) + " elements were MODIFIED in the xml file:\n"
            change_underline = ""
            for i in xrange(len(change_string)):
                change_underline += "-"
            changes += change_string + change_underline + "\n"
            for modified_item in modified_file1:
                changes += "Old: " + modified_item + "=" + modified_file1[modified_item] + "\nNew: " + modified_item + "=" + modified_file2[modified_item] + "\n\n"
        if not modified_file1: changes += "\n"
        if removed:
            change_string = "The following " + str(len(removed)) + " elements were REMOVED from the xml file:\n"
            change_underline = ""
            for i in xrange(len(change_string)):
                change_underline += "-"
            changes += change_string + change_underline + "\n"
            for removed_item in sorted(removed):
                changes += removed_item + "\n"
        if added:
            change_string = "\nThe following " + str(len(added)) + " elements were ADDED to the xml file:\n"
            change_underline = ""
            for i in xrange(len(change_string)):
                change_underline += "-"
            changes += change_string + change_underline + "\n"
            for added_item in sorted(added):
                changes += added_item + "\n"
        if modified_file1: changes += "\n"
        print "Modified:",len(modified_file1)
        print "Removed:",len(removed)
        print "Added:",len(added)
    else:
        changes = "\nNO CHANGES FOUND\n\n"

    print changes

    file1_tags = "\n" + file1 + " tags:\n"
    for node in nodes1_no_text:
#        text_start = node.find("=")
#        if text_start > 0:
#            node = node[:text_start]
        file1_tags += node + "\n"
    file2_tags = "\n" + file2 + " tags:\n"
    for node in nodes2_no_text:
#        text_start = node.find("=")
#        if text_start > 0:
#            node = node[:text_start]
        file2_tags += node + "\n"
    all_tags = "\nALL TAGS\n--------\n" + file1_tags + file2_tags + "\n"

    # put changes at the end of the print but beginning of the log file so that is the easiest thing to find
    #print changes

    try:
        log_file = open(output_location,"w")
        log_file.write(changes + all_tags)
        log_file.close()
        print "Written to log file", output_location
    except:
        print "Invalid log file path provided.  No log file written."


# Script Start

help_text = """
syntax: python compare_xml_files.py old_file.xml new_file.xml {workspace {compare_node_text = True {log_file_path = new_file.log}}}

Setting compare_node_text to False will only check for differences between the xml tags and their attributes.

The default output location for the log file is the location of the new xml file with a .log extension.  Note that passing an invalid log file path will just prevent the log file from being written.
"""

# If arguments were passed from command line, process them
if len(sys.argv[0:])==0:
    print __doc__
    exit()
else:
    if len (sys.argv[1:]) < 2:
        print "Function requires at least two arguments . . ."
        old_xml_file = raw_input("old XML file: ")
        new_xml_file = raw_input("new XML file: ")
        check_text = raw_input("Compare Node Text (y/n)? ")
    else:
        # First two arguments should be the paths for the xml files to compare
        old_xml_file = sys.argv[1]
        new_xml_file = sys.argv[2]
        check_text = None

    # Argument 3 is optional. Sets the working directory.
    if len (sys.argv[1:]) > 2:
        workspace = sys.argv[3]
        if os.path.isdir(workspace): # Ignore if not an existing directory
            os.chdir(workspace)

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

    # Argument 4 is optional. Default=True.
    # It gives the option to skip checking text differences and to focus on only the tags

    if len (sys.argv[1:]) > 3:
        check_text = sys.argv[4]
    if check_text:
        check_text = str(check_text).lower()
        if check_text in ["f","false","n","no"]:
            compare_node_text = False
        elif check_text in ["t","true","y","yes"]:
            compare_node_text = True
        else:
            print "Error: Could not decipher compare_node_text argument.  Should be boolean."
            print help_text
            exit(1)
    else:
        compare_node_text = True #default

    # Argument 5 is optional. Default=new xml file name with a .log extension.
    # This is the log file path.
    if len (sys.argv[1:]) > 4:
        output_location = sys.argv[5]
    else:
        output_location = new_xml_file.replace(".xml",".log") #default


compareXMLfiles(old_xml_file,new_xml_file,output_location)
