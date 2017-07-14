#!/usr/bin/env python3

# imports
import os
import sys
import shutil
import platform
from lxml import etree
from library.support.utility import Utility

"""
Class: Manager

Abstract class.
The Manager class uses XML to store and manage elements.
Contents maybe created, parsed and destroyed.
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
    # End of initializer

    """
    Method: show_menu

    Displays management menu.
    """
    def show_menu(self):
        # Initialize local variables
        avchoices = range(2)
        choice = None

        # Generate menu
        while choice not in avchoices:
            # Clear display.
            Utility.clear()
            # Display menu
            print("Available actions for library {}:".format(self._libtype.upper()))
            print("1. Display item by unique value")
            print("9. Storage utilities")
            print("0. Exit library")
            # Get user choice.
            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                choice = None

            # React to user choice.
            if choice == 0:
                return
            elif choice == 1:
                Utility.clear()
                self.show_element()
            elif choice == 9:
                self.show_utility_menu()
            choice = None
    # End of method show_menu.

    """
    Method: show_utility_menu

    Displays storage utility menu.
    """
    def show_utility_menu(self):
        # Initialize local variables
        avchoices = range(1)
        choice = None

        # Generate menu
        while choice not in avchoices:
            # Clear display.
            Utility.clear()
            # Display menu
            print("Available storage utilities:")
            print("0. Back")
            # Get user choice.
            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                choice = None

            # React to user choice.
            if choice == 0:
                return
            choice = None
    # End of method show_utility_menu.

    # Implemented methods, whis may be called from a Manager instance object..
    """
    Method: validate

    Validates library storage file.
    Returns 0 if validates, 1 if not and 2 in case of error.
    """
    def validate(self):
        return Utility.validate(self._xsdfile, self._xmlfile)
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

    """
    Method: search_elements

    Search for elements containing a given value.
    """
    def search_elements(self, element, value):
        raise NotImplementedError("Method get_element should be implemented in child class.")
    # End of method search_elements.

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

    Gets an element by unique value.
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
    def show_element_editor(self, element = None):
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
