Change Log
==========

1.1.1
-----

* Made RateService_v16.wsdl point at ws.fedex.com instead of
  wsbeta.fedex.com. Fixes issues in production. (ikks)

1.1.0
-----

* A quick PEP8 pass on most of the codebase. Yucky. (gtaylor)
* Changing recommended install method to use pip + PyPi. (radlws)
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
