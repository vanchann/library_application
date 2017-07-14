#!/usr/bin/env python3

# Imports
import unittest
import os
from lxml.etree import _Element
from library.game_management import GameManager

"""
Class: TestGameManager

Testcases for TestGameManager.
"""
class TestGameManager(unittest.TestCase):
    """
    Setup
    """
    def setUp(self):
        self.storagepath = os.path.abspath(__file__).split("/testing/library/test_game_management.py")[0]
        self.storagepath = os.path.join(self.storagepath, "storage")
    # End of method setUp

    """
    Test validate.
    """
    def test_validate(self):
        manager = GameManager(self.storagepath, "library.xml", "library.xsd")
        self.assertEqual(manager.validate(), 0)
    # End of method test_validate.

    """
    Test function get_element using an element which does not exist.
    """
    def test_get_element_non_existent(self):
        manager = GameManager(self.storagepath, "library.xml", "library.xsd")
        self.assertIsNone(manager.get_element("_/T\_ NOT EXISTS TEST _/T\_"))
    # End of method test_get_element_non_existent.

    """
    Test function get_element using an element which exists.
    """
    def test_get_element_existent(self):
        manager = GameManager(self.storagepath, "library.xml", "library.xsd")
        self.assertIsInstance(manager.get_element("Test"), _Element)
    # End of method test_get_element_existent.

    """
    Test function show_element.
    """
    def test_show_element(self):
        manager = GameManager(self.storagepath, "library.xml", "library.xsd")
        manager.show_element()
    # End of method test_show_element.
# End of class TestRunModule

# Test running or loading
if __name__ == "__main__":
    unittest.main()
