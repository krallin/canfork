#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = []

test_requirements = []

setup(
    name='canfork',
    version='0.2.0',
    description="Guess whether a process can fork depending on VSZ.",
    author="Thomas Orozco",
    author_email='thomas@orozco.fr',
    url='https://github.com/krallin/canfork',
    packages=[
        'canfork',
    ],
    package_dir={'canfork':
                 'canfork'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='canfork',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': ['canfork=canfork:main'],
    }
)
