#!/usr/bin/env python
from setuptools import setup

setup(
    name="brittbot",
    version="0.1.0",
    author="Britt Gresham",
    author_email="britt@brittg.com",
    description=("My IRC Bot"),
    license="MIT",
    install_requires=[
        'Flask',
        'flask-socketio',
    ],
    test_require=[
        'mock',
    ],
)
