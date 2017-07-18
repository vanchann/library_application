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
        self.manager = GameManager(self.storagepath, "library.xml", "library.xsd")
    # End of method setUp

    """
    Test validate.
    """
    @unittest.skip("Skipped.")
    def test_validate(self):
        self.assertEqual(self.manager.validate(), 0)
    # End of method test_validate.

    """
    Test function search_elements_none_element without passing in an element.
    """
    @unittest.skip("Skipped.")
    def test_search_elements_none_element(self):
        self.assertIsNone(self.manager.search_elements("", "Test"))
    # End of method test_search_elements_none_element.

    """
    Test function search_elements_no_value without passing an existing value.
    """
    @unittest.skip("Skipped.")
    def test_search_elements_no_value(self):
        self.assertIsNone(self.manager.search_elements("title", "_/T\_ NOT EXISTS TEST _/T\_"))
    # End of method test_search_elements_no_value.

    """
    Test function search_elements using default order.
    """
    @unittest.skip("Skipped.")
    def test_search_elements(self):
        self.assertIsInstance(self.manager.search_elements("finished", "e"), list)
    # End of method test_search_elements.

    """
    Test function show_search_elements using default order.
    """
    @unittest.skip("Skipped.")
    def test_show_search_elements(self):
        self.manager.show_search_elements("finished", "e")
    # End of method show_search_elements.

    """
    Test function get_all_elements using default order.
    """
    @unittest.skip("Skipped.")
    def test_get_all_elements_default_order(self):
        self.assertIsInstance(self.manager.get_all_elements(), list)
    # End of method test_get_all_elements_default_order.

    """
    Test function show_all_elements.
    """
    @unittest.skip("Skipped.")
    def test_show_all_elements(self):
        self.manager.show_all_elements()
    # End of method test_show_all_elements.

    """
    Test function get_element using an element which does not exist.
    """
    @unittest.skip("Skipped.")
    def test_get_element_non_existent(self):
        self.assertIsNone(self.manager.get_element("_/T\_ NOT EXISTS TEST _/T\_"))
    # End of method test_get_element_non_existent.

    """
    Test function get_element using an element which exists.
    """
    @unittest.skip("Skipped.")
    def test_get_element_existent(self):
        self.assertIsInstance(self.manager.get_element("Test"), _Element)
    # End of method test_get_element_existent.

    """
    Test function add_element_invalid_dict.
    """
    #@unittest.skip("Skipped.")
    def test_add_element_invalid_dict(self):
        self.assertEqual(self.manager.add_element({"titlE": "Dict", "shop": "Free", "finished": "No"}), 1)
    # End of method test_add_element_invalid_dict.

    """
    Test function add_element without installer.
    """
    #@unittest.skip("Skipped.")
    def test_add_element_no_installer(self):
        self.assertEqual(self.manager.add_element({"title": "Dict", "shop": "Free", "finished": "No"}), 0)
    # End of method test_add_element_no_installer.

    """
    Test function add_element with installer.
    """
    #@unittest.skip("Skipped.")
    def test_add_element_with_installer(self):
        game = {"title": "Dict installer", "shop": "Free", "finished": "No",
                "installer": [{"system": "Mac", "filename": ["file1", "file2"]}]}
        self.assertEqual(self.manager.add_element(game), 0)
    # End of method test_add_element_with_installer.

    """
    Test function show_element.
    """
    @unittest.skip("Skipped.")
    def test_show_element(self):
        self.manager.show_element()
    # End of method test_show_element.
# End of class TestRunModule

# Test running or loading
if __name__ == "__main__":
    unittest.main()
