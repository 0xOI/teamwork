#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import argparse

import teamwork.modes
from teamwork import __version__
from teamwork.utils.introspect_utils import find_classes_in_package
from teamwork.plugin_bases import ModePlugin


def main():
    parser = argparse.ArgumentParser(
        description='Virtual agent at your service !)')
    parser.add_argument('-v', '--version', action='version', version=__version__)
    subparsers = parser.add_subparsers(title='Modes')

    # add modes and associated cli parsers
    for plugin in find_classes_in_package(teamwork.modes):
        if issubclass(plugin, ModePlugin):
            plugin().add_parser(subparsers)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    exit(main())



