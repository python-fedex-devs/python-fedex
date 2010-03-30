#!/usr/bin/env python
"""
This example shows how to validate addresses. Note that the validation
class can handle up to 100 addresses for validation.
"""
import logging
from example_config import CONFIG_OBJ
from fedex.services.address_validation_service import FedexAddressValidationRequest

# Set this to the INFO level to see the response from Fedex printed in stdout.
logging.basicConfig(level=logging.INFO)

# This is the object that will be handling our tracking request.
# We're using the FedexConfig object from example_config.py in this dir.
address = FedexAddressValidationRequest(CONFIG_OBJ)

address1 = address.create_wsdl_object_of_type('AddressToValidate')
address1.CompanyName = 'International Paper'
address1.Address.StreetLines = ['155 Old Greenville Hwy', 'Suite 103']
address1.Address.City = 'Clemson'
address1.Address.StateOrProvinceCode = 'SC'
address1.Address.PostalCode = 29631
address1.Address.CountryCode = 'US'
address1.Address.Residential = False

address.add_address(address1)
address.send_request()
print address.response
