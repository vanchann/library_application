#!/usr/bin/env python3

# imports
import os
import platform
from lxml import etree

"""
Class: Utility

Utility class offers application supporting utilities via static methods.
"""
class Utility:
    """
    Static method: clear

    Cleans output based on the platform.
    """
    @staticmethod
    def clear():
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
    # End of static method clear.

    """
    Static method: get_answer_yn

    Asks for input until a Y/y or N/n has been entered.
    """
    @staticmethod
    def get_answer_yn(question):
        answer = ""
        while answer.lower() != "y" and answer.lower() != "n":
            answer = input("{} [y/n] ".format(question))
        return answer.lower()
    # End of static method get_answer_yn.

    """
    Method: validate

    Validates XML file given an XSD schema.
    Returns 0 if validates, 1 if not and 2 in case of error.
    """
    @staticmethod
    def validate(schemafile, testfile):
        try:
            with open(schemafile, 'r') as xsdfile, open(testfile, 'r') as xmlfile:
                # Create schema object.
                xmlschema_doc = etree.parse(xsdfile)
                xmlschema = etree.XMLSchema(xmlschema_doc)
                # Create xml tree.
                xmldoc = etree.parse(xmlfile)
                # Validate.
                if xmlschema.validate(xmldoc):
                    return 0
                else:
                    return 1
        except FileNotFoundError:
            return 2
    # End of static method validate.

    """
    Method: validate_tree

    Validates XML tree given an XSD schema.
    Returns 0 if validates, 1 if not and 2 in case of error.
    """
    @staticmethod
    def validate_tree(schemafile, tree):
        try:
            with open(schemafile, 'r') as xsdfile:
                # Create schema object.
                xmlschema_doc = etree.parse(xsdfile)
                xmlschema = etree.XMLSchema(xmlschema_doc)
                # Validate tree.
                if xmlschema.validate(tree):
                    return 0
                else:
                    return 1
        except FileNotFoundError:
            return 2
    # End of static method validate_tree.
# End of class Utility.
