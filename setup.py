#!/usr/bin/env python
"""
 python-fedex 
 Copyright (C) 2009 Gregory Taylor

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from distutils.core import setup
import fedex

LONG_DESCRIPTION = open('README.rst').read()

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

KEYWORDS = 'fedex soap suds wrapper'

setup(name='fedex',
      version=fedex.VERSION,
      description='Fedex Web Services API wrapper.',
      long_description=LONG_DESCRIPTION,
      author='Gregory Taylor',
      author_email='snagglepants@gmail.com.com',
      url='http://code.google.com/p/python-fedex/',
      download_url='http://pypi.python.org/pypi/fedex/',
      packages=['fedex', 'fedex.services', 'fedex.printers'],
      package_dir={'fedex': 'fedex'},
      package_data={'fedex': ['wsdl/*.wsdl', 'wsdl/test_server_wsdl/*.wsdl']},
      platforms=['Platform Independent'],
      license='GPLv3',
      classifiers=CLASSIFIERS,
      keywords=KEYWORDS,
      requires=['suds'],
      install_requires=['suds'],
)
