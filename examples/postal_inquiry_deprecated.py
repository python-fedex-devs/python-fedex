#!/usr/bin/env python
"""
PostalCodeInquiryRequest classes are used to validate and receive additional
information about postal codes.
"""
import logging
import sys
import warnings
from example_config import CONFIG_OBJ
from fedex.services.package_movement import PostalCodeInquiryRequest
from fedex.tools.conversion import sobject_to_dict

# Un-comment to see the response from Fedex printed in stdout.
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

warnings.simplefilter('always', DeprecationWarning)  # Show deprecation on this module in py2.7.

# We're using the FedexConfig object from example_config.py in this dir.
inquiry = PostalCodeInquiryRequest(CONFIG_OBJ)
inquiry.PostalCode = '29631'
inquiry.CountryCode = 'US'

# If you'd like to see some documentation on the ship service WSDL, un-comment
# this line. (Spammy).
# print(inquiry.client)

# Un-comment this to see your complete, ready-to-send request as it stands
# before it is actually sent. This is useful for seeing what values you can
# change.
# print(inquiry.CarrierCode)
# print(inquiry.ClientDetail)
# print(inquiry.TransactionDetail)

# Fires off the request, sets the 'response' attribute on the object.
inquiry.send_request()

# See the response printed out.
# print(inquiry.response)

# This will convert the response to a python dict object. To
# make it easier to work with.
# from fedex.tools.conversion import basic_sobject_to_dict
# print(basic_sobject_to_dict(inquiry.response))

# This will dump the response data dict to json.
# from fedex.tools.conversion import sobject_to_json
# print(sobject_to_json(inquiry.response))

# Here is the overall end result of the query.
print("HighestSeverity: {}".format(inquiry.response.HighestSeverity))
print("ExpressFreightContractorDeliveryArea: {}".format(sobject_to_dict(inquiry.response.ExpressDescription)))
print("ExpressDescription: {}".format(sobject_to_dict(inquiry.response.ExpressFreightDescription)))
