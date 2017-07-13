Personal library management application written in python3.


Directory tree based on default configuration.

library_application/
        config/
                config.xml
                config.xsd
        library/
                support/
                        __init__.py
                        utility.py
                __init__.py
                book_management.py
                game_management.py
                music_management.py
                video_management.py
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
                        library.xsd
                video/
                        library.xml
                        library.xsd
        testing/
                __init__.py
                test_run.py
                test.py
        __init__.py
        application.py
        README.md
        run.py


Testing.

In order to run test from testing module system variable PYTHONPATH should be
set to root (/path/to/library_application) directory of the application.
Otherwise application's module imports will fail.

Alternatively root directory could be appended to sys.path before any import of
the application main module is made.
