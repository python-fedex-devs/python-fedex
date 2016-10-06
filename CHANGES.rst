Change Log
==========

2.4.0
-----

* Pickup Service usingv11 WSDL (hornedbull)
* Added documentation and unit tests for Pickup Service. (radzhome)
* Update package data to include tools (noodlebreak)

2.3.1
-----

* Set fedex logging to INFO for tests. (radzhome)
* Sphinx documentation (hosted on read the docs). (radzhome)
* Update Ship Service test to allow warnings. (radzhome)
* Added log warning for requests that yield a WARNING. (radzhome)

2.3.0
-----

* Added Location Service using v3 WSDL. (radzhome)
* Added examples and unit tests for Location Service. (radzhome)
* Updated certification process scripts to work with latest WSDLs. (radzhome)
* Added warning logging for requests that come back with warning notes. (radzhome)
* Added PyPI, Travis, requires.io integration/badges. (radzhome)
* Organization change from gtaylor to python-fedex-devs. (gtaylor)
* Added deprecation message for movement service. (radzhome)
* Added conversion tools to convert suds xml object into python dict. (radzhome)
* Redirect logging to stdout for examples and tests when not ran via nose. (radzhome)

2.2.0
-----

* Added Country Service / Postal Code Validation service. (radzhome)
* Added CountryService_v4.wsdl for Postal Code Validation. (radzhome)
* Added unit tests and examples for Country service. (radzhome)
* Added Signature Option to ship example. (radzhome)
* Fix base service logging request and response. (radzhome)

2.1.0
-----

* Added Validation, Availability and Commitment (AVC) service. (radzhome)
* Added [Validation]AvailabilityAndCommitmentService_v4.wsdl for AVC service. (radzhome)
* Added examples and unit tests for AVC service.
* Refactored examples and documentation. (radzhome)
* A quick PEP8 pass using pycharm on most of the codebase (radzhome)
* Add travis yml (radzhome)


2.0.0
-----

* Bump ShipService WSDL to v17 for create and delete shipment. (radzhome)
* Bump AddressValidation WSDL to v4. (radzhome)
* Bump RateService WSDL to v18. (radzhome)
* Bump TrackService WSDL to v10. (radzhome)
* General improvements to base class. (radzhome)
* Refactoring and updates to examples. (radzhome)
* Added test classes. (radzhome)
* Remove old and unused WSDLs. (radzhome)
* Change dependency to suds-jurko to include python 3 support. (radzhome)

1.1.1
-----

* Made RateService_v16.wsdl point at ws.fedex.com instead of
  wsbeta.fedex.com. Fixes issues in production. (ikks)

1.1.0
-----

* A quick PEP8 pass on most of the codebase. Yucky. (gtaylor)
* Changing recommended install method to use pip + PyPi. (radzhome)
* Updated rate_request and freight_rate_request examples for WSDL v16
  compatibility. (foxxyz)
* Updated rate service WSDL from v8 to v16. (foxxyz)
* Added a freight rate request example (mwcbrent)
* Bump ShipService WSDL to v13. (mwcbrent)
* Update rate example to show multiple ServiceTypes. (danielatdattrixdotcom)

1.0.14
------

* Re-licensed under BSD.

1.0.12 and 1.0.13
-----------------

* Forget that these ever existed.

1.0.11
------

* Bug fix of a bug fix for regions config. (jcartmell)

1.0.10
------

* Bug fix regarding regions and when they are sent. (jcartmell)

1.0.9
-----

* Various fixes to RateRequest() FedEx API call. (jcartmell)
* Added this changelog. (gtaylor)

1.0.8
-----

* Fixed some problems with the unit tests. (gtaylor)

1.0.7
-----

* Fixed a bug with international rate request example. (gtaylor)

1.0.6
-----

* Lots of documentation improvements. (gtaylor)
* FedEx RateRequest call implemented. (yahtib)
* FedEx Postal Inquiry call implemented. (yahtib)

1.0.4
-----

* Removal of unecessary files. (gtaylor)
* Documentation improvements. (gtaylor)

1.0.3
-----

* Wrote some label certification modules that can help
  with the label certification process. (gtaylor)
