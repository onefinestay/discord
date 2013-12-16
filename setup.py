#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="discord",
    version="0.1",
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
    ],
    license="Apache 2.0",
    classifiers=[
    ]
)