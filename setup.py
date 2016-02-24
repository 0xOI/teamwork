#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from setuptools import find_packages
from setuptools import setup

import teamwork

setup(
    name='teamwork',
    version=teamwork.__version__,
    author='releaseeng@yelp.com',
    author_email='releaseeng@yelp.com',
    license='Copyright Yelp 2014',
    packages=find_packages(),
    description='Team of Bad@$$ virtual agents at your service !)',
    long_description="""
       Team Work makes the Dream Work.
    """,
    install_requires=[
        'argparse==1.2.1',
        'elk==0.3',
        'Flask==0.10.1',
        'makeTorrent==0.14'
    ],
    entry_points={
        'console_scripts': [
            'bot = teamwork.bot:main'
        ],
    }
)
