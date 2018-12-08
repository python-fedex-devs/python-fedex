.. _services:

.. include:: global.txt

Implemented Services
====================

python-fedex implements various `FedEx Web Services`_. These
services along with the implemented functionality is
described below.

Ship Service
------------

Generates (FedEx Waybill) and deletes shipments.

.. autoclass:: fedex.services.ship_service.FedexProcessShipmentRequest

.. autoclass:: fedex.services.ship_service.FedexDeleteShipmentRequest

Rate Service
------------

Calculates the cost of a shipment.

.. autoclass:: fedex.services.rate_service.FedexRateServiceRequest


Validation Availability And Commitment Service
----------------------------------------------

Calculates the estimated arrival time of a shipment.

.. autoclass:: fedex.services.availability_commitment_service.FedexAvailabilityCommitmentRequest


Track Service
-------------

Returns tracking information for a given tracking number.

.. autoclass:: fedex.services.track_service.FedexTrackRequest

Address Validation Service
--------------------------

Validates and cleans a given address.

.. autoclass:: fedex.services.address_validation_service.FedexAddressValidationRequest


Location Service
----------------

Returns FedEx store locations based on a given location query.

.. autoclass:: fedex.services.location_service.FedexSearchLocationRequest


Country Service
---------------

Validates the postal codes for a given address.

.. autoclass:: fedex.services.country_service.FedexValidatePostalRequest


Pickup Service
--------------

Creates a FedEx pickup request.

.. autoclass:: fedex.services.pickup_service.FedexCreatePickupRequest

Queries pickup availability.

.. autoclass:: fedex.services.pickup_service.FedexPickupAvailabilityRequest


Package Movement Service
------------------------

DEPRECATED service that was used to validate postal codes and
calculate shipment arrival times. Replaced with two distinct services:
Validation Availability And Commitment Service, and Country Service.

.. autoclass:: fedex.services.country_service.FedexValidatePostalRequest
