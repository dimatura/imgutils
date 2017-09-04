#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'numpy',
    'pillow'
]

setup_requirements = [
    # 'pytest-runner',
]

test_requirements = [
    # 'pytest',
]

setup(
    name='imgutils',
    version='0.1.2',
    description="Miscellaneous image utility functions.",
    long_description=readme,
    author="Daniel Maturana",
    author_email='dimatura@cmu.edu',
    url='https://github.com/dimatura/imgutils',
    packages=find_packages(include=['imgutils']),
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='imgutils',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
