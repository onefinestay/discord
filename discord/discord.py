#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pip
from tempfile import mkdtemp
from os import listdir
from shutil import rmtree


logger = logging.getLogger(__name__)


class Requirement(object):

    def __init__(self, req):
        self.req = req.strip()
        if "==" in self.req:
            self.name, self.operator, self.version = self.req.partition("==")
        else:
            self.name, self.operator, self.version = self.req, None, None

    def __repr__(self):
        return self.req

    def __eq__(self, other):
        return self.req == other.req

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.req)

    def resolve(self, lookup, parent=None):
        logger.debug(repr(self))
        if self in lookup:
            lookup[self].add(parent)
            return None, {}
        else:
            lookup[self] = set([parent])
        d = mkdtemp()
        try:
            pip.main(["install", "-q", "-d", d, self.req])
            package, subpackages = None, {}
            for p in map(Package, listdir(d)):
                if p.name == self.name:
                    package = p
                else:
                    req = p.requirement
                    subpackages[req] = None
            subpackages = dict((key, key.resolve(lookup, package))
                               for key in subpackages.keys())
            return package, subpackages
        finally:
            rmtree(d)


class Package(object):

    def __init__(self, file_name):
        self.name, stuff = file_name.rpartition("-")[0::2]
        version = []
        for part in stuff.split("."):
            if all(x.isdigit() for x in part):
                version.append(part)
            else:
                break
        self.version = ".".join(version)

    def __repr__(self):
        return "{0} {1}".format(self.name, self.version)

    @property
    def requirement(self):
        return Requirement("{0}=={1}".format(self.name, self.version))


class RequirementsList(object):

    @classmethod
    def from_file(cls, file_name):
        inst = cls()
        with open(file_name) as reqs:
            for line in reqs:
                inst.append(line)
        return inst

    def __init__(self):
        self._reqs = []
        self.packages = {}
        
    def append(self, line):
        if line and not line.startswith("#"):
            self._reqs.append(Requirement(line))
        
    def resolve(self):
        flat = {}
        nested = dict((req, req.resolve(flat)) for req in self._reqs)
        out = {}
        for req, package in flat.items():
            out.setdefault(req.name, {})
            out[req.name][req.version] = package
        return out
    
    def discord(self):
        return dict(filter(lambda (k, v): len(v) > 1, self.resolve().items()))

