#!/usr/bin/env python3

# Imports
import unittest
from unittest.mock import patch
from io import StringIO
from lxml.etree import _Element
import shutil
import sys
import os
# Set path for importing application modules.
appdir = os.path.abspath(__file__).split("/testing/")[0]
sys.path.insert(0, appdir)
# Import application modules.
import library.game_management
from library.game_management import GameManager

"""
Class: TestGameManager

Testcases for TestGameManager.
"""
class TestGameManager(unittest.TestCase):
    """
    Set up.
    """
    def setUp(self):
        # Set up path values.
        self.storagepath = os.path.abspath(__file__).split("/testing/library/test_game_management.py")[0]
        self.storagepath = os.path.join(self.storagepath, "storage")

        self.xmlbackup = os.path.join(self.storagepath, "game", "xmlbackup.test.back")
        self.xsdbackup = os.path.join(self.storagepath, "game", "xsdbackup.test.back")
        self.testlibrary = os.path.join(os.path.split(os.path.abspath(__file__))[0], "test_game_library.xml")

        # Initialize GameManager.
        self.manager = GameManager(self.storagepath, "library.xml", "library.xsd")

        # Take test backup of library xml and schema.
        shutil.copy2(self.manager._xmlfile, self.xmlbackup)
        shutil.copy2(self.manager._xsdfile, self.xsdbackup)
        # Copy test library file.
        shutil.copy2(self.testlibrary, self.manager._xmlfile)
    # End of method setUp.

    """
    Tear down.
    """
    def tearDown(self):
        # Restore library xml and schema from test backup.
        shutil.copy2(self.xmlbackup, self.manager._xmlfile)
        os.remove(self.xmlbackup)
        shutil.copy2(self.xsdbackup, self.manager._xsdfile)
        os.remove(self.xsdbackup)
    # End of method tearDown.

    """
    Test validate.
    """
    #@unittest.skip("Skipped.")
    def test_validate(self):
        self.assertEqual(self.manager.validate(), 0)
    # End of method test_validate.

    """
    Test function search_elements_none_element without passing in an element.
    """
    #@unittest.skip("Skipped.")
    def test_search_elements_none_element(self):
        self.assertIsNone(self.manager.search_elements("", "Test"))
    # End of method test_search_elements_none_element.

    """
    Test function search_elements_no_value without passing an existing value.
    """
    #@unittest.skip("Skipped.")
    def test_search_elements_no_value(self):
        self.assertIsNone(self.manager.search_elements("title", "_/T\_ NOT EXISTS TEST _/T\_"))
    # End of method test_search_elements_no_value.

    """
    Test function search_elements using default order.
    """
    #@unittest.skip("Skipped.")
    def test_search_elements(self):
        self.assertIsInstance(self.manager.search_elements("finished", "e"), list)
    # End of method test_search_elements.

    """
    Test function show_search_elements using default order.
    """
    #@unittest.skip("Skipped.")
    def test_show_search_elements(self):
        originalout = sys.stdout
        out = StringIO()
        sys.stdout = out

        self.manager.show_search_elements("finished", "e")
        sys.stdout = originalout

        test = "\
Title  | Shop     | Finished | System\
-------|----------|----------|-------\
Test   | DRM-free | Yes      | Windows Mac Linux \
a      | DRM-free | Yes      | \
Nofile | Free     | Yes      | Other Linux "
        self.assertEqual("".join(out.getvalue().split(os.linesep)), test)
    # End of method show_search_elements.

    """
    Test function get_all_elements using default order.
    """
    #@unittest.skip("Skipped.")
    def test_get_all_elements_default_order(self):
        self.assertIsInstance(self.manager.get_all_elements(), list)
    # End of method test_get_all_elements_default_order.

    """
    Test function show_all_elements.
    """
    #@unittest.skip("Skipped.")
    def test_show_all_elements(self):
        originalout = sys.stdout
        out = StringIO()
        sys.stdout = out

        self.manager.show_all_elements()
        sys.stdout = originalout

        test = "\
Title  | Shop     | Finished | System\
-------|----------|----------|-------\
a      | DRM-free | Yes      | \
A      | DRM-free | No       | \
Nofile | Free     | Yes      | Other Linux \
Test   | DRM-free | Yes      | Windows Mac Linux \
Test1  | DRM-free | No       | "
        self.assertEqual("".join(out.getvalue().split(os.linesep)), test)
    # End of method test_show_all_elements.

    """
    Test function get_element using an element which does not exist.
    """
    #@unittest.skip("Skipped.")
    def test_get_element_non_existent(self):
        self.assertIsNone(self.manager.get_element("_/T\_ NOT EXISTS TEST _/T\_"))
    # End of method test_get_element_non_existent.

    """
    Test function get_element using an element which exists.
    """
    #@unittest.skip("Skipped.")
    def test_get_element_existent(self):
        self.assertIsInstance(self.manager.get_element("Test"), _Element)
    # End of method test_get_element_existent.

    """
    Test function add_element using invalid dictionary key.
    """
    #@unittest.skip("Skipped.")
    def test_add_element_invalid_dict_key(self):
        game = {"titlE": "Dict", "shop": "Free", "finished": "No"}
        self.assertEqual(self.manager.add_element(game), 1)
    # End of method test_add_element_invalid_dict_key.

    """
    Test function add_element using invalid dictionary value.
    """
    #@unittest.skip("Skipped.")
    def test_add_element_invalid_dict_value(self):
        game = {"title": "Dict installer", "shop": "Free", "finished": "",
                "installer": [{"system": "Mac", "filename": ["file1", "file2"]}]}
        self.assertEqual(self.manager.add_element(game), 3)
    # End of method test_add_element_invalid_dict_value.

    """
    Test function add_element using existing item.
    """
    #@unittest.skip("Skipped.")
    def test_add_element_existing_item(self):
        game = {"title": "Test", "shop": "Free", "finished": "No",
                "installer": [{"system": "Mac", "filename": ["file1", "file2"]}]}
        self.assertEqual(self.manager.add_element(game), 3)
    # End of method test_add_element_existing_item.

    """
    Test function add_element without installer.
    """
    #@unittest.skip("Skipped.")
    def test_add_element_no_installer(self):
        game = {"title": "Dict", "shop": "Free", "finished": "No"}
        self.assertEqual(self.manager.add_element(game), 0)
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
    Test function remove_element.
    """
    #@unittest.skip("Skipped.")
    def test_remove_element(self):
        self.assertEqual(self.manager.remove_element("Nofile"), 0)
    # End of method test_remove_element.

    """
    Test function show_element with existing item.
    """
    #@unittest.skip("Skipped.")
    @patch.object(library.game_management, "input", create = True)
    def test_show_element_existing(self, input):
        input.return_value = "Test"

        originalout = sys.stdout
        out = StringIO()
        sys.stdout = out

        self.manager.show_element()
        sys.stdout = originalout

        test = "\
Exact match will be made!\
Game:\
    Title: Test\
    Shop: DRM-free\
    Finished: Yes\
    Installer: \
        System: Windows\
        Lastupdated: 2017-07-14\
        Filename: win_file_1\
        Filename: win_file_2\
        Filename: win_file_3\
    Installer: \
        System: Mac\
        Filename: mac_file_1\
        Filename: mac_file_2\
    Installer: \
        System: Linux\
        Filename: lin_file_1\
        Filename: lin_file_2"
        self.assertEqual("".join(out.getvalue().split(os.linesep)), test)
    # End of method test_show_element_existing.

    """
    Test function show_element with no existing item.
    """
    #@unittest.skip("Skipped.")
    @patch.object(library.game_management, "input", create = True)
    def test_show_element_no_existing(self, input):
        input.return_value = "TesT"

        originalout = sys.stdout
        out = StringIO()
        sys.stdout = out

        self.manager.show_element()
        sys.stdout = originalout

        test = "Exact match will be made!No game with title TesT found."
        self.assertEqual("".join(out.getvalue().split(os.linesep)), test)
    # End of method test_show_element_no_existing.

    """
    Test function import_csv.
    """
    #@unittest.skip("Skipped.")
    def test_import_csv(self):
        self.assertEqual(self.manager.import_csv("games.csv"), 0)
    # End of method test_import_csv.

    """
    Test function export_csv.
    """
    #@unittest.skip("Skipped.")
    def test_export_csv(self):
        self.assertEqual(self.manager.export_csv("games.csv"), 0)
    # End of method test_export_csv.
# End of class TestGameManager.

# Test running or loading.
if __name__ == "__main__":
    unittest.main()
