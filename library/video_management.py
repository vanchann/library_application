#!/usr/bin/env python3

# imports
import os
import sys
import csv
from lxml import etree
from library.management import Manager
from library.support.utility import Utility

"""
Class: VideoManager

Extends class Manager.
The VideoManager class uses XML to store and manage video elements.
Contents maybe created, parsed and destroyed.
The class also supports validation of the XML file given an XSD schema, so that
it may be used independently.
"""
class VideoManager(Manager):
    """
    Initializer
    """
    def __init__(self, storageroot, libfile, schemafile):
        # Library type.
        libtype = "video"
        # Allow sorting element tags.
        sortingtags = ["title", "format"]
        uniquekey = "title"
        # Call parent initializer.
        super().__init__(storageroot, libfile, schemafile, libtype, sortingtags, uniquekey)
    # End of initializer.
# End of class VideoManager.

# The following section contains code to execute when script is run from the command line.
"""
Function: main

Entry point for the execution of the script.
"""
def main():
    print(__file__)
# End of function main.

# Test running or loading.
if __name__ == "__main__":
    main()
