# -*- coding: utf-8 -*-
#

from setuptools import setup
import os
import sys


long_description = """
owmeta-sciunit
==============
Provides owmeta-core types for storing and loading Sciunit models
"""


for line in open('owmeta_sciunit/__init__.py'):
    if line.startswith("__version__"):
        version = line.split("=")[1].strip()[1:-1]


setup(
    name='owmeta',
    setup_requires=['pytest-runner'],
    install_requires=[
        'owmeta-core',
        'sciunit',
        'neuronunit',
        'rdflib>=4.1.2',
    ],
    version=version,
    packages=['owmeta_sciunit'],
    author='OpenWorm.org authors and contributors',
    author_email='info@openworm.org',
    description='Provides owmeta-core types for storing and loading Sciunit models',
    long_description=long_description,
    license='MIT',
    url='https://owmeta-sciunit.readthedocs.io/en/latest/',
    download_url='https://github.com/openworm/owmeta-sciunit/archive/master.zip',
    entry_points={
        'owmeta_core.commands': [
            'sciunit = owmeta_sciunit.command:OWMSciunit',
        ],
        'owmeta_core.cli_hints': 'hints = owmeta_sciunit.cli_hints:CLI_HINTS',
    },
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering'
    ]
)
