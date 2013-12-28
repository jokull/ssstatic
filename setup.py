#!/usr/bin/env python
# encoding=utf-8

"""Pythonic Setup for ssstatic."""


from setuptools import setup


setup(
    version='0.7',
    name='ssstatic',
    description='Push a website assets to S3 with or without prefix cache busting.',
    author=u'Jökull Sólberg Auðunsson',
    author_email='jokull@solberg.is',
    license='See LICENSE.',
    url='https://github.com/jokull/ssstatic',
    packages=['ssstatic'],
    entry_points={
        'console_scripts': ['ssstatic = ssstatic:main']
    },
    install_requires=['boto>=2.8'],
)
