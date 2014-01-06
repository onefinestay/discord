#!/usr/bin/env python
# -*- coding: utf-8 -*-

from discord import *
import sys


if __name__ == "__main__":

    args = list(sys.argv)

    script_name = args.pop(0)
    verbosity = 0
    req_file_name = None

    while args:
        arg = args.pop(0)
        if arg.startswith("-"):
            if arg == "-v":
                verbosity = 1
        else:
            req_file_name = arg

    def package_repr(package):
        if package is None:
            return "<" + req_file_name + ">"
        else:
            return str(package)

    if not req_file_name:
        req_file_name = "requirements.txt"

    requirements_list = RequirementsList.from_file(req_file_name)
    discord = requirements_list.discord(verbosity=verbosity)
    for package_name, versions in discord.items():
        print package_name
        for version, dependers in sorted(versions.items()):
            dep_list = ", ".join(map(package_repr, dependers))
            print "    {0} is required by {1}".format(version, dep_list)
