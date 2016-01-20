Python FedEx SOAP API Module
============================

.. image:: https://badge.fury.io/py/fedex.svg
    :target: https://badge.fury.io/py/fedex
    
.. image:: https://travis-ci.org/python-fedex-devs/python-fedex.svg?branch=master
    :target: https://travis-ci.org/python-fedex-devs/python-fedex

.. image:: https://requires.io/github/python-fedex-devs/python-fedex/requirements.svg?branch=master
     :target: https://requires.io/github/python-fedex-devs/python-fedex/requirements/?branch=master
     :alt: Requirements Status
     
:Author: Greg Taylor
:Maintainer: Python FedEx Developers
:License: BSD
:Status: Stable

What is it?
-----------

A light wrapper around FedEx's Webservice Soap API. We don't do much of any
validation, but we'll help you sort through the pile of SOAP objects FedEx
uses.

Installation
------------

The easiest way is via pip or easy_install::

    pip install fedex

Quick Start
-----------

Edit the `example_config.py` file in `examples/` with your fedex credentials
and run any of the provided examples.

Documentation
-------------

Refer to the documentation_ for more details on the project.
    
There are also a lot of useful examples under the examples directory within
this directory.

Support
-------

Head over to https://github.com/gtaylor/python-fedex/issues
and submit an issue if you have any problems or questions. 
Most problems are going to require investigation or a submitted 
pull request by someone from the Python FedEx Developers organization.
To contribute a new feature or service, feel free to create a pull request.

Fedex Support and Documentation
-------------------------------

Fedex Support Email: websupport@fedex.com
Developer Portal: http://www.fedex.com/us/developer/

Todos
-----
 * Read the docs documentation
 * Travis test integration
 * Increase validation
 * Remove deprecated services

Legal
-----

Copyright (C) 2008-2015 Greg Taylor
Copyright (C) 2016 Python FedEx Developers

This software is licensed under the BSD License.

python-fedex is not authored by, endorsed by, or in any way affiliated with
FedEx.

.. _documentation: https://pythonhosted.org/fedex/
