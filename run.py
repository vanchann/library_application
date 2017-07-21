#!/usr/bin/env python3

# Imports.
import argparse
import ast
from application import Application

# The following section contains code to execute when script is run from the command line.
"""
Function: main

Entry point for the execution of the script.
Command line arguments will be parsed and translated to their respecive target
fuctionality.
"""
def main():
    # Set command line arguments.
    parser = argparse.ArgumentParser(
                prog = "Ligrary Management",
                description = """
                Library management program utilizing XML human readable storage. Submitting no arguments displays menu.

                For a new element to be added to a library file, it should be passed as a string containing the element as a python dictionary.
                Dictionary syntax is specific to the target library type.
                """,
                epilog = "Created by Evangelos Channakis.")
    excluegroup1 = parser.add_mutually_exclusive_group()
    excluegroup1.add_argument("-c", "--configure", action = "store_true", help = "create or reset configuration.")
    excluegroup1.add_argument("-l", "--load", help = "load library of type 'LOAD'.")
    excluegroup1.add_argument("--validate-configuration", action = "store_true", help = "validate configuration.")

    excluegroup2 = parser.add_mutually_exclusive_group()
    excluegroup2.add_argument("--add", help = "add item 'ADD' to the loaded library.")
    excluegroup2.add_argument("--remove", help = "remove item 'REMOVE' from the loaded library.")
    excluegroup2.add_argument("--search", help = "search in elements 'SEARCH' of the loaded library and show results in ascending order.")
    excluegroup2.add_argument("--show", help = "show specific item of the loaded library.")
    excluegroup2.add_argument("--show-all", action = "store_true", help = "show all items of the loaded library sorted by the default element in ascending order.")
    excluegroup2.add_argument("--show-all-by", help = "show all items of the loaded library sorted by 'SHOW_ALL_BY' element in ascending order.")

    parser.add_argument("--reverse", action = "store_true", help = "sort items in reverse (descending) order.")
    parser.add_argument("--value", help = "the 'VALUE' to search for.")
    parser.add_argument("--version", action = "version", version = "%(prog)s 0.1.0")

    args = parser.parse_args()
    # Create Application object app.
    app = Application()
    # React to arguments passed.
    if args.configure:
        print("Reconfiguring the application...")
        app.configure()
        print("...finished.")
        return
    if args.validate_configuration:
        print("Validating configuration...")
        app.validate_configuration()
        return
    if args.load:
        # print("Loading library of type {}...".format(args.load.lower()))
        if args.show_all:
            app.get_manager(args.load.lower()).show_all_elements(ascending = not args.reverse)
        elif args.show_all_by:
            app.get_manager(args.load.lower()).show_all_elements(args.show_all_by, not args.reverse)
        elif args.show:
            app.get_manager(args.load.lower()).show_element(args.show)
        elif args.search:
            if args.value:
                app.get_manager(args.load.lower()).show_search_elements(args.search, args.value, not args.reverse)
            else:
                print("No value to search for. Please use argument --value.")
        elif args.add:
            app.get_manager(args.load.lower()).show_add_element(ast.literal_eval(args.add))
        elif args.remove:
            app.get_manager(args.load.lower()).show_remove_element(args.remove)
        else:
            app.load_library(args.load.lower())
        return
    # Incorectly used options.
    if args.add:
        # There is no library loaded.
        print("Argument --add, should be used with argument --load.")
        return
    if args.remove:
        # There is no library loaded.
        print("Argument --remove, should be used with argument --load.")
        return
    if args.show_all:
        # There is no library loaded.
        print("Argument --show_all, should be used with argument --load.")
        return
    if args.show_all_by:
        # There is no library loaded.
        print("Argument --show_all_by, should be used with argument --load.")
        return
    if args.show:
        # There is no library loaded.
        print("Argument --show, should be used with argument --load.")
        return
    if args.search:
        # There is no library loaded.
        print("Argument --search, should be used with argument --load.")
        return
    if args.value:
        print("Argument --value, should be used with argument --search.")
        return
    if args.reverse:
        print("Argument --reverse, should be used with arguments --search, --show-all and --show-all-by.")
        return
    # Display menu
    app.show_menu()
# End of function main.

# Test running or loading.
if __name__ == "__main__":
    main()
