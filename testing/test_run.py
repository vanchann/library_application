#!/usr/bin/env python3

# Imports
import unittest
from unittest.mock import patch
import sys
from io import StringIO
# Set path for importing application modules.
import os
appdir = os.path.abspath(__file__).split("/testing/")[0]
sys.path.insert(0, appdir)

# Import application modules.
import run
import application

"""
Class: TestRunModule

Testcases for starting application module run.
"""
class TestRunModule(unittest.TestCase):
    """
    Test function main with no arguments.
    """
    @unittest.skipIf([i for i in ["-v", "--verbose"] if i in sys.argv], "Unittest verbose argument confuses run module")
    @patch.object(application, "input", create = True)
    def test_main(self, input):
        input.return_value = "0"

        originalout = sys.stdout
        out = StringIO()
        sys.stdout = out

        test = run.main()
        sys.stdout = originalout

        self.assertIsNone(test)
    # End of method test_main.
# End of class TestRunModule.

# Test running or loading.
if __name__ == "__main__":
    unittest.main()
