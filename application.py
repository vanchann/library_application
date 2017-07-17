#!/usr/bin/env python3

# Imports
import sys
import platform
import os
from lxml import etree
from library.game_management import GameManager
from library.support.utility import Utility

"""
Class: Application

The main class for starting the appilcation.
"""
class Application:
    """
    Initializer
    """
    def __init__(self):
        super().__init__()
        # Initialize application directory values.
        fullpath = os.path.abspath(__file__)
        self.__rundir = os.path.split(fullpath)[0]
        self.__confdir = os.path.join(self.__rundir, "config")
        self.__confxsd = os.path.join(self.__confdir, "config.xsd")
        self.__confxml = os.path.join(self.__confdir, "config.xml")
    # End of initializer.

    """
    Method: __invalidconfexit

    Check for configuration vallidity. Notify the user and exit in case of
    invalid settings.
    """
    def __invalidconfexit(self):
        # Load configuration
        if Utility.validate(self.__confxsd, self.__confxml) != 0:
            # Validation has failed.
            print("Invalid configuration. Please reconfigure the application")
            sys.exit(2)
    # End of method __invalidconfexit,

    """
    Method: get_manager

    Gets a library manager object.
    """
    def get_manager(self, libtype):
        # Configuration vallidity check.
        self.__invalidconfexit()
        # Chech if library type is supported.
        supportedlibs = self.library_types()
        if libtype not in supportedlibs:
            print("Unsupported library type {}.".format(libtype))
            print("Supported library types by current configuration: {}".format(supportedlibs))
            sys.exit(3)

        # Create xml tree.
        tree = etree.parse(self.__confxml)
        # Find library filename.
        libfile = tree.find("/library").text
        # Find library schema filename.
        libschemafile =tree.find("/schema").text

        # Create library manager for specific library type.
        if libtype == "game":
            manager = GameManager(os.path.join(self.__rundir, "storage"), libfile, libschemafile)
        else:
            print("Not yet inmplemented library type {}.".format(libtype))
            return None
        # Return managet object.
        return manager
    # End of method get_manager.

    """
    Method: load_library

    Loads the library of the specified type.
    """
    def load_library(self, libtype):
        manager = self.get_manager(libtype)
        if manager is None:
            input("Press 'Enter' to return to menu: ")
        else:
            manager.show_menu()
    # End of method load_library.

    """
    Method: library_types

    Return configured ligrary types list.
    """
    def library_types(self):
        # Configuration vallidity check.
        self.__invalidconfexit()

        # Create xml tree.
        tree = etree.parse(self.__confxml)
        # Find all type nodes.
        tnodes = tree.findall("/types/type")
        # Get type text and append it to libtypes list.
        libtypes = []
        for t in tnodes:
            libtypes.append(t.text)
        return libtypes
    # End of method library_types

    """
    Method: show_menu

    Creates menu based on configuration and presents choices to the user.
    """
    def show_menu(self):
        # Initialize local variables
        avtypes = self.library_types()
        avchoices = range(len(avtypes) + 1)
        choice = None

        # Generate menu
        while choice not in avchoices:
            # Clear display.
            Utility.clear()
            # Display menu
            print("Available library types:")
            index = 0
            for t in avtypes:
                index += 1
                print("{}. {}".format(index, t.title()))
            print("0. Quit")
            # Get user choice.
            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                choice = None

            # Exit menu.
            if choice == 0:
                return
            elif choice in avchoices:
                self.load_library(avtypes[choice - 1])
            choice = None
    # End of method show_menu

    """
    Method: configure

    Create or reset configuration. The method is meant to be externaly.
    """
    def configure(self):
        try:
            # Create configuration directory if it does not exist.
            if not os.path.isdir(self.__confdir):
                os.mkdir(self.__confdir)
        except OSError:
            self.__errorexit(conffile, "directory")

        # Create configuration files.
        self.__createconf()
    # End of method configure.

    """
    Method: validate_configuration

    Reads and validates configuration or creates configuration if need.
    Application defaults to save its configuration in a config directory, which
    contains config.xml configuration file and config.xsd schema for validation.
    """
    def validate_configuration(self):
        # Validate configuration.
        if Utility.validate(self.__confxsd, self.__confxml) == 0:
            # Validation was successful.
            print("Validates")
        else:
            # Validation has failed.
            print("Configuration does not validate.")
            # Ask user for creating new configuration.
            newconf = ""
            while newconf.lower() != "y" and newconf.lower() != "n":
                newconf = input("Create new configuration files y(will overwrite existed files)/n? ")

            if newconf.lower() == "y":
                # Create new configuration.
                self.configure()
            else:
                # Exit cleanly.
                sys.exit(0)
    # End of method validate_configuration.

    """
    Method: __createconf

    Creates configuration files. Overwrites existed files, if any.
    """
    def __createconf(self):
        # Create the xml tree.
        root = etree.XML("""
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="config.xsd"></config>
        """)
        elelibrary = etree.SubElement(root, "library")
        elelibrary.text = "library.xml"
        eleschema = etree.SubElement(root, "schema")
        eleschema.text = "library.xsd"
        eletypes = etree.SubElement(root, "types")
        eletype = etree.SubElement(eletypes, "type")
        eletype.text = "book"
        eletype = etree.SubElement(eletypes, "type")
        eletype.text = "game"
        eletype = etree.SubElement(eletypes, "type")
        eletype.text = "music"
        eletype = etree.SubElement(eletypes, "type")
        eletype.text = "video"

        # Write xml tree to file conffile
        xmlout = etree.ElementTree(root)
        try:
            xmlout.write(self.__confxml, xml_declaration=True, encoding="UTF-8", pretty_print=True)
        except OSError:
            self.__errorexit(conffile)

        # Create the xsd tree.
        xsdroot = etree.XML("""
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">

<!-- definition of simple types -->
<xs:element name="library">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:minLength value="5" />
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<xs:element name="schema">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:minLength value="5" />
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<xs:element name="type">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:enumeration value="book"/>
            <xs:enumeration value="game"/>
            <xs:enumeration value="music"/>
            <xs:enumeration value="video"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<!-- definition of complex types -->
<xs:element name="types">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="type" minOccurs="1" maxOccurs="4"/>
        </xs:sequence>
    </xs:complexType>
</xs:element>

<xs:element name="config">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="library"/>
            <xs:element ref="schema"/>
            <xs:element ref="types"/>
        </xs:sequence>
    </xs:complexType>
</xs:element>

</xs:schema>
        """)

        # Write xsd tree to file confschema
        xsdout = etree.ElementTree(xsdroot)
        try:
            xsdout.write(self.__confxsd, xml_declaration=True, encoding="UTF-8", pretty_print=True)
        except OSError:
            self.__errorexit(confschema)
    # End of method __createconf.

    """
    Method: __errorioexit

    Show error messages and terminate execution of the program with an error code.
    """
    def __errorexit(self, name, dirorfile = "file", code = 1):
        # Show error messages and terminate execution of the program.
        print("Creation of {} {} failed".format(dirorfile, name))
        print("Check if path is valid and user has write privilege.")
        print("Program Excecution is terminating.")
        # Exit with an error code.
        sys.exit(1)
    # End of method __errorexit.
# End of class Application.

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
