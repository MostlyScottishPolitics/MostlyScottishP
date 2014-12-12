#!/usr/bin/env python

from setuptools import setup, find_packages
# setup script
setup(
    name='msp',
    version='0.8',
    description='Mostly Scottish Politics',
    author='Team C',
    packages=find_packages(),
    include_package_data=True, requires=['django']
)
