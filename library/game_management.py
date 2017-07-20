#!/usr/bin/env python3

# imports
import os
import sys
from lxml import etree
from library.management import Manager
from library.support.utility import Utility

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
    # End of initializer.

    # File import and export functionality.
    """
    Method: import_csv

    Imports a CSV file as the XML library file.

    :return int: 0 on success and 2 in case of error.
    :raise NotImplementedError: Method should be implemented.
    """
    def import_csv(self):
        raise NotImplementedError("Method import_csv should be implemented in child class.")
        """
        try:
            return 0
        except OSError:
            return 2
        """
    # End of method import_csv.

    """
    Method: export_csv

    Exports XML library file as a CSV file.

    :return int: 0 on success and 2 in case of error.
    :raise NotImplementedError: Method should be implemented.
    """
    def export_csv(self):
        raise NotImplementedError("Method export_csv should be implemented in child class.")
        """
        try:
            return 0
        except OSError:
            return 2
        """
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

<xs:element name="shop">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:minLength value="1"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<xs:element name="lastupdated" type="xs:date"/>

<xs:element name="filename">
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
            <xs:element ref="filename" minOccurs="0" maxOccurs="unbounded"/>
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
    :return int: 0 on success, 2 on write file error and 3 on validation error.
    """
    def _add_element_to_tree(self, element):
            # Create xml tree.
            tree = etree.parse(self._xmlfile)
            # Get a list of all elements.
            nodes = tree.xpath("/library/{}".format(self._libtype))
            # Append to lis.
            nodes.append(element)
            # Sort elements list by title.
            index = self._sortingtags.index("title")
            nodes.sort(key = lambda element: element[index].text.title())
            # Write to file.
            return self._write_tree(nodes)
    # End of method _add_element_to_tree.

    """
    Method: add_element

    Adds an element.

    Python dictionary form:
    {
        "title": "", "shop": "", "finished": "Yes/No",
        "installer": [
            {"system": "", "lastupdated": "YYYY-MM-DD", "filename": [""]}
        ]
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
            subelement = etree.SubElement(element, "shop")
            subelement.text = elementdict["shop"]
            subelement = etree.SubElement(element, "finished")
            subelement.text = elementdict["finished"]

            # Get installer list.
            if "installer" in elementdict:
                for installer in elementdict["installer"]:
                    installertag = etree.SubElement(element, "installer")
                    subelement = etree.SubElement(installertag, "system")
                    subelement.text = installer["system"]
                    if "lastupdated" in installer:
                        subelement = etree.SubElement(installertag, "lastupdated")
                        subelement.text = installer["lastupdated"]
                    # Get filename list
                    if "filename" in installer:
                        for filename in installer["filename"]:
                            subelement = etree.SubElement(installertag, "filename")
                            subelement.text = filename
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
        nodes.remove(node[0])
        # Remove element's node.
        #nodes = node.getparent()
        #nodes.remove(node)
        # Write to file.
        return self._write_tree(nodes)
    # End of method remove_element.

    """
    Method: _show_table

    Shows table of elements.

    :param list elements: List of etree.Element to be shown.
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
            print("No item with '{}' containing '{}' has benn found.".format(element.title(), value))
        else:
            # Show table of results.
            self._show_table(elements)
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
            self._show_table(elements)
        # Pause if the method has been called without an element.
        if menu is not None:
            print()
            input("Press 'Enter' to return to menu: ")
    # End of method show_all_elements.

    """
    Method: show_element

    Shows an element.

    :param str value[=None]: The exact value in element title.
    """
    def show_element(self, value = None):
        if value is None:
            # Get user input.
            print("Exact match will be made!")
            title = input("Enter the title of the game: ")
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
            print("No game with title {} found.".format(title))
        else:
            # Iterate though result as needed and display game information.
            print("{}:".format(element.tag.title()))
            for item in element.iterchildren():
                # Making sure installer tag has text, so that it will be iterated.
                if item.tag == "installer":
                    item.text = " "

                if item.text is not None:
                    depth = 4
                    print("{}{}: {}".format(" " * depth, item.tag.title(), item.text.strip()))
                    for subitem in item.iterchildren():
                        if subitem.text is not None:
                            depth = 8
                            print("{}{}: {}".format(" " * depth, subitem.tag.title(), subitem.text.strip()))
        # Pause if the method has been called without a value.
        if value is None:
            print()
            input("Press 'Enter' to return to menu: ")
    # End of method show_element.

    """
    Method: show_add_element

    Shows messages about new element's addition.

    Python dictionary form:
    {
        "title": "", "shop": "", "finished": "Yes/No",
        "installer": [
            {"system": "", "lastupdated": "YYYY-MM-DD", "filename": [""]}
        ]
    }

    :param str element[=None]: The python dictionary containing the values of the element to be added to library.
    """
    def show_add_element(self, element = None):
        menu = None
        # Get the element's title from the user.
        if element is None:
            menu = True
            Utility.clear()
            # Generate new element.
            element = self._generate_game()
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

    Python dictionary form:
    {
        "title": "", "shop": "", "finished": "Yes/No",
        "installer": [
            {"system": "", "lastupdated": "YYYY-MM-DD", "filename": [""]}
        ]
    }

    :param str element[=None]: The python dictionary containing the values of the element to be edited.
    """
    def show_edit_element(self, element = None):
        menu = None
        # Get the element's title from the user.
        if element is None:
            menu = True
            Utility.clear()
            element = input("Enter the title of the item to be edited: ")
        # Get element.
        game = self.get_element(element)
        if game is None:
            print("No game with title {} found.".format(element))
        elif isinstance(game, int):
            print("Invalid storage file {}.".format(self._xmlfile))
        else:
            # Create python dictionary parsing element's values.
            gamedict = self._xmlgame_to_dict(game)
            # Edit game.
            gamedict = self._generate_game(gamedict)
            #confirm before save.
            print("Saving item:")
            print(gamedict)
            answer = Utility.get_answer_yn("Save item?")
            # User wants to quit.
            if answer == "n":
                return
            # Persist changes.
            try:
                if self.edit_element(element, gamedict) == 0:
                    print("The edited item {} has been saved successfully.".format(element))
                else:
                    print("The edited item {} has not been saved.".format(element))
            except OSError:
                print("Temporary file ha not been removed, after the edited item {} has been saved.".format(element))
        if menu:
            input("Press 'Enter' to return to menu: ")
    # End of method show_edit_element.

    """
    Method: _xmlgame_to_dict

    Generates python dictionary from game xml element.

    :param etree.Element element: The game element node.
    :return dict: The python dictionary version of the XML node.
    """
    def _xmlgame_to_dict(self, element):
        # Create python dictionary parsing element's values.
        gamedict = {}
        installer = []
        for item in element.iterchildren():
            # Making sure installer tag has text, so that it will be iterated.
            if item.tag == "installer":
                item.text = " "
            # Elements in game.
            if item.text is not None:
                gamedict[item.tag] = item.text.strip()
                if item.tag == "installer":
                    installerdict = {}
                    filename = []
                    # Elements in installer.
                    for subitem in item.iterchildren():
                        if subitem.text is not None:
                            if subitem.tag == "filename":
                                filename.append(subitem.text.strip())
                            else:
                                installerdict[subitem.tag] = subitem.text.strip()
                    if filename:
                        installerdict["filename"] = filename
                    installer.append(installerdict)
        if installer:
            gamedict["installer"] = installer

        return gamedict
    # End of method _xmlgame_to_dict.

    """
    Method: show_remove_element

    Shows messages about element's removal.

    :param str element[=None]: The exact value in element title.
    """
    def show_remove_element(self, element = None):
        menu = None
        # Get the element's title from the user.
        if element is None:
            menu = True
            Utility.clear()
            element = input("Enter the title of the item to be removed: ")
        # Remove item.
        if self.remove_element(element) == 0:
            print("The item {} has been removed successfully.".format(element))
        else:
            print("The item {} has not been removed.".format(element))

        if menu:
            input("Press 'Enter' to return to menu: ")
    # End of method show_remove_element.

    """
    Method: _generate_game

    Generate game python dictionary.

    Python dictionary form:
    {
        "title": "", "shop": "", "finished": "Yes/No",
        "installer": [
            {"system": "", "lastupdated": "YYYY-MM-DD", "filename": [""]}
        ]
    }

    :param dict game[=None]: The python dictionary containing the values of the element.
    :return dict: The python dictionary containing new values.
    """
    def _generate_game(self, game = None):
        # Display header.
        if game is None:
            print("New", end = " ")
            game = {"title": None, "shop": None, "finished": None}
        print("Game Editor")
        print()
        # Get game's elements.
        title = ""
        while title == "":
            title = input("Title{}: ".format("" if game["title"] is None else "[" + game["title"] + "]"))
            if game["title"] is not None and title == "":
                title = game["title"]
        # Exit editor if the user is trying to create a game, which already exists.
        if game["title"] is None and self.get_element(title) is not None:
            print("Game {} already exists.".format(title))
            return None

        game["title"] = title

        shop = ""
        while shop == "":
            shop = input("Shop{}: ".format("" if game["shop"] is None else "[" + game["shop"] + "]"))
            if game["shop"] is not None and shop == "":
                shop = game["shop"]
        game["shop"] = shop

        finished = Utility.get_answer_yn("Finished{}:".format("" if game["finished"] is None else "[" + game["finished"] + "]"))
        if finished == "y":
            game["finished"] = "Yes"
        else:
            game["finished"] = "No"

        # Get game's installer elements.
        if Utility.get_answer_yn("Open installer editor?") == "y":
            game = self._generate_installer(game)
        # Return game dictionary.
        return game
    # End of method _generate_game.

    """
    Method: _generate_installer

    Generate installer python dictionary.

    Python dictionary form:
    {
        "title": "", "shop": "", "finished": "Yes/No",
        "installer": [
            {"system": "", "lastupdated": "YYYY-MM-DD", "filename": [""]}
        ]
    }

    :param dict game: The python dictionary containing the values of the element.
    :return dict: The python dictionary containing edited installer list or without installer key, if there is no istaller.
    """
    def _generate_installer(self, game):
        Utility.clear()
        # Display header.
        print("Installer Editor")
        print()
        if "installer" in game:
            removelist = []
            # Generate range of menu values once.
            choices = range(1, 4)
            for installer in game["installer"]:
                print("Installer:")
                for key in installer:
                    print("    {}: {}".format(key, installer[key]))

                # Display menu
                print("1. Keep and continue")
                print("2. Remove installer")
                print("3. Edit installer")
                # Get action from the user.
                choice = None
                # Generate menu
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
                        # Add elements to removal list.
                        removelist.append(installer)
                        print("Installer has been removed.")
                    elif choice == 3:
                        self._get_installer_values(installer)
                    else:
                        choice = None
            # Remove marked installers permanently.
            for rvalue in removelist:
                game["installer"].remove(rvalue)
            # If list is empty remove respective game dictionary key.
            if len(game["installer"]) == 0:
                del game["installer"]
        # Add new installer.
        game = self._generate_new_installer(game)

        return game
    # End of method _generate_installer.

    """
    Method: _generate_new_installer

    Generate new installer python dictionary.

    Python dictionary form:
    {
        "title": "", "shop": "", "finished": "Yes/No",
        "installer": [
            {"system": "", "lastupdated": "YYYY-MM-DD", "filename": [""]}
        ]
    }

    :param dict game: The python dictionary containing the values of the element.
    :return dict: The python dictionary containing new dictionaries into its installer list.
    """
    def _generate_new_installer(self, game):
        # Add new installer.
        installers = []
        while Utility.get_answer_yn("Add new installer?") == "y":
            newinst = self._get_installer_values()
            installers.append(newinst)
        # Add installers to game.
        if installers:
            if "installer" in game:
                game["installer"] += installers
            else:
                game["installer"] = installers
        return game
    # End of method _generate_new_installer.

    """
    Method: _get_installer_values

    Gets game's installer values from the user.

    Python dictionary form:
    {"system": "", "lastupdated": "YYYY-MM-DD", "filename": [""]}

    :param dict installer[=None]: The python dictionary containing the values of the element.
    :return dict: The python dictionary containing new installer values.
    """
    def _get_installer_values(self, installer = None):
        Utility.clear()
        # Display header.
        if installer is None:
            print("New", end = " ")
            installer = {"system": None}
        print("Installer")
        print()
        # Get installer's values.
        # Get system.
        systems = ['Windows', 'Mac', 'Linux', 'Other']
        schoices = range(1, 5)
        system = None
        while system not in systems:
            # Display menu
            print("System{}: ".format("" if installer["system"] is None else "[" + installer["system"] + "]"))
            for s in systems:
                print("{}. {}".format(systems.index(s) + 1, s))
            # Get user choice.
            try:
                choice = input("Enter your choice: ")
                if choice == "":
                    system = installer["system"]
                else:
                    choice = int(choice)
                    if choice in schoices:
                        system = systems[choice - 1]
            except ValueError:
                choice = None
        installer["system"] = system
        # Get lastupdated.
        lastupdated = None
        while lastupdated is None:
            print("Date should be written in form YYYY-MM-DD.")
            lastupdated = input("Last updated at{}: ".format("[" + installer["lastupdated"] + "]" if "lastupdated" in installer else ""))
            # Check if value is a valid date.
            valid = Utility.validate_date(lastupdated)
            if valid is not None:
                installer["lastupdated"] = valid
            elif lastupdated == "":
                # Pass for 1.
                # Alternatively break out of the loop.
                pass
            else:
                lastupdated = None
        # Get filenames.
        installer = self._generate_filename(installer)

        return installer
    # End of method _get_installer_values.

    """
    Method: _generate_filename

    Asks about current filenames.
    Calls method to get new filename values from the user.

    Python dictionary form:
    {"system": "", "lastupdated": "YYYY-MM-DD", "filename": [""]}

    :param dict installer: The python dictionary containing the values of the element.
    :return dict: The python dictionary containing edited filename list or without filename key, if there is no filename.
    """
    def _generate_filename(self, installer):
        removelist = []
        # Get filename.
        if "filename" in installer:
            for filename in installer["filename"]:
                # Get action from the user.
                choices = range(1, 3)
                choice = None
                # Generate menu
                # Display menu
                print(filename)
                print("1. Keep and continue")
                print("2. Remove filename")
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
                        removelist.append(filename)
                        print("Filename has been removed.")
                    else:
                        choice = None
            # Remove marked filenames permanently.
            for rvalue in removelist:
                installer["filename"].remove(rvalue)
            # If list is empty remove respective installer dictionary key.
            if len(installer["filename"]) == 0:
                del installer["filename"]
        # Add new filenames.
        self._get_filename_values(installer)

        return installer
    # End of method _generate_filename.

    """
    Method: _get_filename_values

    Gets new filename values from the user.

    Python dictionary form:
    {"system": "", "lastupdated": "YYYY-MM-DD", "filename": [""]}

    :param dict installer: The python dictionary containing the values of the element.
    :return dict: The python dictionary containing new filenames into its filename list.
    """
    def _get_filename_values(self, installer):
        # Add new filenames.
        fnames = []
        filename = "Enter Loop"
        #print(filename != "")
        while filename != "":
            filename = input("Add filename [leave empty to stop]: ")
            filename = filename.strip()
            if filename != "":
                fnames.append(filename)
        # Add filenames to installer.
        if fnames:
            if "filename" in installer:
                installer["filename"] += fnames
            else:
                installer["filename"] = fnames

        return installer
    # End of method _get_filename_values.
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
