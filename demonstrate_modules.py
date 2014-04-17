#-------------------------------------------------------------------------------
# Name:        demonstrate_modules.py
#
# Purpose:
#
# Author:      Hal Watson (hal.watson@state.mn.us)
#
# Created:     04/17/2014
#
# Requires:
#
#
#-------------------------------------------------------------------------------


def PrintString(my_string):
    # This is an example of a function block that you write
    # directly into your script. To use this function you
    # don't need to "import" any module at all, just call
    # the function from within your main block.
    print my_string
    return None


def main():
    # This is the main code block, and will be executed first.

    # Standard imports (these modules are included in python)

    import sys
    import os


    # These next two lines append a new path to our PYTHONPATH environment
    # This allows us to import modules (collections of functions)
    # that are placed in a specific directory, such as those on the GDRS.

    # We are using os.path.join to constuct the path to the folder
    # Using os.path.join is the most robust way to create a string
    # representing a path to a file.

    system_module_loc = os.path.join('V:', 'gdrs', 'system', 'scripts', 'modules')
    sys.path.append(system_module_loc)


    # Now we can import our custom module (collection of functions).
    # GDRS_UTIL is just an alias for our module that we can use in
    # the code below.

    import gdrs_utility_functions as GDRS_UTIL


    # From the GDRS_UTIL module, get a file friendly date-time stamp.

    date_time_stamp = GDRS_UTIL.GetFileFriendlyDateTimeStamp()

    # Now let's make a .zip archive of a sub-directory, using the
    # date-time stamp as part of the filename. We'll use the "ZipDir"
    # function from the GDRS_UTIL module.
    #
    # Example usage:
    #     folder_to_zip = "/home/drsadmin/temp"
    #     archive_to_create = "/home/drsadmin/temp.zip"
    #     GDRS_UTIL.ZipDir(folder_to_zip, archive_to_create)

    # There are some quirks to constructing paths in Windows, since you can't put a backslash
    # at the end of a path component (e.g 'D:\' is not allowed) .
    # The method below is most robust, but you could also use: r'D:\Users\hawatson\_GISTemp\Hal11'
    # which is what you see in a lot of ArcGIS example documentation
    folder_to_zip = os.path.join('D:', os.sep,  'Users', 'hawatson', '_GISTemp', 'Hal11')

    # Here we construct the full path to the final .zip arcive
    zip_filename = "backup_" + date_time_stamp + ".zip"
    archive_to_create = os.path.join('D:', os.sep, 'Users', 'hawatson', '_GISTemp', zip_filename)

    # And call the function in the GDRS_UTIL module (gdrs_utility_functions)
    GDRS_UTIL.ZipDir(folder_to_zip, archive_to_create)



if __name__ == '__main__':
    main()
