#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="discord",
    version="0.2",
    description="Discord is a tool for determining dependency version "
                "conflicts in complex Python projects.",
    author="onefinestay",
    author_email="engineering@onefinestay.com",
    url="http://github.com/onefinestay/discord",
    packages=[
        "discord",
    ],
    install_requires=[
        "pip",
        "wheel",
    ],
    license="Apache 2.0",
    classifiers=[
    ],
    entry_points={
        "console_scripts": [
            "discord = discord.command:main",
        ],
    },
)