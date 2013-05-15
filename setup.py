#!/usr/bin/env python
# encoding=utf-8

"""Pythonic Setup for ssstatic."""


import setuptools


setuptools.setup(
    version='0.3',
    name='ssstatic',
    description='Push a folder of assets to S3 with guaranteed cache busting.',
    author=u'Jökull Sólberg Auðunsson',
    author_email='jokull@solberg.is',
    license='See LICENSE.',
    url='https://github.com/jokull/ssstatic',
    scripts=['ssstatic'],
    install_requires=['boto>=2.8'],
)
