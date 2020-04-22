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

KEYWORDS = 'fedex soap suds wrapper rate track avs location ship pickup country availability commitment package service'

setup(name='fedex',
      version=fedex.VERSION,
      description='Fedex Web Services API wrapper.',
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/x-rst',
      author='Greg Taylor, Rad Wojcik',
      author_email='gtaylor@gc-taylor.com',
      maintainer='Python Fedex Developers',
      url='https://github.com/python-fedex-devs/python-fedex',
      download_url='http://pypi.python.org/pypi/fedex/',
      packages=['fedex', 'fedex.services', 'fedex.printers'],
      package_dir={'fedex': 'fedex'},
      package_data={'fedex': ['wsdl/*.wsdl', 'wsdl/test_server_wsdl/*.wsdl', 'tools/*']},
      platforms=['Platform Independent'],
      license='BSD',
      classifiers=CLASSIFIERS,
      keywords=KEYWORDS,
      requires=['suds'],
      install_requires=['suds-jurko'],
      )
