#!/usr/bin/env python
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
      license='BSD',
      classifiers=CLASSIFIERS,
      keywords=KEYWORDS,
      requires=['suds'],
      install_requires=['suds'],
)
