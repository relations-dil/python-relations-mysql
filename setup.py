#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="relations-mysql",
    version="0.6.4",
    package_dir = {'': 'lib'},
    py_modules = [
        'relations_mysql',
        'relations_mysql.sql',
        'relations_mysql.expression',
        'relations_mysql.criterion',
        'relations_mysql.criteria',
        'relations_mysql.clause',
        'relations_mysql.query',
        'relations_mysql.ddl',
        'relations_mysql.column',
        'relations_mysql.index',
        'relations_mysql.table'
    ],
    install_requires=[
        'relations-sql>=0.6.8'
    ],
    url="https://github.com/relations-dil/python-relations-mysql",
    author="Gaffer Fitch",
    author_email="relations@gaf3.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license_files=('LICENSE.txt',),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]
)
