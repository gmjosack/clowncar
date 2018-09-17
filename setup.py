#!/usr/bin/env python

import setuptools
from distutils.core import setup

exec(open('clowncar/version.py').read())

kwargs = {
    "name": "clowncar",
    "version": str(__version__),
    "packages": ["clowncar"],
    "description": "Simple client side load balancing module.",
    # PyPi, despite not parsing markdown, will prefer the README.md to the
    # standard README. Explicitly read it here.
    "long_description": open("README").read(),
    "author": "Gary M. Josack",
    "maintainer": "Gary M. Josack",
    "author_email": "gary@byoteki.com",
    "maintainer_email": "gary@byoteki.com",
    "license": "MIT",
    "url": "https://github.com/gmjosack/clowncar",
    "download_url": "https://github.com/gmjosack/clowncar/archive/master.tar.gz",
    "classifiers": [
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
}

setup(**kwargs)
