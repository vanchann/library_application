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
    confgroup = parser.add_mutually_exclusive_group()
    confgroup.add_argument("-c", "--configure", action="store_true", help="create or reset configuration")
    confgroup.add_argument("--validate-configuration", action="store_true", help="validate configuration")
    confgroup.add_argument("-l", "--load", help="load library of type LOAD")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
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
        app.load_library(args.load.lower())
        return
    # Display menu
    app.load_library(app.show_menu())
# End of function main

# Test running or loading
if __name__ == "__main__":
    main()
