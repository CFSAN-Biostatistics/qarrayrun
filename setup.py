#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    "pytest",
]

setup(
    name='qarrayrun',
    version='1.0.1',
    description="A helper tool for running array jobs on an HPC computational node.",
    long_description=readme + '\n\n' + history,
    author="Steve Davis",
    author_email='steven.davis@fda.hhs.gov',
    url='https://github.com/CFSAN-Biostatistics/qarrayrun',
    packages=[
        'qarrayrun',
    ],
    package_dir={'qarrayrun':
                 'qarrayrun'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords=['bioinformatics', 'NGS', 'qarrayrun'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={'console_scripts': ['qarrayrun = qarrayrun.cli:main']},
    setup_requires=["pytest-runner"],
    tests_require=test_requirements
)
