#!/usr/bin/env python
"""
PostalCodeInquiryRequest classes are used to validate and receive additional
information about postal codes.
"""
import logging
from example_config import CONFIG_OBJ
from fedex.services.package_movement import PostalCodeInquiryRequest

# Set this to the INFO level to see the response from Fedex printed in stdout.
logging.basicConfig(level=logging.INFO)

# We're using the FedexConfig object from example_config.py in this dir.
inquiry = PostalCodeInquiryRequest(CONFIG_OBJ)
inquiry.PostalCode = '29631'
inquiry.CountryCode = 'US'

# Fires off the request, sets the 'response' attribute on the object.
inquiry.send_request()

# See the response printed out.
print inquiry.response