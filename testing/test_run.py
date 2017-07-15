#!/usr/bin/env python3

# Imports
import unittest

# Set path for importing application modules
import sys
import os
appdir = os.path.abspath(__file__).split("/testing/")[0]
sys.path.insert(0, appdir)

# Import application modules
import run

"""
Class: TestRunModule

Testcases for starting application module run.
"""
class TestRunModule(unittest.TestCase):
    """
    Test function main with no arguments.
    """
    @unittest.skipIf([i for i in ["-v", "--verbose"] if i in sys.argv], "Verbose argument confuses run module")
    def test_main(self):
        self.assertIsNone(run.main())
    # End of method test_main.

    """
    Test function main with verbose argument.
    """
    @unittest.skipUnless([i for i in ["-v", "--verbose"] if i in sys.argv], "Verbose argument confuses run module")
    def test_main(self):
        with self.assertRaises(SystemExit):
            run.main()
    # End of method test_main.
# End of class TestRunModule

# Test running or loading
if __name__ == "__main__":
    unittest.main()
