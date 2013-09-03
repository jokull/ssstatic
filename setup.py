#!/usr/bin/env python
# encoding=utf-8

"""Pythonic Setup for ssstatic."""


import setuptools


setuptools.setup(
    version='0.5',
    name='ssstatic',
    description='Push a website assets to S3 with or without prefix cache busting.',
    author=u'Jökull Sólberg Auðunsson',
    author_email='jokull@solberg.is',
    license='See LICENSE.',
    url='https://github.com/jokull/ssstatic',
    scripts=['ssstatic'],
    install_requires=['boto>=2.8'],
)
