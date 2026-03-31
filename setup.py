#!/usr/bin/env python

from setuptools import setup


requirements = open('requirements.txt').read()
readme = open('README.rst').read()

setup(
    name="similar",
    version="1.0.0",
    url='http://github.com/ncrocfer/similar',
    author='Nicolas Crocfer',
    author_email='ncrocfer@gmail.com',
    description="A similar text finder written in Python",
    long_description=readme,
    packages=['similar'],
    include_package_data=True,
    install_requires=requirements,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14'
    ),
    python_requires=">=3.10",
)