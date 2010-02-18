#!/usr/bin/env python

from distutils.core import setup

classifiers = """Programming Language :: Python
License :: OSI Approved :: GNU General Public License (GPL)
Operating System :: OS Independent
Development Status :: 4 - Beta
Environment :: Web Environment
Intended Audience :: Developers
Topic :: Internet :: WWW/HTTP
Topic :: Software Development :: Libraries :: Python Modules""".splitlines()

#from README.txt
long_description = """
============================================================
socialgraph - a python wrapper for google's Social Graph API
============================================================

The `Google Social Graph API <http://code.google.com/apis/socialgraph/>`_
makes information about the public connections between people on the web more
easily available. **socialgraph** is a python wrapper for the web api.


Installation
------------

**development version**::

    git clone git@github.com:hoffmann/python-socialgraph.git
    cd python-socialgraph
    sudo python setup.py install

**from pypi.python.org**::

    pip install socialgraph
"""

setup(name='socialgraph',
      version='0.2.3',
      description='''Python wrapper for Google's Social Graph API''',
      author='Peter Hoffmann',
      author_email='ph@peter-hoffmann.com',
      url='http://www.peter-hoffmann.com/code/python-socialgraph/',
      license='GPL',
      platforms=['any'],
      py_modules=['socialgraph'],
      classifiers=classifiers,
      long_description=long_description)
