#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from importlib import import_module
from inspect import isclass
from os.path import dirname
from pkgutil import iter_modules


def find_classes_in_package(package):
    """ Generator which returns every class in a module included within a package

    :param package: The package in which to search
    :return: A generator of class objects
    """
    for module_name in find_modules_in(package):
        module = import_module('{}.{}'.format(package.__name__, module_name))
        for cls in find_classes_in_module(module):
            yield cls


def find_classes_in_module(module):
    """ Generator which returns every class in a module

    :param module: The module in which to search
    :return: A generator of class objects
    """
    for name in dir(module):
        obj = getattr(module, name)
        if isclass(obj) and obj.__module__ == module.__name__:
            yield obj


def find_modules_in(package):
    """ Generator which returns every module in a package.

    :param package: The package in which to search:
    :return: A generator of module names
    """
    for (loader, name, ispkg) in iter_modules([dirname(package.__file__)]):
        yield name
