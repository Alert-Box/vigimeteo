#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='vigimeteo',
    version=__import__("vigimeteo").__version__,
    packages=find_packages(),
    author="Olivier Watte",
    author_email="owatte@emnet.cc",

    description=' '.join(["Current French West Indies weather awareness level",
                          "(Vigilance Meteo)"]),
    long_description=open('README.md').read(),

    include_package_data=True,
    url='https://github.com/Alert-Box/vigimeteo',

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        " ".join(["License :: OSI Approved :: GNU Lesser General Public",
                  "License v3 or later (LGPLv3+)"]),
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
    ],
    install_requires=[
        "beautifulsoup4==4.4.1",
        "bs4==0.0.1",
        "pdfminer==20110515",
        "six==1.10.0",
    ],
    entry_points={
        'console_scripts': [
            'vigimeteo = vigimeteo.vigimeteo:run',
        ],
    },
)
