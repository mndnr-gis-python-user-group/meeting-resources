#-------------------------------------------------------------------------------
# Updated:     2017-05-18
#
# Name:        jmr_helpers.py
# Purpose:     Helper function for jmr_class_builder (passNull) and a date
#              reformatter that I found useful (dateToMDYYYY).
#
# Author:      Jeff Reinhart
#
# Created:     2017-05-18
#-------------------------------------------------------------------------------

def passNull(fieldValue, propertyValue):
    if fieldValue != None:
        return fieldValue
    else:
        return propertyValue

def dateToMDYYYY(dateIn):
    if dateIn == datetime.datetime(1900,1,1,0,0,0) or dateIn is None:
        dateStr = ''
    else:
        dateStr = "{dt.month}/{dt.day}/{dt.year}".format(dt = dateIn)
    return dateStr