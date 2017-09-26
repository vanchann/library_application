#!/usr/bin/env python3

# imports
import os
import sys
import csv
import re
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
        uniquekey = "isbn"
        # Call parent initializer.
        super().__init__(storageroot, libfile, schemafile, libtype, sortingtags, uniquekey)
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
                    subelement = etree.SubElement(element, "authors")
                    for author in authors:
                        authorelement = etree.SubElement(subelement, "author")
                        authorelement.text = author
                    subelement = etree.SubElement(element, "category")
                    subelement.text = row["Category"]
                    # Add format subelements.
                    formats = row["Format"].split(", ")
                    subelement = etree.SubElement(element, "formats")
                    for bformat in formats:
                        formatelement = etree.SubElement(subelement, "format")
                        formatelement.text = bformat
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
                # Check if library is empty.
                if items is None:
                    return 0
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
                    filewriter.writerow([item[0].text, ", ".join(authors), item[2].text, ", ".join(formats), item[4].text, item[-1].text])
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
            tnodes = tree.xpath("/library/{0}/{1}s/{1}[contains(translate(., '{3}', '{4}'), '{2}')]/ancestor::{0}".format(self._libtype, element, value.lower(), self._uppercase, self._lowercase))
        else:
            tnodes = tree.xpath("/library/{0}/{1}[contains(translate(., '{3}', '{4}'), '{2}')]/ancestor::{0}".format(self._libtype, element, value.lower(), self._uppercase, self._lowercase))

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

    """
    Method: add_element

    Adds an element.

    Python dictionary form:
    {
        "title": "", "authors": [""], "category": "", "formats": [""], "isbn": "",
        "publicationdate": "YYYY-MM-DD", "publisher": "", "edition": "",
        "pagenumber": "", "lastpageread": "", "shop": "", "finished": "Yes/No"
    }

    :param dict elementdict: The python dictionary containing the values of the element to be added to library.
    :return int: 0 on success, 1 on dictionary key error, 2 on write file error and 3 on validation error.
    """
    def add_element(self, elementdict):
        # Create new element from elementdict.
        element = etree.Element(self._libtype)
        try:
            subelement = etree.SubElement(element, "title")
            subelement.text = elementdict["title"]
            # Add author subelements.
            subelement = etree.SubElement(element, "authors")
            for author in elementdict["authors"]:
                authorelement = etree.SubElement(subelement, "author")
                authorelement.text = author
            subelement = etree.SubElement(element, "category")
            subelement.text = elementdict["category"]
            # Add format subelements.
            subelement = etree.SubElement(element, "formats")
            for bformat in elementdict["formats"]:
                formatelement = etree.SubElement(subelement, "format")
                formatelement.text = bformat
            subelement = etree.SubElement(element, "isbn")
            subelement.text = elementdict["isbn"]
            # Add optional subelements.
            if "publicationdate" in elementdict:
                subelement = etree.SubElement(element, "publicationdate")
                subelement.text = elementdict["publicationdate"]
            if "publisher" in elementdict:
                subelement = etree.SubElement(element, "publisher")
                subelement.text = elementdict["publisher"]
            if "edition" in elementdict:
                subelement = etree.SubElement(element, "edition")
                subelement.text = elementdict["edition"]
            if "pagenumber" in elementdict:
                subelement = etree.SubElement(element, "pagenumber")
                subelement.text = elementdict["pagenumber"]
            if "lastpageread" in elementdict:
                subelement = etree.SubElement(element, "lastpageread")
                subelement.text = elementdict["lastpageread"]
            if "shop" in elementdict:
                subelement = etree.SubElement(element, "shop")
                subelement.text = elementdict["shop"]
            subelement = etree.SubElement(element, "finished")
            subelement.text = elementdict["finished"]
            # Write to file.
            return self._add_element_to_tree(element)
        except KeyError:
            return 1
    # End of method add_element.

    """
    Method: remove_element

    Removes an element.

    :param str element: The exact value in element isbn.
    :return int: 0 on success, 1 in case no node found, 2 on write file error and 3 on validation error.
    """
    def remove_element(self, element):
        # Create xml tree.
        tree = etree.parse(self._xmlfile)
        # Get a list of all elements.
        nodes = tree.xpath("/library/{}".format(self._libtype))
        # Find the element to remove using exact match.
        node = tree.xpath("/library/{0}/isbn[text()='{1}']/ancestor::{0}".format(self._libtype, element))
        if not node:
            return 1
        # Remove element's node.
        nodes.remove(node[0])
        # Write to file.
        return self._write_tree(nodes)
    # End of method remove_element.

    """
    Method: show_table

    Shows table of elements.

    :param list elements: List of etree.Element to be shown.
    """
    def show_table(self, elements):
        # Calculate max column widths.
        titlewidth = 5
        authorwidth = 6
        categorywidth = 8
        formatwidth = 6
        isbnwidth = 13
        finishedwidth = 8
        # Prepare for displaying.
        for item in elements:
            # Title width.
            width = len(item[0].text.strip())
            if titlewidth < width:
                titlewidth = width
            # Author width.
            authors = []
            for author in item[1]:
                authors.append(author.text.strip())
            width = len(", ".join(authors))
            if authorwidth < width:
                authorwidth = width
            # Category width.
            width = len(item[2].text.strip())
            if categorywidth < width:
                categorywidth = width
            # Format width.
            formats = []
            for bformat in item[3]:
                formats.append(bformat.text.strip())
            width = len(", ".join(formats))
            if formatwidth < width:
                formatwidth = width
        # Display header.
        print("{:{}} | {:{}} | {:{}} | {:{}} | {:{}} | {:{}}".format(
                self._sortingtags[0].title(), titlewidth,
                self._sortingtags[1].title(), authorwidth,
                self._sortingtags[2].title(), categorywidth,
                self._sortingtags[3].title(), formatwidth,
                self._sortingtags[4].title(), isbnwidth,
                self._sortingtags[5].title(), finishedwidth))
        print("{}-|-{}-|-{}-|-{}-|-{}-|-{}".format(
                "-" * titlewidth, "-" * authorwidth, "-" * categorywidth,
                "-" * formatwidth, "-" * isbnwidth, "-" * finishedwidth))
        # Iterate though result as needed and display book information.
        for item in elements:
            authors = []
            for author in item[1]:
                authors.append(author.text.strip())
            authorstr = ", ".join(authors)
            formats = []
            for bformat in item[3]:
                formats.append(bformat.text.strip())
            formatstr = ", ".join(formats)
            print("{:{}} | {:{}} | {:{}} | {:{}} | {:{}} | {:{}}".format(
                item[0].text.strip(), titlewidth,
                authorstr, authorwidth,
                item[2].text.strip(), categorywidth,
                formatstr, formatwidth,
                item[4].text.strip(), isbnwidth,
                item[-1].text.strip(), finishedwidth))
    # End of method show_table.

    # Display methods.
    """
    Method: show_element

    Shows an element.

    :param str value[=None]: The exact value in element isbn.
    """
    def show_element(self, value = None):
        if value is None:
            # Get user input.
            print("Exact match will be made!")
            isbn = input("Enter the book's isbn: ")
            print()
        else:
            # set isbn using value parameter
            isbn = value
        # Get element.
        element = self.get_element(isbn)
        # Display result.
        if isinstance(element, int):
            print("Invalid storage file {}.".format(self._xmlfile))
        elif element is None:
            print("No book with isbn '{}' found.".format(isbn))
        else:
            # Iterate though result as needed and display book information.
            print("{}:".format(element.tag.title()))
            for item in element.iterchildren():
                # Making sure authors and formats tags have text,
                # so that they will be iterated.
                if item.tag == "authors":
                    item.text = " "
                if item.tag == "formats":
                    item.text = " "

                if item.text is not None:
                    depth = 4
                    print("{}{}: {}".format(" " * depth, item.tag.upper() if item.tag == "isbn" else item.tag.title(), item.text.strip()))
                    for subitem in item.iterchildren():
                        if subitem.text is not None:
                            depth = 8
                            print("{}{}".format(" " * depth, subitem.text.strip()))

        # Pause if the method has been called without a value.
        if value is None:
            print()
            input("Press 'Enter' to return to menu: ")
    # End of method show_element.

    """
    Method: _xmlitem_to_dict

    Generates python dictionary from book xml element.

    :param etree.Element element: The book element node.
    :return dict: The python dictionary version of the XML node.
    """
    def _xmlitem_to_dict(self, element):
        # Create python dictionary parsing element's values.
        bookdict = {}
        for item in element.iterchildren():
            # Making sure authors and formats tags have text,
            # so that they will be iterated.
            if item.tag == "authors":
                item.text = " "
            if item.tag == "formats":
                item.text = " "

            # Elements in book.
            if item.text is not None:
                bookdict[item.tag] = item.text.strip()
                if item.tag == "authors":
                    authors = []
                    # Elements in authors.
                    for subitem in item.iterchildren():
                        if subitem.text is not None:
                            authors.append(subitem.text.strip())
                if item.tag == "formats":
                    formats = []
                    # Elements in formats.
                    for subitem in item.iterchildren():
                        if subitem.text is not None:
                            formats.append(subitem.text.strip())
        # Add lists to book dictionary.
        bookdict["authors"] = authors
        bookdict["formats"] = formats

        return bookdict
    # End of method _xmlitem_to_dict.

    """
    Method: _generate_libtype_element

    Generate book python dictionary.

    Python dictionary form:
    {
        "title": "", "authors": [""], "category": "", "formats": [""], "isbn": "",
        "publicationdate": "YYYY-MM-DD", "publisher": "", "edition": "",
        "pagenumber": "", "lastpageread": "", "shop": "", "finished": "Yes/No"
    }

    :param dict element[=None]: The python dictionary containing the values of the element.
    :return dict: The python dictionary containing new values.
    """
    def _generate_libtype_element(self, element = None):
        # Display header.
        if element is None:
            print("New", end = " ")
            element = {"title": None, "authors": None, "category": None,
                       "formats": None, "isbn": None, "finished": None}
        print("Book Editor")
        print()
        # Get book's elements.
        isbn = ""
        while isbn == "":
            isbn = input("ISBN{}: ".format("" if element["isbn"] is None else "[" + element["isbn"] + "]"))
            if element["isbn"] is not None and isbn == "":
                isbn = element["isbn"]
            # Check if ISBN has 13 digits.
            pattern = re.compile("^\d{13}$")
            match = pattern.match(isbn)
            if match is None:
                print("ISBN should be 13 digits.".format(isbn))
                return None
        # Exit editor if the user is trying to create a book, which already exists.
        if element["isbn"] is None and self.get_element(isbn) is not None:
            print("Book {} already exists.".format(isbn))
            return None
        # Exit editor if new isbn already exists.
        if element["isbn"] is not None:
            if isbn != element["isbn"] and self.get_element(isbn) is not None:
                print("ISBN '{}' has already been used for a book.".format(isbn))
                return None

        element["isbn"] = isbn

        # Edit mandatory elements.
        element = self._edit_mandatory_tag(element, "title")
        element = self._edit_mandatory_tag(element, "category")

        # Edit mandatory lists.
        element = self._generate_mandatory_list(element, "authors")
        element = self._generate_mandatory_list(element, "formats", ["Hardback", "Paperback", "eBook", "Other"])

        finished = Utility.get_answer_yn("Finished{}:".format("" if element["finished"] is None else "[" + element["finished"] + "]"))
        if finished == "y":
            element["finished"] = "Yes"
        else:
            element["finished"] = "No"

        # Edit optional elements.
        publicationdate = None
        while publicationdate is None:
            publicationdate = input("Publication date{} [YYYY-MM-DD or leave empty to remove]: ".format("[" + element["publicationdate"] + "]" if "publicationdate" in element else ""))
            if publicationdate == "":
                if "publicationdate" in element:
                    del element["publicationdate"]
            else:
                publicationdate = Utility.validate_date(publicationdate)
                if publicationdate is not None:
                    element["publicationdate"] = publicationdate

        element = self._edit_optional_tag(element, "publisher")
        element = self._edit_optional_tag(element, "edition")
        element = self._edit_optional_tag(element, "pagenumber")
        element = self._edit_optional_tag(element, "lastpageread")
        element = self._edit_optional_tag(element, "shop")

        # Return book dictionary.
        return element
    # End of method _generate_libtype_element.

    """
    Method: _generate_mandatory_list

    Generates list for a mandatory python dictionary key.

    Python dictionary form:
    {
        "title": "", "authors": [""], "category": "", "formats": [""], "isbn": "",
        "publicationdate": "YYYY-MM-DD", "publisher": "", "edition": "",
        "pagenumber": "", "lastpageread": "", "shop": "", "finished": "Yes/No"
    }

    :param dict element: The python dictionary containing the values of the element.
    :param str tag: The dictionary key, which holds the list.
    :param list values: The list of valid values.
    :return dict: The python dictionary containing edited list.
    """
    def _generate_mandatory_list(self, element, tag, values = None):
        removelist = []
        # Get items.
        if element[tag] is not None:
            for item in element[tag]:
                # Get action from the user.
                choices = range(1, 3)
                choice = None
                # Generate menu
                # Display menu
                print("{}: {}".format(tag[:-1].title(), item))
                print("1. Keep and continue")
                print("2. Remove")
                while choice not in choices:
                    # Get user choice.
                    try:
                        choice = int(input("Enter your choice: "))
                    except ValueError:
                        choice = None

                    # React to user choice.
                    if choice == 1:
                        # Pass for 1.
                        # Alternatively break out of the loop.
                        pass
                    elif choice == 2:
                        removelist.append(item)
                        print("'{}' has been removed.".format(item))
                    else:
                        choice = None
            # Remove marked items permanently.
            for rvalue in removelist:
                element[tag].remove(rvalue)
        # Add new items.
        element = self._get_list_values(element, tag, values)
        # Mandatory list cannot be empty.
        while element[tag] is None or len(element[tag]) == 0:
            print("At least one {} is required".format(tag[:-1]))
            element = self._get_list_values(element, tag, values)

        return element
    # End of method _generate_mandatory_list.

    """
    Method: _get_list_values

    Gets new values from the user and add the to a list in the dictionary.

    Python dictionary form:
    {
        "title": "", "authors": [""], "category": "", "formats": [""], "isbn": "",
        "publicationdate": "YYYY-MM-DD", "publisher": "", "edition": "",
        "pagenumber": "", "lastpageread": "", "shop": "", "finished": "Yes/No"
    }

    :param dict element: The python dictionary containing the values of the element.
    :param str tag: The dictionary key, which holds the list.
    :param list values: The list of valid values.
    :return dict: The python dictionary containing new list values.
    """
    def _get_list_values(self, element, tag, values = None):
        # If values come from a list call _get_list_values_from_list.
        if values is not None:
            return self._get_list_values_from_list(element, tag, values)
        # Allow free input.
        # Add new values.
        values = []
        value = "Enter Loop"
        while value != "":
            value = input("Add {} [leave empty to stop]: ".format(tag[:-1].title()))
            value = value.strip()
            if value != "":
                values.append(value)
        # Add values to element.
        if values:
            if element[tag] is None:
                element[tag] = values
            else:
                element[tag] += values

        return element
    # End of method _get_list_values.

    """
    Method: _edit_mandatory_tag

    Edits or generates a mandatory tag of an element.

    :param dict element[=None]: The python dictionary containing the values of the element.
    :param str tag: The dictionary key, which holds the list.
    :return dict: The python dictionary containing new values.
    """
    def _edit_mandatory_tag(self, element, tag):
        value = ""
        while value == "":
            value = input("{}{}: ".format(tag.title(),"" if element[tag] is None else "[" + element[tag] + "]"))
            if element[tag] is not None and value == "":
                value = element[tag]
        element[tag] = value
        return element
    # End of method _edit_mandatory_tag.

    """
    Method: _edit_optional_tag

    Edits, generates or removes an optional tag of an element.
    Values may be typed in freely.

    :param dict element[=None]: The python dictionary containing the values of the element.
    :param str tag: The dictionary key, which holds the list.
    :return dict: The python dictionary containing new values.
    """
    def _edit_optional_tag(self, element, tag):
        choice = Utility.get_answer_yn("{} {}:".format("Edit" if tag in element else "Create", tag))
        if choice == "y":
            value = input("{}{} [leave empty to remove]: ".format(tag, "[" + element[tag] + "]" if tag in element else ""))
            if value == "":
                # Remove tag if exists.
                if tag in element:
                    del element[tag]
                return element
            element[tag] = value
        return element
    # End of method _edit_optional_tag.

    """
    Method: _get_list_values_from_list

    Gets new values from the user and add the to a list in the dictionary.
    Values may be selected from a list only.

    :param dict element[=None]: The python dictionary containing the values of the element.
    :param str tag: The dictionary key, which holds the list.
    :param list values: The list of valid values.
    :return dict: The python dictionary containing new values.
    """
    def _get_list_values_from_list(self, element, tag, values):
        # Display menu.
        choice = None
        choices = []
        print("Valid {}: ".format(tag))
        for value in values:
            print("{}. {}".format(values.index(value) + 1, value))
        while choice is None:
            # Get user choice.
            choice = input("Enter your choice[leave empty to stop]: ")
            if choice != "":
                try:
                    choice = int(choice)
                    if choice > 0:
                        choices.append(values[choice - 1])
                    else:
                        raise ValueError
                except IndexError:
                    print("Invalid index {}.".format(choice))
                except ValueError:
                    print("Invalid input {}. Only listed numbers are valid.".format(choice))
                choice = None
        # Add choices to element.
        if choices:
            if element[tag] is None:
                element[tag] = choices
            else:
                element[tag] += choices
        return element
    # End of method _get_list_values_from_list.
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
