"""
python-fedex API Documentation
==============================
The python-fedex module is a light wrapper around Fedex's Web Services SOAP API.
Using the excellent U{suds<https://fedorahosted.org/suds/>} SOAP client,
the Fedex requests and responses are trivial to work with.

What python-fedex is
--------------------
    - A light wrapper around Fedex Web Services SOAP API.
    - Simple and easy to use.
    - Minimal by design.

What python-fedex is not
------------------------
    - An abstraction layer. python-fedex only assembles the needed SOAP calls
        and returns a SOAP response through suds. This is easy enough to work with
        that no abstraction is needed. Doing so would limit your use of the data.
    - Anything more than a light wrapper.
    
A note on completeness
----------------------
python-fedex was created for use with some of my internal projects. For the
initial release, only the things that I needed at the time were implemented.
If there is missing functionality, please report an U{issue<http://code.google.com/p/python-fedex/issues/list>}
so that I may make this module more useful to others. Likewise, feel free to
submit patches as well if you would like to help.

Getting Started
---------------
The best place to get started is by viewing the examples in the 'examples'
directory. These should be very self-explanatory. For further details, you
may review the API here, or get support by reading the instructions in the
appropriately named section below.

The L{services} module is also a good place to start looking at the different
objects used for issuing Fedex requests.

As a general tip, the best way to see which attributes are available on WSDL
objects is to simply print them, hitting their __str__() method.

Fedex Documentation
-------------------
If you are wondering what attributes or variables are present, you'll want to
refer to the Fedex Web Services documentation at http://fedex.com/developer/.
Complete specification documents are there, which correspond very closely with
what you'll be able to do with python-fedex.
    
Getting Support
---------------
If you have any questions, problems, ideas, or patch submissions, please visit
our U{Google Code project<http://code.google.com/p/python-fedex/>} and enter
an issue in the U{Issue Tracker<http://code.google.com/p/python-fedex/issues/list>}.
"""
VERSION = '1.0.14'
