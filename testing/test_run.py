#!/usr/bin/env python3

# Imports
import unittest
import run

"""
Class: TestRunModule

Testcases for starting application module run.
"""
class TestRunModule(unittest.TestCase):
    """
    Test function main with no arguments.
    """
    def test_main(self):
        with self.assertRaises(SystemExit):
            run.main()
    # End of method test_main.
# End of class TestRunModule

# Test running or loading
if __name__ == "__main__":
    unittest.main()
