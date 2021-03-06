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
    def __init__(self, storageroot, libfile, schemafile, libtype, sortingtags, uniquekey):
        super().__init__()
        # Initialize library variables.
        self._storageroot = storageroot
        self._libtype = libtype
        self._xmlfile = os.path.join(self._storageroot, self._libtype, libfile)
        self._xsdfile = os.path.join(self._storageroot, self._libtype, schemafile)
        self._sortingtags = sortingtags
        self._uniquekey = uniquekey
        # Initialize character sets for case inseincitive rearches.
        self._uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self._lowercase = 'abcdefghijklmnopqrstuvwxyz'
    # End of initializer.

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
            print("2. Display item by {}".format(self._uniquekey))
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
                Utility.clear()
                self.show_search_elements()
            elif choice == 4:
                self.show_add_element()
            elif choice == 5:
                self.show_edit_element()
            elif choice == 6:
                self.show_remove_element()
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

    :return str_or_None: Union[str, None].
    """
    def get_sorting_element(self):
        # Generate menu
        choices = range(1, len(self._sortingtags) + 1)
        choice = None
        while choice not in choices:
            # Clear display.
            Utility.clear()
            # Display menu
            print("Element [to sort by, search for, etc]:")
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

    :return bool: The ascending order.
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
            overwrite = Utility.get_answer_yn("A backup file already exists. Overwrite?")

            # Making sure that only Y or y will overwrite the backup.
            if overwrite != "y":
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

    Displays messages for restoring the library file from backup.
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
            overwrite = Utility.get_answer_yn("This operation will overwrite existing library if any. Continue?")

            # Making sure that only Y or y will overwrite the backup.
            if overwrite != "y":
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
            overwrite = Utility.get_answer_yn("This operation will overwrite the existing library. Continue?")

            # Making sure that only Y or y will overwrite the existing library.
            if overwrite != "y":
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
            overwrite = Utility.get_answer_yn("This operation will overwrite the existing library schema. Continue?")

            # Making sure that only Y or y will overwrite the existing schema.
            if overwrite != "y":
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

    :return int: 0 on success and 2 in case of error.
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

    Restores the library file from backup.

    :return int: 0 on success and 2 in case of error.
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

    :return int: 0 on success, 1 in case of directory tree error and 2 in case of file error.
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

    """
    Method: edit_element

    Edits an element.

    :return int: 0 on success, 1 in case of directory tree error and 2 in case of file error.
    """
    def edit_element(self, originalkey, elementdict):
        # Initialization is not necessary, but helps readability.
        value = 0
        try:
            # Create a temporary library backup.
            temp =  self._xmlfile + ".temp"
            shutil.copy2(self._xmlfile, temp)
            # Remove original element.
            value = self.remove_element(originalkey)
            if value == 0:
                # Save new file containing the edited element.
                value = self.add_element(elementdict)
                if value != 0:
                    # Restore original file from temp.
                    shutil.copy2(temp, self._xmlfile)
        except OSError:
            return 2
        finally:
            # Remove temporary file.
            # If a new exception will be raised here, keep the temporary file on
            # disk, so that library restoration may still be possible and let
            # the exception bubbling.
            # Since the users has the privilege to create the file, its revoval
            # should have been possible too.
            os.remove(temp)

        return value
    # End of method edit_element.

    # Display methods.
    """
    Method: show_search_elements

    Shows elements of a search result.

    :param str element[=None]: The element tag containing the value. Should be in _sortingtags list.
    :param str value[=None]: The value inside element tag to search for.
    :param bool ascending[=True]: The order to sort the results.
    """
    def show_search_elements(self, element = None, value = None, ascending = True):
        menu = None
        # Get all elements
        if element is None:
            menu = True
            # Get user input.
            element = self.get_sorting_element()
            value = input("Enter a value to search for: ")
            elements = self.search_elements(element, value, self.get_sorting_order())
            Utility.clear()
        else:
            elements = self.search_elements(element, value, ascending)
        # Display results
        if isinstance(elements, int):
            print("Invalid storage file {}.".format(self._xmlfile))
        elif elements is None:
            print("No item with '{}' containing '{}' has been found.".format(element.title(), value))
        else:
            # Show table of results.
            self.show_table(elements)
        # Pause if the method has been called without an element.
        if menu:
            print()
            input("Press 'Enter' to return to menu: ")
    # End of method show_search_elements.

    """
    Method: show_all_elements

    Shows all elements.

    :param str element[=None]: The element tag on which show will be based. Should be in _sortingtags list.
    :param bool ascending[=True]: The order to sort the results.
    :param bool menu[=None]: Display menu.
    """
    def show_all_elements(self, element = None, ascending = True, menu = None):
        # Get all elements
        if menu is None:
            elements = self.get_all_elements(element, ascending)
        else:
            # Get user input.
            elements = self.get_all_elements(self.get_sorting_element(), self.get_sorting_order())
            Utility.clear()
        # Display results
        if isinstance(elements, int):
            print("Invalid storage file {}.".format(self._xmlfile))
        elif elements is None:
            print("The library is empty.")
        else:
            # Show table of results.
            self.show_table(elements)
        # Pause if the method has been called without an element.
        if menu is not None:
            print()
            input("Press 'Enter' to return to menu: ")
    # End of method show_all_elements.

    """
    Method: show_add_element

    Shows messages about new element's addition.

    :param str element[=None]: The python dictionary containing the values of the element to be added to library.
    :raise NotImplementedError: Through methods add_element or _generate_libtype_element, if at least one of them is not implemented in child class.
    """
    def show_add_element(self, element = None):
        menu = None
        # Get the element from the user.
        if element is None:
            menu = True
            Utility.clear()
            # Generate new element.
            element = self._generate_libtype_element()
            # Return if element is still None.
            if element is None:
                input("Press 'Enter' to return to menu: ")
                return

            print("Adding item:")
            print(element)
            answer = Utility.get_answer_yn("Add item?")
            # User wants to quit.
            if answer == "n":
                return

        # Add item.
        if self.add_element(element) == 0:
            print("The item {} has been added successfully.".format(element))
        else:
            print("The item {} has not been added.".format(element))

        if menu:
            input("Press 'Enter' to return to menu: ")
    # End of method show_add_element.

    """
    Method: show_edit_element

    Shows element's editing messages.

    :param str element[=None]: The python dictionary containing the values of the element to be edited.
    :raise NotImplementedError: Through methods get_element or _xmlitem_to_dict or _generate_libtype_element, if at least one of them is not implemented in child class.
    """
    def show_edit_element(self, element = None):
        menu = None
        # Get the element's unique key from the user.
        if element is None:
            menu = True
            Utility.clear()
            element = input("Enter the {} of the item to be edited: ".format(self._uniquekey))
        # Get element.
        item = self.get_element(element)
        if item is None:
            print("No item with {} '{}' found.".format(self._uniquekey, element))
        elif isinstance(item, int):
            print("Invalid storage file {}.".format(self._xmlfile))
        else:
            # Create python dictionary parsing element's values.
            itemdict = self._xmlitem_to_dict(item)
            # Edit item.
            itemdict = self._generate_libtype_element(itemdict)
            # Check if itemdict contains values.
            if itemdict is not None:
                #confirm before save.
                print("Saving item:")
                print(itemdict)
                answer = Utility.get_answer_yn("Save item?")
                # User wants to quit.
                if answer == "n":
                    return
                # Persist changes.
                try:
                    if self.edit_element(element, itemdict) == 0:
                        print("The edited item {} has been saved successfully.".format(element))
                    else:
                        print("The edited item {} has not been saved.".format(element))
                except OSError:
                    print("Temporary file ha not been removed, after the edited item {} has been saved.".format(element))
        if menu:
            input("Press 'Enter' to return to menu: ")
    # End of method show_edit_element.

    """
    Method: show_remove_element

    Shows messages about element's removal.

    :param str element[=None]: The exact value in element title.
    :raise NotImplementedError: Method should be implemented in child class.
    """
    def show_remove_element(self, element = None):
        menu = None
        # Get the element's title from the user.
        if element is None:
            menu = True
            Utility.clear()
            element = input("Enter the {} of the item to be removed: ".format(self._uniquekey))
        # Remove item.
        if self.remove_element(element) == 0:
            print("The item {} has been removed successfully.".format(element))
        else:
            print("The item {} has not been removed.".format(element))

        if menu:
            input("Press 'Enter' to return to menu: ")
    # End of method show_remove_element.

    """
    Method: show_import_csv

    Shows import CSV file messages.
    Valid CSV header is subclass specific.

    :param str impfile: the file to import.
    :return int: 0 on success, 1 if CSV is not valid, 2 in case of filesystem write error and 3 if XML the tree created in memory is not valid.
    """
    def show_import_csv(self, impfile):
        result = 1
        # Check if file exists.
        if not os.path.isfile(impfile):
            print("File {} does not exist.".format(impfile))
            return result
        # Import file.
        result = self.import_csv(impfile)
        if result == 0:
            print("File '{}' has been imported successfully.".format(impfile))
        elif result == 1 or result == 3:
            print("CSV file is not valid.")
        else:
            print("A filesystem error occurred. Make sure you have write provileges in '{}'.".format(os.path.join(self._storageroot, self._libtype)))
        return result
    # End of method show_import_csv.

    """
    Method: show_export_csv

    Shows export CSV messages.

    :param str expfile: the file to export.
    :return int: 0 on success, 1 if library file is not valid and 2 in case of error.
    """
    def show_export_csv(self, expfile):
        # Export file.
        result = self.export_csv(expfile)
        if result == 0:
            print("File '{}' has been exported successfully.".format(expfile))
        else:
            print("An error occurred.")
        return result
    # End of method show_export_csv.

    # Utility methods, which meant to be called only form inside Manager class or its subclasses.
    # Like protected methods in other languages.
    """
    Method: _write_tree

    Adds nodes to tree and writes it to file.

    :param list nodes: The list of etree.Element nodes.
    :return int: 0 on success, 2 on write file error and 3 on validation error.
    """
    def _write_tree(self, nodes):
            # Create the xml tree.
            root = etree.XML("""
<library xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="{}"></library>
            """.format(os.path.basename(self._xsdfile)))
            for node in nodes:
                root.append(node)
            # Generate new tree.
            xmlout = etree.ElementTree(root)
            # Validate tree.
            if Utility.validate_tree(self._xsdfile, xmlout) != 0:
                return 3
            # Write to file.
            try:
                xmlout.write(self._xmlfile, xml_declaration = True, encoding = "UTF-8", pretty_print = True)
                return 0
            except OSError:
                return 2
    # End of method _write_tree.

    """
    Method: _add_element_to_tree

    Adds new element to tree nodes.

    :param etree.Element element: The element to be added.
    :param str sorttag[="title"]: The element to use for sorting. Should be a mandatory direct child of basic item element.
    :return int: 0 on success, 2 on write file error and 3 on validation error.
    """
    def _add_element_to_tree(self, element, sorttag = "title"):
            # Create xml tree.
            tree = etree.parse(self._xmlfile)
            # Get a list of all elements.
            nodes = tree.xpath("/library/{}".format(self._libtype))
            # Append to lis.
            nodes.append(element)
            # Sort elements list by title.
            index = self._sortingtags.index(sorttag)
            nodes.sort(key = lambda element: element[index].text.title())
            # Write to file.
            return self._write_tree(nodes)
    # End of method _add_element_to_tree.

    # NOT implemented methods. Child class should implemented them, based on their storage settings.
    # Utility methods, which meant to be called only form inside Manager class or its subclasses.
    # Like protected methods in other languages.
    """
    Method: _xmlitem_to_dict

    Generates python dictionary from dictionary XML element.

    :param etree.Element element: The XML element node.
    :return dict: The python dictionary version of the XML node.
    :raise NotImplementedError: Method should be implemented in child class.
    """
    def _xmlitem_to_dict(self, element):
        raise NotImplementedError("Method _xmlitem_to_dict should be implemented in child class.")
    # End of method _xmlitem_to_dict.

    """
    Method: _generate_libtype_element

    Generate library type python dictionary.

    :param dict element[=None]: The python dictionary containing the values of the element.
    :return dict: The python dictionary containing new values.
    :raise NotImplementedError: Method should be implemented in child class.
    """
    def _generate_libtype_element(self, element = None):
        raise NotImplementedError("Method _generate_libtype_element should be implemented in child class.")
    # End of method _generate_libtype_element.


    # File import and export functionality.
    """
    Method: import_csv

    Imports a CSV file as the XML library file.

    :param str impfile: the file to import.
    :return int: 0 on success and 2 in case of error.
    :raise NotImplementedError: Method should be implemented in child class.
    """
    def import_csv(self, impfile):
        raise NotImplementedError("Method import_csv should be implemented in child class.")
    # End of method import_csv.

    """
    Method: export_csv

    Exports XML library file as a CSV file.

    :param str expfile: the file to export.
    :return int: 0 on success and 2 in case of error.
    :raise NotImplementedError: Method should be implemented in child class.
    """
    def export_csv(self, expfile):
        raise NotImplementedError("Method export_csv should be implemented in child class.")
    # End of method export_csv.

    # Storage management methods.
    """
    Method: restore_schema

    Restores the library schema file.

    :return int: 0 on success and 2 in case of error.
    :raise NotImplementedError: Method should be implemented in child class.
    """
    def restore_schema(self):
        raise NotImplementedError("Method restore_schema should be implemented in child class.")
    # End of method restore_schema.

    # Element manipulation methods.
    """
    Method: search_elements

    Search for elements containing a given value.

    :param str element: The element tag containing the value. Should be in _sortingtags list.
    :param str value: The value inside element tag to search for.
    :param bool ascending[=True]: The order to sort the results.
    :raise NotImplementedError: Method should be implemented in child class.
    """
    def search_elements(self, element, value, ascending = True):
        raise NotImplementedError("Method search_elements should be implemented in child class.")
    # End of method search_elements.

    """
    Method: get_all_elements

    Gets all elements in the specified order.

    :param str element[=None]: The element tag on which get will be based. Should be in _sortingtags list.
    :param bool ascending[=True]: The order to sort the results.
    :raise NotImplementedError: Method should be implemented in child class.
    """
    def get_all_elements(self, element = None, ascending = True):
        raise NotImplementedError("Method get_all_elements should be implemented in child class.")
    # End of method get_all_elements.

    """
    Method: get_element

    Gets an element by unique value.

    :param str element: The exact value in element tag. Tag text should be unique.
    :raise NotImplementedError: Method should be implemented in child class.
    """
    def get_element(self, element):
        raise NotImplementedError("Method get_element should be implemented in child class.")
    # End of method get_element.

    """
    Method: add_element

    Adds an element.

    :param dict elementdict: The python dictionary containing the values of the element to be added to library.
    :raise NotImplementedError: Method should be implemented in child class.
    """
    def add_element(self, elementdict):
        raise NotImplementedError("Method add_element should be implemented in child class.")
    # End of method add_element.

    """
    Method: remove_element

    Removes an element.

    :param str element: The exact value in element tag. Tag text should be unique.
    :raise NotImplementedError: Method should be implemented in child class.
    """
    def remove_element(self, element):
        raise NotImplementedError("Method remove_element should be implemented in child class.")
    # End of method remove_element.

    # Display methods.
    """
    Method: show_table

    Shows table of elements.

    :param list elements: List of etree.Element to be shown.
    :raise NotImplementedError: Method should be implemented in child class.
    """
    def show_table(self, elements):
        raise NotImplementedError("Method show_search_elements should be implemented in child class.")
    # End of method show_table.

    """
    Method: show_element

    Shows an element.

    :param str value[=None]: The exact value in element tag. Tag text should be unique.
    :raise NotImplementedError: Method should be implemented in child class.
    """
    def show_element(self, value = None):
        raise NotImplementedError("Method show_element should be implemented in child class.")
    # End of method show_element.
# End of class Manager.

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
