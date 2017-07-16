#!/usr/bin/env python3

# Imports
import unittest
#import os
from lxml.etree import _Element
# Set path for importing application modules
import sys
import os
appdir = os.path.abspath(__file__).split("/testing/")[0]
sys.path.insert(0, appdir)
# Import application modules
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
    @unittest.skip("Skipped.")
    def test_validate(self):
        manager = GameManager(self.storagepath, "library.xml", "library.xsd")
        self.assertEqual(manager.validate(), 0)
    # End of method test_validate.

    """
    Test function get_all_elements using default order.
    """
    #@unittest.skip("Skipped.")
    def test_get_all_elements_default_order(self):
        manager = GameManager(self.storagepath, "library.xml", "library.xsd")
        self.assertIsInstance(manager.get_all_elements(), list)
    # End of method test_get_all_elements_default_order.

    """
    Test function show_all_elements.
    """
    #@unittest.skip("Skipped.")
    def test_show_all_elements(self):
        manager = GameManager(self.storagepath, "library.xml", "library.xsd")
        manager.show_all_elements()
    # End of method test_show_all_elements.

    """
    Test function get_element using an element which does not exist.
    """
    @unittest.skip("Skipped.")
    def test_get_element_non_existent(self):
        manager = GameManager(self.storagepath, "library.xml", "library.xsd")
        self.assertIsNone(manager.get_element("_/T\_ NOT EXISTS TEST _/T\_"))
    # End of method test_get_element_non_existent.

    """
    Test function get_element using an element which exists.
    """
    @unittest.skip("Skipped.")
    def test_get_element_existent(self):
        manager = GameManager(self.storagepath, "library.xml", "library.xsd")
        self.assertIsInstance(manager.get_element("Test"), _Element)
    # End of method test_get_element_existent.

    """
    Test function show_element.
    """
    @unittest.skip("Skipped.")
    def test_show_element(self):
        manager = GameManager(self.storagepath, "library.xml", "library.xsd")
        manager.show_element()
    # End of method test_show_element.
# End of class TestRunModule

# Test running or loading
if __name__ == "__main__":
    unittest.main()
