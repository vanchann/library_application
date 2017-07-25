#!/usr/bin/env python3

# imports
import os
import sys
import csv
from lxml import etree
from library.management import Manager
from library.support.utility import Utility

"""
Class: BookManager

Extends class Manager.
The BookManager class uses XML to store and manage book elements.
Contents maybe created, parsed and destroyed.
The class also supports validation of the XML file given an XSD schema, so that
it may be used independently.
"""
class BookManager(Manager):
    """
    Initializer
    """
    def __init__(self, storageroot, libfile, schemafile):
        # Library type.
        libtype = "book"
        # Allow sorting element tags.
        sortingtags = ["title", "author", "category", "format", "isbn", "finished"]
        # Call parent initializer.
        super().__init__(storageroot, libfile, schemafile, libtype, sortingtags)
    # End of initializer.

    # File import and export functionality.
    """
    Method: import_csv

    Imports a CSV file as the XML library file.
    Only fields listed in sortingtags are supported.

    Character set: UTF-8
    Field delimiter: ,
    Text delimiter: \

    Valid CSV header:
    Title,Author,Category,Format,ISBN,Finished

    :param str impfile: the file to import.
    :return int: 0 on success, 1 if CSV header is not valid and 2 in case of filesystem write error.
    """
    def import_csv(self, impfile):
        try:
            # List of books.
            books = []
            with open(impfile, newline="") as csvfile:
                filereader = csv.DictReader(csvfile, quotechar="\\")
                for row in filereader:
                    # Create new element from elementdict.
                    element = etree.Element(self._libtype)
                    # Add subelements.
                    subelement = etree.SubElement(element, "title")
                    subelement.text = row["Title"]
                    # Add author subelements.
                    authors = row["Author"].split(", ")
                    for author in authors:
                        subelement = etree.SubElement(element, "authors")
                        authorelement = etree.SubElement(subelement, "author")
                        authorelement.text = author
                    subelement = etree.SubElement(element, "category")
                    subelement.text = row["Category"]
                    # Add author subelements.
                    formats = row["Format"].split(", ")
                    for bformat in formats:
                        subelement = etree.SubElement(element, "formats")
                        formatelement = etree.SubElement(subelement, "format")
                        authorelement.text = bformat
                    # Add remaining subelements
                    subelement = etree.SubElement(element, "isbn")
                    subelement.text = row["ISBN"]
                    subelement = etree.SubElement(element, "finished")
                    subelement.text = row["Finished"]

                    # Add new element to books list.
                    books.append(element)
                # Write the elements to a new library file.
                wbooks = self._write_tree(books)
                if wbooks != 0:
                    return wbooks
        except OSError:
            return 2
        except KeyError:
            return 1
        # File import was successful.
        return 0
    # End of method import_csv.

    """
    Method: export_csv

    Exports XML library file as a CSV file.
    Only fields listed in sortingtags are supported.

    Character set: UTF-8
    Field delimiter: ,
    Text delimiter: \

    Valid CSV header:
    Title,Author,Category,Format,ISBN,Finished

    :param str expfile: the file to export.
    :return int: 0 on success, 1 if library file is not valid and 2 in case of error.
    """
    def export_csv(self, expfile):
        try:
            # Open CSV file for writing.
            with open(expfile, "w", newline = "") as csvfile:
                filewriter = csv.writer(csvfile, quotechar = "\\", quoting = csv.QUOTE_MINIMAL)
                # Write header row.
                filewriter.writerow([self._sortingtags[0].title(), self._sortingtags[1].title(), self._sortingtags[2].title(),
                                    self._sortingtags[3].title(), self._sortingtags[4].upper(), self._sortingtags[5].title()])
                # Get all items
                items = self.get_all_elements()
                # Check for errors before proceed.
                if isinstance(items, int):
                    return items
                # Write items to CSV file.
                for item in items:
                    authors = []
                    formats = []
                    # Add authors.
                    for author in item[1]:
                        authors.append(author.text)
                    # Add formats.
                    for bformat in item[3]:
                        formats.append(bformat.text)
                    # Write row.
                    filewriter.writerow([item[0].text, ", ".join(authors), item[2].text, ", ".join(formats), item[4].text, item[5].text])
        except OSError:
            return 2
        # File export was successful.
        return 0
    # End of method export_csv.

    # Storage management methods.
    """
    Method: restore_schema

    Restores the library schema file.

    :return int: 0 on success and 2 in case of error.
    """
    def restore_schema(self):
        # Create the xsd tree.
        xsdroot = etree.XML("""
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">

<!-- definition of simple elements -->
<xs:element name="title">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:minLength value="1"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<xs:element name="author">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:minLength value="1"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<xs:element name="category">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:minLength value="1"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<xs:element name="format">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:enumeration value="Hardback"/>
            <xs:enumeration value="Paperback"/>
            <xs:enumeration value="eBook"/>
            <xs:enumeration value="Other"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<xs:element name="isbn">
    <xs:simpleType>
        <xs:restriction base="xs:integer">
            <xs:totalDigits value="13"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<xs:element name="publicationdate" type="xs:date"/>

<xs:element name="pagenumber">
    <xs:simpleType>
        <xs:restriction base="xs:integer">
            <xs:minInclusive value="1"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<xs:element name="lastpageread">
    <xs:simpleType>
        <xs:restriction base="xs:integer">
            <xs:minInclusive value="1"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<xs:element name="publisher">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:minLength value="1"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<xs:element name="edition">
    <xs:simpleType>
        <xs:restriction base="xs:integer">
            <xs:minInclusive value="1"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<xs:element name="shop">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:minLength value="1"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<xs:element name="finished">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:enumeration value="Yes"/>
            <xs:enumeration value="No"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<!-- definition of complex types -->
<xs:element name="authors">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="author" minOccurs="1" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
</xs:element>

<xs:element name="formats">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="format" minOccurs="1" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
</xs:element>

<xs:element name="book">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="title"/>
            <xs:element ref="authors"/>
            <xs:element ref="category"/>
            <xs:element ref="formats"/>
            <xs:element ref="isbn"/>
            <xs:element ref="publicationdate" minOccurs="0" maxOccurs="1"/>
            <xs:element ref="publisher" minOccurs="0" maxOccurs="1"/>
            <xs:element ref="edition" minOccurs="0" maxOccurs="1"/>
            <xs:element ref="pagenumber" minOccurs="0" maxOccurs="1"/>
            <xs:element ref="lastpageread" minOccurs="0" maxOccurs="1"/>
            <xs:element ref="shop" minOccurs="0" maxOccurs="1"/>
            <xs:element ref="finished"/>
        </xs:sequence>
    </xs:complexType>
</xs:element>

<xs:element name="library">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="book" minOccurs="0" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
    <xs:unique name="uniqueIsbn">
        <xs:selector xpath="book/isbn"/>
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

    # Element manipulation methods.
    """
    Method: search_elements

    Search for elements containing a given value.

    :param str element: The element tag containing the value. Should be in _sortingtags list.
    :param str value: The value inside element tag to search for.
    :param bool ascending[=True]: The order to sort the results.
    :return int_or_list_or_None: Union[int, list, None].
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
        tnodes = None
        if element == "author" or element == "format":
            tnodes = tree.xpath("/library/{0}/{1}s/{1}[contains(., '{2}')]/ancestor::{0}".format(self._libtype, element, value))
        else:
            tnodes = tree.xpath("/library/{0}/{1}[contains(., '{2}')]/ancestor::{0}".format(self._libtype, element, value))

        # Return elements if exist or none if list is empty.
        if tnodes:
            # Sort the list.
            index = self._sortingtags.index(element)
            if element == "author" or element == "format":
                # Sort by the first listed author or format.
                tnodes.sort(key = lambda element: element[index][0].text.title(), reverse = not ascending)
            else:
                tnodes.sort(key = lambda element: element[index].text.title(), reverse = not ascending)
            return tnodes
        else:
            return None
    # End of method search_elements.

    """
    Method: get_all_elements

    Gets all elements in the specified order.

    :param str element[=None]: The element tag on which get will be based. Should be in _sortingtags list.
    :param bool ascending[=True]: The order to sort the results.
    :return int_or_list_or_None: Union[int, list, None].
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
            if element == "author" or element == "format":
                # Sort by the first listed author or format.
                tnodes.sort(key = lambda element: element[index][0].text.title(), reverse = not ascending)
            else:
                tnodes.sort(key = lambda element: element[index].text.title(), reverse = not ascending)
            return tnodes
        else:
            return None
    # End of method get_all_elements.

    """
    Method: get_element

    Gets an element by unique value.

    :param str element: The exact value in element isbn.
    :return int_or_etree.Element_or_None: Union[int, etree.Element, None].
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
        tnodes = tree.xpath("/library/{0}/isbn[text()='{1}']/ancestor::{0}".format(self._libtype, element))

        # Return element if exists or none if list is empty
        if tnodes:
            return tnodes[0]
        else:
            return None
    # End of method get_element.

# End of class BookManager.

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
