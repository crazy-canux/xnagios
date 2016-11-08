#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Auto config and deploy nagios configuration.

Copyright (C) 2015 Canux CHENG
All rights reserved.
Name: setup.py
Author: Canux CHENG canuxcheng@gmail.com
Version: V1.0.0.0
Time: Fri 05 Aug 2016 09:59:29 AM CST

Exapmle:
    ./nagios -h
"""
import os

from setuptools import setup, find_packages

import nagios


def read(readme):
    """Give reST format README for pypi."""
    extend = os.path.splitext(readme)[1]
    if (extend == '.rst'):
        import codecs
        return codecs.open(readme, 'r', 'utf-8').read()
    elif (extend == '.md'):
        import pypandoc
        return pypandoc.convert(readme, 'rst')

INSTALL_REQUIRES = [
]

setup(
    name='znagios',
    version=nagios.__version__,
    author='Canux CHENG',
    author_email='canuxcheng@gmail.com',
    maintainer='Canux CHENG',
    maintainer_email='canuxcheng@gmail.com',
    description='Congiruration and deploy nagios configuration automatic.',
    long_description=read('README.rst'),
    license='GPL',
    platforms='any',
    keywords='monitoring nagios configuration tools',
    url='https://github.com/crazy-canux/znagios',
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: System :: Monitoring"
    ],
)
