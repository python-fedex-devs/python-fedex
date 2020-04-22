Python FedEx SOAP API Module
============================

.. image:: https://badge.fury.io/py/fedex.svg
    :target: https://badge.fury.io/py/fedex
    
.. image:: https://travis-ci.org/python-fedex-devs/python-fedex.svg?branch=master
    :target: https://travis-ci.org/python-fedex-devs/python-fedex

.. image:: https://requires.io/github/python-fedex-devs/python-fedex/requirements.svg?branch=master
     :target: https://requires.io/github/python-fedex-devs/python-fedex/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://readthedocs.org/projects/python-fedex/badge/?version=latest
     :target: http://python-fedex.readthedocs.org/en/latest/?badge=latest
     :alt: Documentation Status

:Author: Greg Taylor, Radek Wojcik
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

- Clone this repository.

- Edit the `example_config.py` file in See `examples/ <examples/>`_ with your fedex credentials and run any of the provided examples.

Documentation
-------------

Refer to the documentation_ for more details on the project. Latest doc builds
are found in docs_ and doc build scripts in doc_source_. Sphinx documentation is in doc_src_.
    
There are also a lot of useful examples under the examples directory within
this directory.

Support
-------

Issues & Questions: https://github.com/gtaylor/python-fedex/issues

Most problems are going to require investigation or a submitted 
pull request by someone from the Python FedEx Developers organization.
To contribute a new feature or service, feel free to create a pull request.
We are always looking for new contributors to help maintain the project.

Fedex Support and Documentation
-------------------------------

Fedex Support Email: websupport@fedex.com

Developer Portal: http://www.fedex.com/us/developer/

Updates To Services: https://www.fedex.com/us/developer/web-services/process.html (FedEx Web Services Announcements)


Related Projects
----------------

- FedEx Commercial Invoice Generation, see https://github.com/radzhome/fedex-commercial-invoice

Todos
-----

- Increase service specific request validation
- Remove deprecated services (package movement service)
- Pickup service unit tests

Legal
-----

Copyright (C) 2008-2015 Greg Taylor

Copyright (C) 2015-2016 Python FedEx Developers

This software is licensed under the BSD License.

python-fedex is not authored by, endorsed by, or in any way affiliated with
FedEx.

.. _documentation: https://readthedocs.org/projects/python-fedex/
.. _documentation2: https://pythonhosted.org/fedex/
.. _docs: docs/
.. _doc_source: doc_source/
.. _doc_src: doc_src/
