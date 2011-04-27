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
connection = FedexAddressValidationRequest(CONFIG_OBJ)

# The AddressValidationOptions are created with default values of None, which
# will cause WSDL validation errors. To make things work, each option needs to
# be explicitly set or deleted.

## Set the flags we want to True (or a value).
connection.AddressValidationOptions.CheckResidentialStatus = True
connection.AddressValidationOptions.VerifyAddresses = True
connection.AddressValidationOptions.RecognizeAlternateCityNames = True
connection.AddressValidationOptions.MaximumNumberOfMatches = 3

## Delete the flags we don't want.
del connection.AddressValidationOptions.ConvertToUpperCase
del connection.AddressValidationOptions.ReturnParsedElements

## *Accuracy fields can be TIGHT, EXACT, MEDIUM, or LOOSE. Or deleted.
connection.AddressValidationOptions.StreetAccuracy = 'LOOSE'
del connection.AddressValidationOptions.DirectionalAccuracy
del connection.AddressValidationOptions.CompanyNameAccuracy

## Create some addresses to validate
address1 = connection.create_wsdl_object_of_type('AddressToValidate')
address1.CompanyName = 'International Paper'
address1.Address.StreetLines = ['155 Old Greenville Hwy', 'Suite 103']
address1.Address.City = 'Clemson'
address1.Address.StateOrProvinceCode = 'SC'
address1.Address.PostalCode = 29631
address1.Address.CountryCode = 'US'
address1.Address.Residential = False
connection.add_address(address1)

address2 = connection.create_wsdl_object_of_type('AddressToValidate')
address2.Address.StreetLines = ['320 S Cedros', '#200']
address2.Address.City = 'Solana Beach'
address2.Address.StateOrProvinceCode = 'CA'
address2.Address.PostalCode = 92075
address2.Address.CountryCode = 'US'
connection.add_address(address2)

## Send the request and print the response
connection.send_request()
print connection.response
