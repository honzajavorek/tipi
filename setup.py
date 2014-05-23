# -*- coding: utf-8 -*-


import os
import re
import sys
import shlex
import subprocess

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages  # NOQA


base_path = os.path.dirname(__file__)


# version
meta_file = os.path.join(base_path, 'tipi/__init__.py')
meta_file_contents = open(meta_file).read()
meta = dict(re.findall(r'__([^_]+)__ = \'([^\']*)\'', meta_file_contents))


# release a version, publish to GitHub and PyPI
if sys.argv[-1] == 'publish':
    command = lambda cmd: subprocess.check_call(shlex.split(cmd))
    command('git tag v' + meta['version'])
    command('git push --tags origin master:master')
    command('python setup.py sdist upload')
    sys.exit()


setup(
    name=meta['title'],
    version=meta['version'],
    description='Typographic replacements in HTML',
    long_description=open('README.rst').read(),
    author=meta['author'],
    author_email='mail@honzajavorek.cz',
    url='https://github.com/honzajavorek/tipi',
    license=open('LICENSE').read(),
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=['lxml'],
    zip_safe=False,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Markup :: HTML',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    )
)
