#!/usr/bin/env python3

# Imports
import unittest
# Import testing modules.
from test_run import TestRunModule
from testing.library.test_book_management import TestBookManager
from testing.library.test_game_management import TestGameManager
from testing.library.test_music_management import TestMusicManager
from testing.library.test_video_management import TestVideoManager

# Test running or loading.
if __name__ == "__main__":
    unittest.main()
else:
    print("{} is the test starting point of the application.".format(__file__))
