#!/usr/bin/env python3

# imports
import os
import sys
from lxml import etree

"""
Class: Manager

!!! Abstract class !!!
The Manager class uses XML to store and manage elements.
Contents maybe created, parsed and destroyed.
The class also supports validation of the XML file given an XSD schema, so that
it may be used independently.
"""
class Manager:
    """
    Initializer
    """
    def __init__(self, storageroot, libtype):
        super().__init__()
        # Initialize application directory values.
        self.__storageroot = storageroot
        #self.__confdir = os.path.join(self.__rundir, "config")
        #self.__confxsd = os.path.join(self.__confdir, "config.xsd")
        #self.__confxml = os.path.join(self.__confdir, "config.xml")
    # End of initializer

    # Implemented methods, whis may be called from a Manager instance object..
    """
    Method: validate

    Validates XML file given an XSD schema.
    Returns 0 if validates, 1 if not and 2 in case of error.
    """
    def validate(self, schemafile, testfile):
        try:
            with open(schemafile, 'r') as xsdfile, open(testfile, 'r') as xmlfile:
                # Create schema object.
                xmlschema_doc = etree.parse(xsdfile)
                xmlschema = etree.XMLSchema(xmlschema_doc)
                # Create xml tree.
                xmldoc = etree.parse(xmlfile)
                # Validate.
                if xmlschema.validate(xmldoc):
                    return 0
                else:
                    return 1
        except FileNotFoundError:
            return 2
    # End of method validate.

    # NOT implemented methods. Child class should implemented them, based on their storage settings.
    """
    Method: show_all_elements

    Shows all in the specified order.
    """
    def show_all_elements(self, order = None):
        raise NotImplementedError("Method show_all_elements should be implemented in child class.")
    # End of method show_all_elements.
# End of class Manager.

# The following section contains code to execute when script is run from the command line.
"""
Function: main

Entry point for the execution of the script.
"""
def main():
    library = Manager()

# Test running or loading
if __name__ == "__main__":
    main()
