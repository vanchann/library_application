#!/usr/bin/env python3

# imports
import os
import sys
from lxml import etree
#from lxml import objectify
from library.management import Manager
#from library.support.utility import Utility

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
        # Library type.
        libtype = "game"
        # Allow sorting element tags.
        sortingtags = ["title", "shop", "finished"]
        # Call parent initializer.
        super().__init__(storageroot, libfile, schemafile, libtype, sortingtags)
    # End of initializer

    # NOT implemented parent methods. Child class should implemented them, based on their storage settings.
    # Storage management methods.
    """
    Method: restore_schema

    Restores the library schema file.
    Returns 0 on success and 2 in case of error.
    """
    def restore_schema(self):
        # Create the xsd tree.
        xsdroot = etree.XML("""
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">

<!-- definition of simple elements -->
<xs:element name="title" type="xs:string"/>
<xs:element name="shop" type="xs:string"/>
<xs:element name="lastupdated" type="xs:date"/>
<xs:element name="filename" type="xs:string"/>

<!-- definition of simple types -->
<xs:element name="finished">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:enumeration value="Yes"/>
            <xs:enumeration value="No"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<xs:element name="system">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:enumeration value="Linux"/>
            <xs:enumeration value="Mac"/>
            <xs:enumeration value="Windows"/>
            <xs:enumeration value="Other"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<!-- definition of complex types -->
<xs:element name="installer">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="system"/>
            <xs:element ref="lastupdated" minOccurs="0" maxOccurs="1"/>
            <xs:element ref="filename" minOccurs="1" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
</xs:element>

<xs:element name="game">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="title"/>
            <xs:element ref="shop"/>
            <xs:element ref="finished"/>
            <xs:element ref="installer" minOccurs="0" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
</xs:element>

<xs:element name="library">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="game" minOccurs="0" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
    <xs:unique name="uniqueTitle">
        <xs:selector xpath="game/title"/>
        <xs:field xpath="."/>
    </xs:unique>
</xs:element>

</xs:schema>
        """)

        # Write xsd tree to file confschema
        xsdout = etree.ElementTree(xsdroot)
        try:
            xsdout.write(self._xsdfile, xml_declaration=True, encoding="UTF-8", pretty_print=True)
            return 0
        except OSError:
            return 2
    # End of method restore_schema.

    """
    Method: search_elements

    Search for elements containing a given value.
    """
    def search_elements(self, element, value, ascending = True):
        # Validate storage.
        validate = self.validate()
        if validate != 0:
            return validate

        if element not in self._sortingtags:
            return None

        # Create xml tree.
        tree = etree.parse(self._xmlfile)
        # Search for elements containing the value.
        tnodes = tree.xpath("/library/{0}/{1}[contains(., '{2}')]/ancestor::{0}".format(self._libtype, element, value))

        # Return elements if exist or none if list is empty.
        if tnodes:
            # Sort the list.
            index = self._sortingtags.index(element)
            tnodes.sort(key = lambda element: element[index].text.title(), reverse = not ascending)
            return tnodes
        else:
            return None
    # End of method search_elements.

    # Element manipulation methods.
    """
    Method: get_all_elements

    Gets all elements in the specified order.
    """
    def get_all_elements(self, element = None, ascending = True):
        # Validate storage.
        validate = self.validate()
        if validate != 0:
            return validate

        # Create xml tree.
        tree = etree.parse(self._xmlfile)
        # Get a list of all elements.
        tnodes = tree.xpath("/library/{}".format(self._libtype))

        # Return elements if exist or none if list is empty.
        if tnodes:
            # If element is None, title is used.
            if element is None:
                element = "title"
            # Sort the list.
            index = self._sortingtags.index(element)
            tnodes.sort(key = lambda element: element[index].text.title(), reverse = not ascending)
            return tnodes
        else:
            return None
    # End of method get_all_elements.

    """
    Method: get_element

    Gets an element by unique value.
    """
    def get_element(self, element):
        # Validate storage.
        validate = self.validate()
        if validate != 0:
            return validate

        # Create xml tree.
        tree = etree.parse(self._xmlfile)
        # Find node.
        # Scheme validation garanties unique key value, so a list containing
        # only one element on an empty one will be returned.
        tnodes = tree.xpath("/library/{0}/title[text()='{1}']/ancestor::{0}".format(self._libtype, element))

        # Return element if exists or none if list is empty
        if tnodes:
            return tnodes[0]
        else:
            return None
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

    """
    Method: _show_table

    Shows table of elements.
    """
    def _show_table(self, elements):
        # Calculate max column widths.
        titlewidth = 5
        shopwidth = 4
        for item in elements:
            # Title width.
            width = len(item[0].text.strip())
            if titlewidth < width:
                titlewidth = width
            # Shop width.
            width = len(item[1].text.strip())
            if shopwidth < width:
                shopwidth = width
        # Display header.
        print("{:{}} | {:{}} | {:8} | {}".format(self._sortingtags[0].title(), titlewidth, self._sortingtags[1].title(), shopwidth, self._sortingtags[2].title(), "System"))
        print("{}-|-{}-|-{}-|-{}".format("-" * titlewidth, "-" * shopwidth, "-" * 8, "-" * 6))
        # Iterate though result as needed and display game information.
        for item in elements:
            print("{:{}} | {:{}} | {:8} | ".format(item[0].text.strip(), titlewidth, item[1].text.strip(), shopwidth, item[2].text.strip()), end = "")
            for subitem in item:
                if subitem.tag == "installer":
                    print("{} ".format(subitem[0].text.strip()), end = "")
            print()
    # End of method _show_table.

    # Display methods.
    """
    Method: show_search_elements

    Shows elements of a search result.
    """
    def show_search_elements(self, element = None, value = None, ascending = True, menu = None):
        # Get all elements
        if menu is None:
            elements = self.search_elements(element, value, ascending)
        else:
            # Get user input.
            element = self.get_sorting_element()
            value = input("Enter a value to search for: ")
            elements = self.search_elements(element, value, self.get_sorting_order())
        # Display results
        if isinstance(elements, int):
            print("Invalid storage file {}.".format(self._xmlfile))
        elif elements is None:
            print("The library is empty.")
        else:
            # Show table of results.
            self._show_table(elements)
        print()
        # Pause if the method has been called without an element.
        if menu is not None:
            input("Press 'Enter' to return to menu: ")
    # End of method show_search_elements.

    """
    Method: show_all_elements

    Shows all elements.
    """
    def show_all_elements(self, element = None, ascending = True, menu = None):
        # Get all elements
        if menu is None:
            elements = self.get_all_elements(element, ascending)
        else:
            # Get user input.
            elements = self.get_all_elements(self.get_sorting_element(), self.get_sorting_order())
        # Display results
        if isinstance(elements, int):
            print("Invalid storage file {}.".format(self._xmlfile))
        elif elements is None:
            print("The library is empty.")
        else:
            # Show table of results.
            self._show_table(elements)
        print()
        # Pause if the method has been called without an element.
        if menu is not None:
            input("Press 'Enter' to return to menu: ")
    # End of method show_all_elements.

    """
    Method: show_element

    Shows an element.
    Value parameter may be used to pass the title to search programmatically.
    """
    def show_element(self, value = None):
        if value is None:
            # Get user input.
            print("Exact match will be made!")
            title = input("Enter the title of the game: ")
        else:
            # set title using value parameter
            title = value
        # Get element.
        element = self.get_element(title)
        print()
        # Display result.
        if isinstance(element, int):
            print("Invalid storage file {}.".format(self._xmlfile))
        elif element is None:
            print("No game with title {} found.".format(title))
        else:
            # Iterate though result as needed and display game information.
            print("{}:".format(element.tag.title()))
            for item in element.iterchildren():
                if item.text is not None:
                    depth = 4
                    print("{}{}: {}".format(" " * depth, item.tag.title(), item.text.strip()))
                    for subitem in item.iterchildren():
                        if subitem.text is not None:
                            depth = 8
                            print("{}{}: {}".format(" " * depth, subitem.tag.title(), subitem.text.strip()))
        print()
        # Pause if the method has been called without a value.
        if value is None:
            input("Press 'Enter' to return to menu: ")
    # End of method show_element.

    """
    Method: show_element_editor

    Shows the element editor.
    """
    def show_element_editor(self, element = None):
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
