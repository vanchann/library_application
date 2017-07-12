#!/usr/bin/env python3

# imports
import os
import sys
from lxml import etree
from library.management import Manager

"""
Class: GameManager

Extends class Manager.
The GameManager class uses XML to store and manage game elements.
Contents maybe created, parsed and destroyed.
The class also supports validation of the XML file given an XSD schema, so that
it may be used independently.
"""
class GameManager(Manager):
    """
    Initializer
    """
    def __init__(self, storageroot, libfile, schemafile):
        super().__init__(storageroot, libfile, schemafile, "game")
    # End of initializer

    # NOT implemented parent methods. Child class should implemented them, based on their storage settings.
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
# End of class GameManager.

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
