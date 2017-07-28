#!/usr/bin/env python3

# imports
import os
import sys
import csv
from lxml import etree
from library.management import Manager
from library.support.utility import Utility

"""
Class: VideoManager

Extends class Manager.
The VideoManager class uses XML to store and manage video elements.
Contents maybe created, parsed and destroyed.
The class also supports validation of the XML file given an XSD schema, so that
it may be used independently.
"""
class VideoManager(Manager):
    """
    Initializer
    """
    def __init__(self, storageroot, libfile, schemafile):
        # Library type.
        libtype = "video"
        # Allow sorting element tags.
        sortingtags = ["title", "format"]
        uniquekey = "title"
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
    Title,Format

    :param str impfile: the file to import.
    :return int: 0 on success, 1 if CSV header is not valid and 2 in case of filesystem write error.
    """
    def import_csv(self, impfile):
        try:
            # List of video items.
            videoitems = []
            with open(impfile, newline="") as csvfile:
                filereader = csv.DictReader(csvfile, quotechar="\\")
                for row in filereader:
                    # Create new element from elementdict.
                    element = etree.Element(self._libtype)
                    # Add subelements.
                    subelement = etree.SubElement(element, "title")
                    subelement.text = row["Title"]
                    # Add format subelements.
                    formats = row["Format"].split(", ")
                    subelement = etree.SubElement(element, "formats")
                    for bformat in formats:
                        formatelement = etree.SubElement(subelement, "format")
                        formatelement.text = bformat
                    # Add new element to videoitems list.
                    videoitems.append(element)
                # Write the elements to a new library file.
                wvideoitems = self._write_tree(videoitems)
                if wvideoitems != 0:
                    return wvideoitems
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
    Title,Format

    :param str expfile: the file to export.
    :return int: 0 on success, 1 if library file is not valid and 2 in case of error.
    """
    def export_csv(self, expfile):
        try:
            # Open CSV file for writing.
            with open(expfile, "w", newline = "") as csvfile:
                filewriter = csv.writer(csvfile, quotechar = "\\", quoting = csv.QUOTE_MINIMAL)
                # Write header row.
                filewriter.writerow([self._sortingtags[0].title(),
                                     self._sortingtags[1].title()])
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
                    formats = []
                    # Add formats.
                    for bformat in item[1]:
                        formats.append(bformat.text)
                    # Write row.
                    filewriter.writerow([item[0].text, ", ".join(formats)])
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

<xs:element name="genre">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:minLength value="1"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<xs:element name="format">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:enumeration value="DVD"/>
            <xs:enumeration value="MP4"/>
            <xs:enumeration value="AVI"/>
            <xs:enumeration value="Blu-ray"/>
            <xs:enumeration value="Other"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<xs:element name="releasedate" type="xs:date"/>

<xs:element name="label">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:minLength value="1"/>
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


<!-- definition of complex types -->
<xs:element name="genres">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="genre" minOccurs="1" maxOccurs="unbounded"/>
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

<xs:element name="video">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="title"/>
            <xs:element ref="formats"/>
            <xs:element ref="genres" minOccurs="0" maxOccurs="1"/>
            <xs:element ref="releasedate" minOccurs="0" maxOccurs="1"/>
            <xs:element ref="label" minOccurs="0" maxOccurs="1"/>
            <xs:element ref="shop" minOccurs="0" maxOccurs="1"/>
        </xs:sequence>
    </xs:complexType>
</xs:element>

<xs:element name="library">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="video" minOccurs="0" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
    <xs:unique name="uniqueTitle">
        <xs:selector xpath="video/title"/>
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
        if element == "format":
            tnodes = tree.xpath("/library/{0}/{1}s/{1}[contains(., '{2}')]/ancestor::{0}".format(self._libtype, element, value))
        else:
            tnodes = tree.xpath("/library/{0}/{1}[contains(., '{2}')]/ancestor::{0}".format(self._libtype, element, value))

        # Return elements if exist or none if list is empty.
        if tnodes:
            # Sort the list.
            index = self._sortingtags.index(element)
            if element == "format":
                # Sort by the first listed format.
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
            if element == "format":
                # Sort by the first listed format.
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

    :param str element: The exact value in element title.
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

    Python dictionary form:
    {
        "title": "", "formats": [""], "genres": [""],
        "releasedate": "YYYY-MM-DD", "label": "", "shop": ""
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
            # Add format subelements.
            subelement = etree.SubElement(element, "formats")
            for bformat in elementdict["formats"]:
                formatelement = etree.SubElement(subelement, "format")
                formatelement.text = bformat
            # Add optional subelements.
            if "genres" in elementdict:
                subelement = etree.SubElement(element, "genres")
                for genre in elementdict["genres"]:
                    genreelement = etree.SubElement(subelement, "genre")
                    genreelement.text = genre
            if "releasedate" in elementdict:
                subelement = etree.SubElement(element, "releasedate")
                subelement.text = elementdict["releasedate"]
            if "label" in elementdict:
                subelement = etree.SubElement(element, "label")
                subelement.text = elementdict["label"]
            if "shop" in elementdict:
                subelement = etree.SubElement(element, "shop")
                subelement.text = elementdict["shop"]
            # Write to file.
            return self._add_element_to_tree(element)
        except KeyError:
            return 1
    # End of method add_element.

    """
    Method: remove_element

    Removes an element.

    :param str element: The exact value in element title.
    :return int: 0 on success, 1 in case no node found, 2 on write file error and 3 on validation error.
    """
    def remove_element(self, element):
        # Create xml tree.
        tree = etree.parse(self._xmlfile)
        # Get a list of all elements.
        nodes = tree.xpath("/library/{}".format(self._libtype))
        # Find the element to remove using exact match.
        node = tree.xpath("/library/{0}/title[text()='{1}']/ancestor::{0}".format(self._libtype, element))
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
        formatwidth = 6
        genrewidth = 5
        # Prepare for displaying.
        for item in elements:
            # Title width.
            width = len(item[0].text.strip())
            if titlewidth < width:
                titlewidth = width
            # Format width.
            formats = []
            for bformat in item[1]:
                formats.append(bformat.text.strip())
            width = len(", ".join(formats))
            if formatwidth < width:
                formatwidth = width
            # Genre width.
            if len(item) > 2 and item[2].tag == "genres":
                genres = []
                for genre in item[2]:
                    genres.append(genre.text.strip())
                width = len(", ".join(genres))
                if genrewidth < width:
                    genrewidth = width
        # Display header.
        print("{:{}} | {:{}} | {:{}}".format(
                self._sortingtags[0].title(), titlewidth,
                self._sortingtags[1].title(), formatwidth,
                "Genre", genrewidth))
        print("{}-|-{}-|-{}".format(
                "-" * titlewidth, "-" * formatwidth, "-" * genrewidth))
        # Iterate though result as needed and display video item information.
        for item in elements:
            formats = []
            genrestr = ""
            for bformat in item[1]:
                formats.append(bformat.text.strip())
            formatstr = ", ".join(formats)
            if len(item) > 2 and item[2].tag == "genres":
                genres = []
                for genre in item[2]:
                    genres.append(genre.text.strip())
                genrestr = ", ".join(genres)
            print("{:{}} | {:{}} | {:{}}".format(
                item[0].text.strip(), titlewidth,
                formatstr, formatwidth,
                genrestr, genrewidth))
    # End of method show_table.

    # Display methods.
    """
    Method: show_element

    Shows an element.

    :param str value[=None]: The exact value in element title.
    """
    def show_element(self, value = None):
        if value is None:
            # Get user input.
            print("Exact match will be made!")
            title = input("Enter the item's title: ")
            print()
        else:
            # set title using value parameter
            title = value
        # Get element.
        element = self.get_element(title)
        # Display result.
        if isinstance(element, int):
            print("Invalid storage file {}.".format(self._xmlfile))
        elif element is None:
            print("No item with title '{}' found.".format(title))
        else:
            # Iterate though result as needed and display video item information.
            print("{}:".format(element.tag.title()))
            for item in element.iterchildren():
                # Making sure formats and genres tags have text,
                # so that they will be iterated.
                if item.tag == "formats":
                    item.text = " "
                if item.tag == "genres":
                    item.text = " "

                if item.text is not None:
                    depth = 4
                    print("{}{}: {}".format(" " * depth, item.tag.title(), item.text.strip()))
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

    Generates python dictionary from video xml element.

    :param etree.Element element: The video element node.
    :return dict: The python dictionary version of the XML node.
    """
    def _xmlitem_to_dict(self, element):
        # Create python dictionary parsing element's values.
        videodict = {}
        genres = None
        for item in element.iterchildren():
            # Making sure formats, genres and tracks tags have text,
            # so that they will be iterated.
            if item.tag == "formats":
                item.text = " "
            if item.tag == "genres":
                item.text = " "

            # Elements in video.
            if item.text is not None:
                videodict[item.tag] = item.text.strip()
                if item.tag == "formats":
                    formats = []
                    # Elements in formats.
                    for subitem in item.iterchildren():
                        if subitem.text is not None:
                            formats.append(subitem.text.strip())
                if item.tag == "genres":
                    genres = []
                    # Elements in genres.
                    for subitem in item.iterchildren():
                        if subitem.text is not None:
                            genres.append(subitem.text.strip())

        # Add lists to video dictionary.
        videodict["formats"] = formats
        if genres:
            videodict["genres"] = genres

        return videodict
    # End of method _xmlitem_to_dict.

    """
    Method: _generate_libtype_element

    Generate video python dictionary.

    Python dictionary form:
    {
        "title": "", "formats": [""], "genres": [""],
        "releasedate": "YYYY-MM-DD", "label": "", "shop": ""
    }

    :param dict element[=None]: The python dictionary containing the values of the element.
    :return dict: The python dictionary containing new values.
    """
    def _generate_libtype_element(self, element = None):
        # Display header.
        if element is None:
            print("New", end = " ")
            element = {"title": None, "formats": None}
        print("video Item Editor")
        print()
        # Get item's elements.
        title = ""
        while title == "":
            title = input("Title{}: ".format("" if element["title"] is None else "[" + element["title"] + "]"))
            if element["title"] is not None and title == "":
                title = element["title"]
        # Exit editor if the user is trying to create an item, which already exists.
        if element["title"] is None and self.get_element(title) is not None:
            print("Item {} already exists.".format(title))
            return None
        # Exit editor if new title already exists.
        if element["title"] is not None:
            if title != element["title"] and self.get_element(title) is not None:
                print("Title '{}' has already been used for an item.".format(title))
                return None

        element["title"] = title

        # Edit mandatory lists.
        element = self._generate_list(element, "formats", ["DVD", "MP4", "AVI", "Blu-ray", "Other"])
        # Edit optional lists.
        element = self._generate_list(element, "genres", mandatory = False)

        # Edit optional elements.
        releasedate = None
        while releasedate is None:
            releasedate = input("Publication date{} [YYYY-MM-DD or leave empty to remove]: ".format("[" + element["releasedate"] + "]" if "releasedate" in element else ""))
            if releasedate == "":
                if "releasedate" in element:
                    del element["releasedate"]
            else:
                releasedate = Utility.validate_date(releasedate)
                if releasedate is not None:
                    element["releasedate"] = releasedate

        element = self._edit_optional_tag(element, "label")
        element = self._edit_optional_tag(element, "shop")

        # Return video item dictionary.
        return element
    # End of method _generate_libtype_element.

    """
    Method: _generate_list

    Generates list for a mandatory python dictionary key.

    Python dictionary form:
    {
        "title": "", "formats": [""], "genres": [""],
        "releasedate": "YYYY-MM-DD", "label": "", "shop": ""
    }

    :param dict element: The python dictionary containing the values of the element.
    :param str tag: The dictionary key, which holds the list.
    :param list values: The list of valid values.
    :param bool mandatory[=True]: Indicates if tag is mandatory in the dictionary.
    :return dict: The python dictionary containing edited list.
    """
    def _generate_list(self, element, tag, values = None, mandatory = True):
        removelist = []
        # Get items.
        if tag in element and element[tag] is not None:
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
        if mandatory:
            while element[tag] is None or len(element[tag]) == 0:
                print("At least one {} is required".format(tag[:-1]))
                element = self._get_list_values(element, tag, values)
        # Remove tag if it's empty.
        if tag in element and len(element[tag]) == 0:
            del element[tag]
        return element
    # End of method _generate_list.

    """
    Method: _get_list_values

    Gets new values from the user and add the to a list in the dictionary.

    Python dictionary form:
    {
        "title": "", "formats": [""], "genres": [""],
        "releasedate": "YYYY-MM-DD", "label": "", "shop": ""
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
            if tag not in element or element[tag] is None:
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
# End of class VideoManager.

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
