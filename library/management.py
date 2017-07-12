#!/usr/bin/env python3

# imports
import os
import sys
import shutil
from lxml import etree

"""
Class: Manager

Abstract class.
The Manager class uses XML to store and manage elements.
Contents maybe created, parsed and destroyed.
The class also supports validation of the XML file given an XSD schema, so that
it may be used independently.
"""
class Manager:
    """
    Initializer
    """
    def __init__(self, storageroot, libfile, schemafile, libtype):
        super().__init__()
        # Initialize library variables.
        self._storageroot = storageroot
        self._libtype = libtype
        self._xmlfile = os.path.join(self._storageroot, self._libtype, libfile)
        self._xsdfile = os.path.join(self._storageroot, self._libtype, schemafile)
        #print(self._xmlfile)
        #print(self._xsdfile)
    # End of initializer

    # Implemented methods, whis may be called from a Manager instance object..
    """
    Method: validate

    Validates library storage file.
    Returns 0 if validates, 1 if not and 2 in case of error.
    """
    def validate(self):
        try:
            with open(self._xsdfile, 'r') as xsdfile, open(self._xmlfile, 'r') as xmlfile:
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

    """
    Method: backup

    Creates backup of the library file.
    Returns 0 on success and 2 in case of error.
    """
    def backup(self):
        try:
            shutil.copy2(self._xmlfile, self._xmlfile + ".back")
            return 0
        except OSError:
            return 2
    # End of method backup.

    """
    Method: restore

    Restores the library file form backup.
    Returns 0 on success and 2 in case of error.
    """
    def restore(self):
        try:
            shutil.copy2(self._xmlfile + ".back", self._xmlfile)
            return 0
        except OSError:
            return 2
    # End of method restore.

    """
    Method: create_library

    Creates a new empty library storage file.
    Returns 0 on success, 1 in case of directory tree error and 2 in case of file error.
    """
    def create_library(self):
        storagedir = os.path.join(self._storageroot, self._libtype)
        # Create directory tree is necessary.
        if not os.path.isdir(storagedir):
            try:
                os.makedirs(storagedir)
            except OSError:
                return 1
        # Create the xml tree.
        root = etree.XML("""
<library xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="{}"></library>
        """.format(os.path.basename(self._xsdfile)))

        # Write xml tree to storage file
        xmlout = etree.ElementTree(root)
        try:
            xmlout.write(self._xmlfile, xml_declaration=True, encoding="UTF-8", pretty_print=True)
            return 0
        except OSError:
            return 2
    # End of method create_library.

    # NOT implemented methods. Child class should implemented them, based on their storage settings.
    # Storage management methods.
    """
    Method: restore_schema

    Restores the library schema file.
    Returns 0 on success and 2 in case of error.
    """
    def restore_schema(self):
        raise NotImplementedError("Method get_all_elements should be implemented in child class.")
        """
        try:
            return 0
        except OSError:
            return 2
        """
    # End of method restore_schema.

    # Element manipulation methods.
    """
    Method: get_all_elements

    Gets all elements in the specified order.
    """
    def get_all_elements(self, order = None):
        raise NotImplementedError("Method get_all_elements should be implemented in child class.")
    # End of method get_all_elements.

    """
    Method: get_element

    Gets an element.
    """
    def get_element(self, element):
        raise NotImplementedError("Method get_element should be implemented in child class.")
    # End of method get_element.

    """
    Method: add_element

    Adds an element.
    """
    def add_element(self, element):
        raise NotImplementedError("Method add_element should be implemented in child class.")
    # End of method add_element.

    """
    Method: remove_element

    Removes an element.
    """
    def remove_element(self, element):
        raise NotImplementedError("Method remove_element should be implemented in child class.")
    # End of method remove_element.

    """
    Method: edit_element

    Edits an element.
    """
    def edit_element(self, element):
        raise NotImplementedError("Method edit_element should be implemented in child class.")
    # End of method edit_element.

    # Display methods.
    """
    Method: show_menu

    Displays management menu.
    """
    def show_menu(self):
        raise NotImplementedError("Method show_menu should be implemented in child class.")
    # End of method show_menu.

    """
    Method: show_all_elements

    Shows all elements.
    """
    def show_all_elements(self):
        raise NotImplementedError("Method show_all_elements should be implemented in child class.")
    # End of method show_all_elements.

    """
    Method: show_element

    Shows an element.
    """
    def show_element(self):
        raise NotImplementedError("Method show_element should be implemented in child class.")
    # End of method show_element.

    """
    Method: show_element_editor

    Shows the element editor.
    """
    def show_element_editor(self, element):
        raise NotImplementedError("Method show_element_editor should be implemented in child class.")
    # End of method show_element_editor.
# End of class Manager.

# The following section contains code to execute when script is run from the command line.
"""
Function: main

Entry point for the execution of the script.
"""
def main():
    print(__file__)
# End of function main.

# Test running or loading
if __name__ == "__main__":
    main()
