#!/usr/bin/env python
# -*- coding: utf-8 -*-

from discord import *
import sys


def package_repr(package):
    if package is None:
        return "local requirements"
    else:
        return str(package)


if __name__ == "__main__":
    try:
        req_file_name = sys.argv[1]
    except IndexError:
        req_file_name = "requirements.txt"
    discord = RequirementsList.from_file(req_file_name).discord()
    for package_name, versions in discord.items():
        print package_name
        for version, dependers in sorted(versions.items()):
            print "    {0} is required by {1}".format(version, ", ".join(map(package_repr, dependers)))

