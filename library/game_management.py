#!/usr/bin/env python3

# imports
import os
import sys
from lxml import etree
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
        # Create the xsd tree.
        xsdroot = etree.XML("""
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">

<!-- definition of simple elements -->
<xs:element name="title" type="xs:string">
    <xs:unique name="uniqueTitle">
        <xs:selector xpath="title"/>
        <xs:field xpath="."/>
    </xs:unique>
</xs:element>
<xs:element name="shop" type="xs:string"/>
<xs:element name="finished" type="xs:boolean" default="false"/>
<xs:element name="lastupdated" type="xs:date"/>
<xs:element name="filename" type="xs:string"/>

<!-- definition of simple types -->
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
