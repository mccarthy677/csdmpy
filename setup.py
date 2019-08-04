#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import find_packages
from setuptools import setup

# from csdmpy._version import __version__

# Package meta-data.
NAME = "csdmpy"
DESCRIPTION = "A python module for importing and exporting CSD model file-format."
URL = "https://github.com/DeepanshS/csdmpy"
EMAIL = "srivastava.89@osu.edu"
AUTHOR = "Deepansh Srivastava"
REQUIRES_PYTHON = ">=3.6"
VERSION = "0.1.0"

# What packages are required for this module to be executed?
REQUIRED = [
    "numpy>=1.13.3",
    "setuptools>=27.3",
    "astropy>=3.0",
    "requests>=2.21.0",
    "matplotlib>=3.0.2",
]

SETUP_REQUIRES = ["setuptools>=27.3"]

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier
# for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    # extras_require=EXTRAS,
    setup_requires=SETUP_REQUIRES,
    tests_require=["pytest", "pytest-runner"],
    include_package_data=True,
    license="BSD-3-Clause",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        # 'Programming Language :: Python :: Implementation :: CPython',
        # 'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
