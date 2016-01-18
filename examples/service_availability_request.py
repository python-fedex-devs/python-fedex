#!/usr/bin/env python
"""
This example shows how to use the FedEx Service Validation,
Availability and Commitment Service.
The variables populated below represents common values.
You will need to fill out the required values or risk seeing a SchemaValidationError
exception thrown by suds.
"""
import logging
import sys
import datetime

from example_config import CONFIG_OBJ
from fedex.services.availability_commitment_service import FedexAvailabilityCommitmentRequest

# Un-comment to see the response from Fedex printed in stdout.
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# This is the object that will be handling our service availability request.
# We're using the FedexConfig object from example_config.py in this dir.
customer_transaction_id = "*** AvailabilityAndCommitment Request v4 using Python ***"  # Optional transaction_id
avc_request = FedexAvailabilityCommitmentRequest(CONFIG_OBJ, customer_transaction_id=customer_transaction_id)

# Specify the origin postal code and country code. These fields are required.
avc_request.Origin.PostalCode = '29631'
avc_request.Origin.CountryCode = 'US'

# Specify the destination postal code and country code. These fields are required.
avc_request.Destination.PostalCode = '27577'
avc_request.Destination.CountryCode = 'US'

# Can be set to FEDEX_TUBE, YOUR_PACKAGING, FEDEX_BOX etc.. Defaults to YOUR_PACKAGING if not set.
# avc_request.Packaging = 'FEDEX_ENVELOPE'

# Can be set to the expected date. Defaults to today if not set.
avc_request.ShipDate = datetime.date.today().isoformat()

# Can be set to PRIORITY_OVERNIGHT, FEDEX_2_DAY, STANDARD_OVERNIGHT etc.. Defaults to showing all options if not set.
# avc_request.Service = 'FEDEX_2_DAY'

# Fires off the request, sets the 'response' attribute on the object.
avc_request.send_request()

# If you'd like to see some documentation on the ship service WSDL, un-comment this line.
print(avc_request.client)

# Un-comment this to see your complete, ready-to-send request as it stands
# before it is actually sent. This is useful for seeing what values you can change.
# print(avc_request.Origin)
# print(avc_request.Destination)
# print(avc_request.ShipDate)
# print(avc_request.CarrierCode)
# print(avc_request.Service)
# print(avc_request.Packaging)

# This will show the reply to your avc_request being sent. You can access the
# attributes through the response attribute on the request object. This is
# good to un-comment to see the variables returned by the FedEx reply.
# print(avc_request.response)

# This will convert the response to a python dict object. To
# make it easier to work with.
# from fedex.tools.conversion import basic_sobject_to_dict
# print(basic_sobject_to_dict(avc_request.response))

# This will dump the response data dict to json.
# from fedex.tools.conversion import sobject_to_json
# print(basic_sobject_to_dict(avc_request.response))

# Here is the overall end result of the query.
print("HighestSeverity: {}".format(avc_request.response.HighestSeverity))
print("")

# Cycle through all the Notifications
for notification in avc_request.response.Notifications:
    print("Notification:")
    print("Severity {} Source {}".format(notification.Severity, notification.Source))
    if hasattr(notification, 'Code'):
        print("Code {}".format(notification.Code))
    if hasattr(notification, 'Message'):
        print("Message {}".format(notification.Message))
    if hasattr(notification, 'LocalizedMessage'):
        print("LocalizedMessage {}".format(notification.LocalizedMessage))
    print("")

# Cycle through all the shipping options
for option in avc_request.response.Options:
    print("Ship Option:")
    if hasattr(option, 'Service'):
        print("Service {}".format(option.Service))
    if hasattr(option, 'DeliveryDate'):
        print("DeliveryDate {}".format(option.DeliveryDate))
    if hasattr(option, 'DeliveryDay'):
        print("DeliveryDay {}".format(option.DeliveryDay))
    if hasattr(option, 'DestinationStationId'):
        print("DestinationStationId {}".format(option.DestinationStationId))
    if hasattr(option, 'DestinationAirportId'):
        print("DestinationAirportId {}".format(option.DestinationAirportId))
    if hasattr(option, 'TransitTime'):
        print("TransitTime {}".format(option.TransitTime))
    print("")
