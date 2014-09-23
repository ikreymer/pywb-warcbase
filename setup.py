#!/usr/bin/env python
# vim: set sw=4 et:

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_suite = True

    def run_tests(self):
        import pytest
        import sys
        import os
        cmdline = ' --cov warcbase -v tests/'
        errcode = pytest.main(cmdline)
        sys.exit(errcode)

setup(
    name='pywb-warcbase',
    version='0.1.0',
    url='https://github.com/ikreymer/pywb-warcbase',
    author='Ilya Kreymer',
    author_email='ikreymer@gmail.com',
    description='WarcBase Client for pywb',
    long_description='WarcBase Client for pywb',
    license='GPL',
    packages=find_packages(),
    provides=[
        'warcbase',
        ],
    install_requires=[
        'pywb==0.6.1',
        ],
    dependency_links=[
        "git+git://github.com/ikreymer/pywb.git@develop#egg=pywb-0.6.1"
    ],
    zip_safe=False,
    cmdclass={'test': PyTest},
    test_suite='',
    tests_require=[
        'pytest',
        'pytest-cov',
        'httmock',
    ])
