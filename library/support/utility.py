#!/usr/bin/env python3

# imports
import os
import platform
import re
import calendar
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

    :param str question: The message asking for input.
    :return str: Valid user input, y or n.
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

    :param str schemafile: The absolute path of XSD file.
    :param str testfile: The absolute path of XML file.
    :return int: 0 if validates, 1 if not and 2 in case of error.
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

    :param str schemafile: The absolute path of XSD file.
    :param str tree: The XML tree.
    :return int: 0 if validates, 1 if not and 2 in case of error.
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

    """
    Method: validate_date

    Checks if string is a valid date.
    Date string pattern is YYYY-MM-DD.

    :param str datestr: The string representation of the date.
    :return str_or_None: Union[str, None].
    """
    @staticmethod
    def validate_date(datestr):
        pattern = re.compile("^\d{4}-\d{2}-\d{2}$")
        datestr = datestr.strip()
        match = pattern.match(datestr)
        # No match.
        if match is None:
            return None

        # Cast strings to integers.
        numbers = match.group().split("-")
        try:
            for i in range(len(numbers)):
                numbers[i] = int(numbers[i])
        except ValueError:
            return None
        # Check if months and days are valid.
        if numbers[1] < 1 or numbers[1] > 12:
            # Invalid month.
            return None
        elif numbers[2] < 1:
            # Invalid number of days.
            return None
        elif numbers[1] in [4, 6, 9, 11] and numbers[2] > 30:
            # Invalid number of days per month.
            return None
        elif numbers[1] in [1, 3, 5 ,7 , 8, 10, 12] and numbers[2] > 31:
            # Invalid number of days per month.
            return None
        elif numbers[1] == 2:
            if calendar.isleap(numbers[0]):
                if numbers[2] > 29:
                    # Invalid number of days per month.
                    return None
            elif numbers[2] > 28:
                # Invalid number of days per month.
                return None

        # String is a valid date.
        return match.group()
    # End of static method validate_date.
# End of class Utility.
