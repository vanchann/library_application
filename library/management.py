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
    def __init__(self, storageroot, libfile, schemafile, libtype, sortingtags):
        super().__init__()
        # Initialize library variables.
        self._storageroot = storageroot
        self._libtype = libtype
        self._xmlfile = os.path.join(self._storageroot, self._libtype, libfile)
        self._xsdfile = os.path.join(self._storageroot, self._libtype, schemafile)
        self._sortingtags = sortingtags
    # End of initializer

    # Implemented methods, whis may be called from a Manager instance object.
    """
    Method: show_menu

    Displays management menu.
    """
    def show_menu(self):
        # Initialize local variables
        avchoices = range(7)
        choice = None

        # Generate menu
        while choice not in avchoices:
            # Clear display.
            Utility.clear()
            # Display menu
            print("Available actions for library {}:".format(self._libtype.upper()))
            print("1. Display all items")
            print("2. Display item by unique value")
            print("3. Search for items")
            print("4. Add new item")
            print("5. Edit existing item")
            print("6. Remove item")
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
                self.show_all_elements(menu = True)
            elif choice == 2:
                Utility.clear()
                self.show_element()
            elif choice == 3:
                pass
            elif choice == 4:
                pass
            elif choice == 5:
                pass
            elif choice == 6:
                pass
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
            print("1. Validate library storage")
            print("2. Backup library")
            print("3. Restore library from backup")
            print("4. Create new empty library")
            print("5. Restore library schema")
            print("0. Back")
            # Get user choice.
            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                choice = None

            # React to user choice.
            if choice == 0:
                return
            elif choice == 1:
                self.show_validation()
            elif choice == 2:
                self.show_backup()
            elif choice == 3:
                self.show_restore()
            elif choice == 4:
                self.show_create_library()
            elif choice == 5:
                self.show_restore_schema()
            choice = None
    # End of method show_utility_menu.

    """
    Method: get_sorting_element

    Gets a shortng elements tag.
    """
    def get_sorting_element(self):
        # Generate menu
        choices = range(1, len(self._sortingtags) + 1)
        choice = None
        while choice not in choices:
            # Clear display.
            Utility.clear()
            # Display menu
            print("Sort by:")
            i = 0
            for sorttag in self._sortingtags:
                i += 1
                print("{}. {}".format(i, sorttag))
            # Get user choice.
            try:
                choice = input("Enter your choice [default 1]: ")
                if choice == "":
                    return self._sortingtags[0]
                choice = int(choice)
            except ValueError:
                choice = None

        return  self._sortingtags[choice - 1]
    # End of method get_sorting_element

    """
    Method: get_sorting_order

    Gets sorting order.
    """
    def get_sorting_order(self):
        # Generate menu
        choices = range(1, 3)
        choice = None
        while choice not in choices:
            # Clear display.
            Utility.clear()
            # Display menu
            print("Order:")
            print("1. Ascending")
            print("2. Descending")
            # Get user choice.
            try:
                choice = input("Enter your choice [default 1]: ")
                if choice == "":
                    return True
                choice = int(choice)
            except ValueError:
                choice = None

        if choice == 1:
            return True

        return False
    # End of method get_sorting_order

    """
    Method: show_validation

    Displays library storage file validation results.
    """
    def show_validation(self):
        Utility.clear()
        if self.validate() == 0:
            print("Validates.")
        else:
            print("Does NOT validate.")
        input("Press 'Enter' to continue: ")
    # End of method show_validation.

    """
    Method: show_backup

    Displays backup messages.
    """
    def show_backup(self):
        Utility.clear()
        if os.path.isfile(self._xmlfile + ".back"):
            # Ask user for overwriting existing backup file.
            overwrite = Utility.get_answer_yn("A backup file already exists. Overwrite [y/n]? ")

            # Making sure that only Y or y will overwrite the backup.
            if overwrite.lower() != "y":
                print("Nothing has changed.")
                input("Press 'Enter' to continue: ")
                return

        # If there isn't any backup already or the user has entered Y or y
        # create a new backup, overwriting existing one if any.
        if self.backup() == 0:
            print("New backup file has been created successfully.")
        else:
            print("Backup process has failed.")
            print("Make sure a [valid] '{}' file exists and you have write privilege in containing folder.".format(self._xmlfile))

        input("Press 'Enter' to continue: ")
    # End of method show_backup.

    """
    Method: show_restore

    Displays messages for restoring the library file form backup.
    """
    def show_restore(self):
        Utility.clear()
        backupfile = self._xmlfile + ".back"
        if os.path.isfile(backupfile):
            # Validate backup file before continue.
            if Utility.validate(self._xsdfile, backupfile) != 0:
                print("'{}' is not a valid library file.".format(self._xmlfile))
                print("Nothing has changed.")
                input("Press 'Enter' to continue: ")
                return
            # Ask user for overwriting existing library file.
            overwrite = Utility.get_answer_yn("This operation will overwrite existing library if any. Continue [y/n]? ")

            # Making sure that only Y or y will overwrite the backup.
            if overwrite.lower() != "y":
                print("Nothing has changed.")
                input("Press 'Enter' to continue: ")
                return

            # Restore library file, overwriting existing one if any.
            if self.restore() == 0:
                print("Library file has been restored successfully.")
            else:
                print("Library restoration process has failed.")
                print("Make sure a [valid] '{}' file exists and you have write privilege in containing folder.".format(backupfile))
        else:
            print("No backup file has been found.")
        input("Press 'Enter' to continue: ")
    # End of method show_restore.

    """
    Method: show_create_library

    Displays messages for creating a new empty library.
    """
    def show_create_library(self):
        Utility.clear()
        if os.path.isfile(self._xmlfile):
            # Ask user for overwriting existing library.
            overwrite = Utility.get_answer_yn("This operation will overwrite the existing library. Continue [y/n]? ")

            # Making sure that only Y or y will overwrite the existing library.
            if overwrite.lower() != "y":
                print("Nothing has changed.")
                input("Press 'Enter' to continue: ")
                return

        # If there isn't any library file already or the user has entered Y or y
        # create a new empty library, overwriting existing one if any.
        if self.create_library() == 0:
            print("New empty library has been created successfully.")
        else:
            print("New library creation process has failed.")
            print("Make sure you have write privilege in '{}' folder.".format(os.path.join(self._storageroot, self._libtype)))

        input("Press 'Enter' to continue: ")
    # End of method show_create_library.

    """
    Method: show_restore_schema

    Displays messages for restoring the library schema file.
    """
    def show_restore_schema(self):
        Utility.clear()
        if os.path.isfile(self._xsdfile):
            # Ask user for overwriting existing schema file.
            overwrite = Utility.get_answer_yn("This operation will overwrite the existing library schema. Continue [y/n]? ")

            # Making sure that only Y or y will overwrite the existing schema.
            if overwrite.lower() != "y":
                print("Nothing has changed.")
                input("Press 'Enter' to continue: ")
                return

        # If there isn't any schema file already or the user has entered Y or y
        # restore the default library schema, overwriting existing one if any.
        if self.restore_schema() == 0:
            print("Default library schema has been restored successfully.")
        else:
            print("Library schema restoration process has failed.")
            print("Make sure you have write privilege in '{}' folder.".format(os.path.join(self._storageroot, self._libtype)))

        input("Press 'Enter' to continue: ")
    # End of method show_restore_schema.

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
        raise NotImplementedError("Method restore_schema should be implemented in child class.")
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
    def get_all_elements(self, element = None, ascending = True):
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
    def show_all_elements(self, value = None, ascending = True, menu = None):
        raise NotImplementedError("Method show_all_elements should be implemented in child class.")
    # End of method show_all_elements.

    """
    Method: show_element

    Shows an element.
    """
    def show_element(self, value = None):
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
