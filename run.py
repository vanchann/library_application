#!/usr/bin/env python3

# Imports.
import argparse
from application import Application

# The following section contains code to execute when script is run from the command line.
"""
Function: main

Entry point for the execution of the script.
"""
def main():
    # Set command line arguments.
    parser = argparse.ArgumentParser(
                prog = "Ligrary Management",
                description = "Library management program utilizing XML human readable storage. Submitting no arguments displays menu.",
                epilog = "Created by Evangelos Channakis.")
    excluegroup1 = parser.add_mutually_exclusive_group()
    excluegroup1.add_argument("-c", "--configure", action = "store_true", help = "create or reset configuration.")
    excluegroup1.add_argument("-l", "--load", help = "load library of type 'LOAD'.")
    excluegroup1.add_argument("--validate-configuration", action = "store_true", help = "validate configuration.")

    excluegroup2 = parser.add_mutually_exclusive_group()
    excluegroup2.add_argument("--show", help = "show specific item of the loaded library.")
    excluegroup2.add_argument("--show-all", action = "store_true", help = "show all items of the loaded library sorted by the default element in ascending order.")
    excluegroup2.add_argument("--show-all-by", help = "show all items of the loaded library sorted by 'SHOW_ALL_BY' element in ascending order.")

    parser.add_argument("--reverse", action = "store_true", help = "sort items in reverse (descending) order.")
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
        print("Loading library of type {}...".format(args.load.lower()))
        if args.show_all:
            app.get_manager(args.load.lower()).show_all_elements(ascending = not args.reverse)
        elif args.show_all_by:
            app.get_manager(args.load.lower()).show_all_elements(args.show_all_by, not args.reverse)
        elif args.show:
            app.get_manager(args.load.lower()).show_element(args.show)
        else:
            app.load_library(args.load.lower())
        return
    # Incorectly used options.
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
    if args.reverse:
        print("Argument --reverse, should be used with arguments --show-all and --show-all-by.")
        return
    # Display menu
    app.show_menu()
# End of function main

# Test running or loading
if __name__ == "__main__":
    main()
