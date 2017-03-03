.. _quick_start:

.. include:: global.txt

Quick Start
===========

To get you started, a comprehensive set of examples and tests is included in
the examples and tests directory respectively. The examples below are
come from the included unit tests.

Initialize Config Object
------------------------

.. code-block:: python

    from fedex.config import FedexConfig
    CONFIG_OBJ = FedexConfig(key='<key>',
                             password='<pass>',
                             account_number='<account_no>',
                             meter_number='<meter_no>')

Create and Delete a Shipment
----------------------------

.. code-block:: python

    shipment = FedexProcessShipmentRequest(CONFIG_OBJ)

    shipment.RequestedShipment.DropoffType = 'REGULAR_PICKUP'
    shipment.RequestedShipment.ServiceType = 'FEDEX_GROUND'
    shipment.RequestedShipment.PackagingType = 'YOUR_PACKAGING'

    shipment.RequestedShipment.Shipper.Contact.PersonName = 'Sender Name'
    shipment.RequestedShipment.Shipper.Contact.PhoneNumber = '9012638716'

    shipment.RequestedShipment.Shipper.Address.StreetLines = ['Address Line 1']
    shipment.RequestedShipment.Shipper.Address.City = convert_to_utf8('Herndon')
    shipment.RequestedShipment.Shipper.Address.StateOrProvinceCode = 'VA'
    shipment.RequestedShipment.Shipper.Address.PostalCode = '20171'
    shipment.RequestedShipment.Shipper.Address.CountryCode = 'US'

    shipment.RequestedShipment.Recipient.Contact.PersonName = 'Recipient Name'
    shipment.RequestedShipment.Recipient.Contact.PhoneNumber = '9012637906'

    shipment.RequestedShipment.Recipient.Address.StreetLines = ['Address Line 1']
    shipment.RequestedShipment.Recipient.Address.City = convert_to_utf8('TorontoåæâèéHerndon')
    shipment.RequestedShipment.Recipient.Address.StateOrProvinceCode = 'VA'
    shipment.RequestedShipment.Recipient.Address.PostalCode = '20171'
    shipment.RequestedShipment.Recipient.Address.CountryCode = 'US'
    shipment.RequestedShipment.EdtRequestType = 'NONE'

    shipment.RequestedShipment.ShippingChargesPayment.Payor.ResponsibleParty.AccountNumber \
        = CONFIG_OBJ.account_number

    shipment.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'

    shipment.RequestedShipment.LabelSpecification.LabelFormatType = 'COMMON2D'
    shipment.RequestedShipment.LabelSpecification.ImageType = 'PNG'
    shipment.RequestedShipment.LabelSpecification.LabelStockType = 'PAPER_7X4.75'
    shipment.RequestedShipment.LabelSpecification.LabelPrintingOrientation = 'BOTTOM_EDGE_OF_TEXT_FIRST'

    # Use order if setting multiple labels or delete
    del shipment.RequestedShipment.LabelSpecification.LabelOrder

    package1_weight = shipment.create_wsdl_object_of_type('Weight')
    package1_weight.Value = 2.0
    package1_weight.Units = "LB"
    package1 = shipment.create_wsdl_object_of_type('RequestedPackageLineItem')
    package1.PhysicalPackaging = 'ENVELOPE'
    package1.Weight = package1_weight
    shipment.add_package(package1)

    shipment.send_validation_request()
    shipment.send_request()

    assert shipment.response
    assert shipment.response.HighestSeverity == 'SUCCESS'
    track_id = shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].TrackingIds[0].TrackingNumber
    assert track_id

    del_shipment = FedexDeleteShipmentRequest(CONFIG_OBJ)
    del_shipment.DeletionControlType = "DELETE_ALL_PACKAGES"
    del_shipment.TrackingId.TrackingNumber = track_id
    del_shipment.TrackingId.TrackingIdType = 'EXPRESS'

    del_shipment.send_request()

Get the Response
----------------

Once you perform `send_request()`, you can access the `response` attribute
of the service request object. To access the response from the
above delete shipment example:

.. code-block:: python

    request_response = del_shipment.response

Validate an Address
-------------------

.. code-block:: python

    avs_request = FedexAddressValidationRequest(CONFIG_OBJ)
    address1 = avs_request.create_wsdl_object_of_type('AddressToValidate')
    address1.Address.StreetLines = ['155 Old Greenville Hwy', 'Suite 103']
    address1.Address.City = 'Clemson'
    address1.Address.StateOrProvinceCode = 'SC'
    address1.Address.PostalCode = 29631
    address1.Address.CountryCode = 'US'
    address1.Address.Residential = False
    avs_request.add_address(address1)

    avs_request.send_request()

Estimate Delivery Time
----------------------

.. code-block:: python

    avc_request = FedexAvailabilityCommitmentRequest(CONFIG_OBJ)
    avc_request.Origin.PostalCode = 'M5V 3A4'
    avc_request.Origin.CountryCode = 'CA'
    avc_request.Destination.PostalCode = '27577'  # 29631
    avc_request.Destination.CountryCode = 'US'

Validate Postal Code
--------------------

.. code-block:: python

    inquiry = FedexValidatePostalRequest(CONFIG_OBJ)
    inquiry.Address.PostalCode = '29631'
    inquiry.Address.CountryCode = 'US'

    inquiry.send_request()

FedEx Store Search
------------------

.. code-block:: python

    location_request = FedexSearchLocationRequest(CONFIG_OBJ)
    location_request.Address.PostalCode = '38119'
    location_request.Address.CountryCode = 'US'


Get Package Rate
----------------

.. code-block:: python

    rate = FedexRateServiceRequest(CONFIG_OBJ)

    rate.RequestedShipment.DropoffType = 'REGULAR_PICKUP'
    rate.RequestedShipment.ServiceType = 'FEDEX_GROUND'
    rate.RequestedShipment.PackagingType = 'YOUR_PACKAGING'

    rate.RequestedShipment.Shipper.Address.StateOrProvinceCode = 'SC'
    rate.RequestedShipment.Shipper.Address.PostalCode = '29631'
    rate.RequestedShipment.Shipper.Address.CountryCode = 'US'

    rate.RequestedShipment.Recipient.Address.StateOrProvinceCode = 'NC'
    rate.RequestedShipment.Recipient.Address.PostalCode = '27577'
    rate.RequestedShipment.Recipient.Address.CountryCode = 'US'

    rate.RequestedShipment.EdtRequestType = 'NONE'
    rate.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'

    package1_weight = rate.create_wsdl_object_of_type('Weight')
    package1_weight.Value = 1.0
    package1_weight.Units = "LB"
    package1 = rate.create_wsdl_object_of_type('RequestedPackageLineItem')
    package1.Weight = package1_weight
    package1.PhysicalPackaging = 'BOX'
    package1.GroupPackageCount = 1
    rate.add_package(package1)

    rate.send_request()

Track a Package
---------------

.. code-block:: python

    track = FedexTrackRequest(CONFIG_OBJ)
    tracking_num = '781820562774'
    track.SelectionDetails.PackageIdentifier.Type = 'TRACKING_NUMBER_OR_DOORTAG'
    track.SelectionDetails.PackageIdentifier.Value = tracking_num
    track.send_request()


Get JSON and Dictionary Response
--------------------------------

.. code-block:: python

    from fedex.tools.conversion import sobject_to_dict
    from fedex.tools.conversion import sobject_to_json
    response_dict = sobject_to_dict(shipment.response)
    response_json = sobject_to_json(shipment.response)

Advanced Requests
-----------------

Since this module is a suds wrapper, you can browse each service's WSDL
in ``fedex/wsdls`` and add any required objects to your request.

For example, the `Ship Service` WSDL has a `simpleType` definition for `ServiceType`
with the following options:

* ``'STANDARD_OVERNIGHT'``
* ``'PRIORITY_OVERNIGHT'``
* ``'FEDEX_GROUND'``
* ``'FEDEX_EXPRESS_SAVER'``
* ``'FEDEX_2_DAY'``
* ``'INTERNATIONAL_PRIORITY'``
* ``'SAME_DAY'``
* ``'INTERNATIONAL_ECONOMY'``

You can see all what is available for a specific definition by
browsing a service's WSDL. It is possible to customize your request beyond what
is included in the examples but still within the confines of
this package. If it's something common enough, please bring it
forward so that it can be included along as an example.