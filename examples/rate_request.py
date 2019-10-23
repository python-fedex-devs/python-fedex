#!/usr/bin/env python
"""
This example shows how to use the FedEx RateRequest service.
The variables populated below represents the minimum required values.
You will need to fill all of these, or risk seeing a SchemaValidationError
exception thrown by suds.

TIP: Near the bottom of the module, see how to check the if the destination
     is Out of Delivery Area (ODA).
"""
import logging
import sys

from example_config import CONFIG_OBJ
from fedex.services.rate_service import FedexRateServiceRequest
from fedex.tools.conversion import sobject_to_dict

# Un-comment to see the response from Fedex printed in stdout.
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# This is the object that will be handling our request.
# We're using the FedexConfig object from example_config.py in this dir.
customer_transaction_id = "*** RateService Request v18 using Python ***"  # Optional transaction_id
rate_request = FedexRateServiceRequest(CONFIG_OBJ, customer_transaction_id=customer_transaction_id)

# If you wish to have transit data returned with your request you
# need to uncomment the following
# rate_request.ReturnTransitAndCommit = True

# This is very generalized, top-level information.
# REGULAR_PICKUP, REQUEST_COURIER, DROP_BOX, BUSINESS_SERVICE_CENTER or STATION
rate_request.RequestedShipment.DropoffType = 'REGULAR_PICKUP'

# See page 355 in WS_ShipService.pdf for a full list. Here are the common ones:
# STANDARD_OVERNIGHT, PRIORITY_OVERNIGHT, FEDEX_GROUND, FEDEX_EXPRESS_SAVER
# To receive rates for multiple ServiceTypes set to None.
rate_request.RequestedShipment.ServiceType = 'FEDEX_GROUND'

# What kind of package this will be shipped in.
# FEDEX_BOX, FEDEX_PAK, FEDEX_TUBE, YOUR_PACKAGING
rate_request.RequestedShipment.PackagingType = 'YOUR_PACKAGING'

# Shipper's address
rate_request.RequestedShipment.Shipper.Address.StateOrProvinceCode = 'SC'
rate_request.RequestedShipment.Shipper.Address.PostalCode = '29631'
rate_request.RequestedShipment.Shipper.Address.CountryCode = 'US'
rate_request.RequestedShipment.Shipper.Address.Residential = False

# Recipient address
rate_request.RequestedShipment.Recipient.Address.StateOrProvinceCode = 'NC'
rate_request.RequestedShipment.Recipient.Address.PostalCode = '27577'
rate_request.RequestedShipment.Recipient.Address.CountryCode = 'US'
# This is needed to ensure an accurate rate quote with the response.
# rate_request.RequestedShipment.Recipient.Address.Residential = True
# include estimated duties and taxes in rate quote, can be ALL or NONE
rate_request.RequestedShipment.EdtRequestType = 'NONE'

# Who pays for the rate_request?
# RECIPIENT, SENDER or THIRD_PARTY
rate_request.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'

package1_weight = rate_request.create_wsdl_object_of_type('Weight')
# Weight, in LB.
package1_weight.Value = 1.0
package1_weight.Units = "LB"

package1 = rate_request.create_wsdl_object_of_type('RequestedPackageLineItem')
package1.Weight = package1_weight
# can be other values this is probably the most common
package1.PhysicalPackaging = 'BOX'
# Required, but according to FedEx docs:
# "Used only with PACKAGE_GROUPS, as a count of packages within a
# group of identical packages". In practice you can use this to get rates
# for a shipment with multiple packages of an identical package size/weight
# on rate request without creating multiple RequestedPackageLineItem elements.
# You can OPTIONALLY specify a package group:
# package1.GroupNumber = 0  # default is 0
# The result will be found in RatedPackageDetail, with specified GroupNumber.
package1.GroupPackageCount = 1
# Un-comment this to see the other variables you may set on a package.
# print(package1)

# This adds the RequestedPackageLineItem WSDL object to the rate_request. It
# increments the package count and total weight of the rate_request for you.
rate_request.add_package(package1)

# If you'd like to see some documentation on the ship service WSDL, un-comment
# this line. (Spammy).
# print(rate_request.client)

# Un-comment this to see your complete, ready-to-send request as it stands
# before it is actually sent. This is useful for seeing what values you can
# change.
# print(rate_request.RequestedShipment)

# Fires off the request, sets the 'response' attribute on the object.
rate_request.send_request()

# This will show the reply to your rate_request being sent. You can access the
# attributes through the response attribute on the request object. This is
# good to un-comment to see the variables returned by the FedEx reply.
# print(rate_request.response)

# This will convert the response to a python dict object. To
# make it easier to work with.
# from fedex.tools.conversion import basic_sobject_to_dict
# print(basic_sobject_to_dict(rate_request.response))

# This will dump the response data dict to json.
# from fedex.tools.conversion import sobject_to_json
# print(sobject_to_json(rate_request.response))

# Here is the overall end result of the query.
print("HighestSeverity: {}".format(rate_request.response.HighestSeverity))

# RateReplyDetails can contain rates for multiple ServiceTypes if ServiceType was set to None
for service in rate_request.response.RateReplyDetails:
    for detail in service.RatedShipmentDetails:
        for surcharge in detail.ShipmentRateDetail.Surcharges:
            if surcharge.SurchargeType == 'OUT_OF_DELIVERY_AREA':
                print("{}: ODA rate_request charge {}".format(service.ServiceType, surcharge.Amount.Amount))

    for rate_detail in service.RatedShipmentDetails:
        print("{}: Net FedEx Charge {} {}".format(service.ServiceType,
                                                  rate_detail.ShipmentRateDetail.TotalNetFedExCharge.Currency,
                                                  rate_detail.ShipmentRateDetail.TotalNetFedExCharge.Amount))

# Check for warnings, this is also logged by the base class.
if rate_request.response.HighestSeverity == 'NOTE':
    for notification in rate_request.response.Notifications:
        if notification.Severity == 'NOTE':
            print(sobject_to_dict(notification))
