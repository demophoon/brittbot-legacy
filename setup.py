#!/usr/bin/env python
from setuptools import setup

setup(
    name="Brittbot",
    version="1.0.0",
    author="Britt Gresham",
    author_email="brittbot@brittg.com",
    description=("My IRC Bot"),
    license="MIT",
    install_requires=[
        "pillow",
        "textblob",
        "python-dateutil",
        "beautifulsoup",
        "pylast",
        "lxml",
        "sqlalchemy",
    ],
)
