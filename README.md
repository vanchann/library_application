GENERAL INFORMATION
--------------------------------------------------------------------------------

The library_application module contains a personal library management application
written in python 3.

This is the offline CLI version.

DESCRIPTION AND REQUIREMENTS
--------------------------------------------------------------------------------

Python is very helpful for quick coding solutions.
The minimum version for this application is python 3.2, because of argparse module
dependency in run script.

If run is not going to be used, the rest of the code should be fine with any python
3 version.

Testing requires a least python version 3.3, due to unittest.mock module dependency.

The application may be launch via run.py script, which is actually just the command
line gate to the application.

run.py -h (and run.py --help) will display usage instructions.
run.py without any command line arguments will display the application's menu.

Application configuration generation and validation, as well as library import to
and export from CSV file functionality is available only through command line arguments.

This module is being developed and tested on FreeBSD and Linux (Debian stable).

It should work on Windows, since code has been written in a system adaptive way,
but it has not been tested on Windows yet.

Storage is consisted of XML files, validated based on XSD schema files and python's
lxml module is required. This decision has been made, to keep the application free
of external database dependencies. This way, the whole module may be reside and run
from any external storage devices.

XML is also a human readable markup language, so the files may be read, edited
and generally used whatever way the user would like independently of the application.

I'm thinking about an online version with local XML library synchronization. Maybe
even a GUI version.

I'm developing this application according to my personal needs, but new ideas would
be more than welcome.

CSV FORMAT
--------------------------------------------------------------------------------
```
Character set: UTF-8
Field delimiter: ,
Text delimiter: \

Book Library CSV header: Title,Author,Category,Format,ISBN,Finished
Game Library CSV header: Title,Shop,Finished,System
```
DIRECTORY TREE BASED ON DEFAULT CONFIGURATION
--------------------------------------------------------------------------------
```
library_application/
        config/
                config.xml
                config.xsd
        library/
                support/
                        __init__.py
                        utility.py
                __init__.py
                book_management.py    # Implemented, but still under test.
                game_management.py    # Implemented, but still under test.
                music_management.py   # Contains not yet implemented dummy class.
                video_management.py   # Contains not yet implemented dummy class.
                management.py
        storage/
                book/
                        library.xml
                        library.xsd
                game/
                        library.xml
                        library.xsd
                music/
                        library.xml
                        library.xsd   # Will be generated programmatically by MusicManager class
                video/
                        library.xml
                        library.xsd   # Will be generated programmatically by VideoManager class
        testing/                      # Testing is not exhaustive nor complete at this time.
                library/
                        __init__.py
                        test_book_library.xml
                        test_book_management.py
                        test_game_library.xml
                        test_game_management.py
                __init__.py
                test_run.py
                test.py
        __init__.py
        application.py
        README.md
        run.py
```
TESTING
--------------------------------------------------------------------------------
Testing is not exhaustive nor complete at this time.

Minimum required python version for testing is 3.3, due to unittest.mock module
dependency.

In order to run tests from testing module, system variable PYTHONPATH should be
set to root (/path/to/library_application) directory of the application.
Otherwise application's module imports will fail.

To overcome the above issue, root directory has already be inserted in sys.path
before any import of the main application's modules.
