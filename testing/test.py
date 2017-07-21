#!/usr/bin/env python3

# Imports
import unittest
# Import testing modules.
from test_run import TestRunModule
from testing.library.test_game_management import TestGameManager

# Test running or loading.
if __name__ == "__main__":
    unittest.main()
else:
    print("{} is the test starting point of the application.".format(__file__))
