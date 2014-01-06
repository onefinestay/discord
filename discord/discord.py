#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pip
import re
import sys
from tempfile import mkdtemp
from os import listdir
from shutil import rmtree


logger = logging.getLogger(__name__)

WHEEL_NAME = re.compile(r"[^-]+-[0-9.]+-[^-]+-[^-]+")


class Requirement(object):
    """ A requirement holds a package specification, such as "requests==2.1.0".
    """

    def __init__(self, req):
        req = req.strip()
        self._req = req
        if WHEEL_NAME.match(req):
            self._is_wheel = True
            bits = req.split("-")
            self.name = bits[0]
            self.equality = "=="
            self.version = bits[1]
            self.pythons = bits[2]
            self.abi = bits[3]
        else:
            self._is_wheel = False
            if "==" in req:
                self.name, self.equality, self.version = req.partition("==")
            else:
                self.name, self.equality, self.version = req, None, None
            self.pythons = None
            self.abi = None

    def __repr__(self):
        return self.string

    @property
    def string(self):
        if self.equality and self.version:
            return "".join((self.name, self.equality, self.version))
        else:
            return self.name

    @property
    def description(self):
        s = []
        s.append(self.name)
        s.append(" ")
        s.append(self.version)
        s.append(" [")
        s.append(self._req)
        s.append("]")
        return "".join(s)

    @property
    def is_wheel(self):
        return self._is_wheel

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.string)

    def resolve(self, lookup, parent=None):
        """ Resolve this requirement and return a Package object along with
        that package's dependencies.
        """
        sys.stderr.write("Resolving {0}\n".format(self.description))
        if self in lookup:
            #print "Adding {0} as dependency of {1}".format(self, parent)
            lookup[self].add(parent)
            return None, {}
        else:
            #print "Adding {0} as dependency of {1} (new)".format(self, parent)
            lookup[self] = set([parent])
        d = mkdtemp()
        try:
            status = pip.main(["install", "-q", "-d", d, self.string])
            if status != 0:
                sys.stderr.write("!! Pip failed with "
                                 "status {0}\n".format(status))
            package, subpackages = None, {}
            for p in map(Package, listdir(d)):
                if p.name == self.name or (p.name.startswith(self.name + "-")
                                           and p.name.endswith(".whl")):
                    package = p
                else:
                    req = p.requirement
                    subpackages[req] = None
            #print "Resolving subpackages for {0} - {1}".format(package, subpackages)
            #if package is None:
            #    import ipdb; ipdb.set_trace()
            subpackages = dict((key, key.resolve(lookup, package))
                               for key in subpackages.keys())
            return package, subpackages
        finally:
            rmtree(d)


class Package(object):
    """ A Package object refers to a specific version of a package in an
    archive file.
    """

    def __init__(self, file_name):
        if file_name.endswith(".whl"):
            self.name, self.version = file_name.split("-")[0:2]
        else:
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
        """ Convert this package into a requirement specification.
        """
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
        for req in self._reqs:
            req.resolve(flat)
        out = {}
        for req, package in flat.items():
            out.setdefault(req.name, {})
            out[req.name][req.version] = package
        return out
    
    def discord(self):
        return dict(filter(lambda (k, v): len(v) > 1, self.resolve().items()))
