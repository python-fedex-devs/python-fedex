#!/usr/bin/env python
"""
This example shows how to delete existing shipments.
"""
import logging
import sys

from example_config import CONFIG_OBJ
from fedex.services.ship_service import FedexDeleteShipmentRequest
from fedex.base_service import FedexError

# Un-comment to see the response from Fedex printed in stdout.
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# This is the object that will be handling our request.
# We're using the FedexConfig object from example_config.py in this dir.
del_request = FedexDeleteShipmentRequest(CONFIG_OBJ)

# Either delete all packages in a shipment, or delete an individual package.
# Docs say this isn't required, but the WSDL won't validate without it.
# DELETE_ALL_PACKAGES, DELETE_ONE_PACKAGE
del_request.DeletionControlType = "DELETE_ALL_PACKAGES"

# The tracking number of the shipment to delete.
del_request.TrackingId.TrackingNumber = '794798682968'  # '111111111111' will also not delete

# What kind of shipment the tracking number used.
# Docs say this isn't required, but the WSDL won't validate without it.
# EXPRESS, GROUND, or USPS
del_request.TrackingId.TrackingIdType = 'EXPRESS'

# Fires off the request, sets the 'response' attribute on the object.
try:
    del_request.send_request()
except FedexError as e:
    if 'Unable to retrieve record' in str(e):
        print "WARNING: Unable to delete the shipment with the provided tracking number."
    else:
        print(e)

# See the response printed out.
# print(del_request.response)

# This will convert the response to a python dict object. To
# make it easier to work with.
# from fedex.tools.conversion import basic_sobject_to_dict
# print(basic_sobject_to_dict(del_request.response))

# This will dump the response data dict to json.
# from fedex.tools.conversion import sobject_to_json
# print(sobject_to_json(del_request.response))

# Here is the overall end result of the query.
print("HighestSeverity: {}".format(del_request.response.HighestSeverity))
