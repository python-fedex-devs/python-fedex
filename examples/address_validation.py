#!/usr/bin/env python
"""
This example shows how to validate addresses. Note that the validation
class can handle up to 100 addresses for validation.
"""
import logging
import sys

from example_config import CONFIG_OBJ
from fedex.services.address_validation_service import FedexAddressValidationRequest

# NOTE: TO USE ADDRESS VALIDATION SERVICES, YOU NEED TO REQUEST FEDEX TO ENABLE THIS SERVICE FOR YOUR ACCOUNT.
# BY DEFAULT, THE SERVICE IS DISABLED AND YOU WILL RECEIVE AUTHENTICATION FAILED, 1000 RESPONSE.

# Un-comment to see the response from Fedex printed in stdout.
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# This is the object that will be handling our avs request.
# We're using the FedexConfig object from example_config.py in this dir.
customer_transaction_id = "*** AddressValidation Request v4 using Python ***"  # Optional transaction_id
# Optional locale & language client data
client_language_code = 'EN'
client_locale_code = 'US'
avs_request = FedexAddressValidationRequest(CONFIG_OBJ, customer_transaction_id=customer_transaction_id,
                                            client_locale_code=client_locale_code,
                                            client_language_code=client_language_code)

# Create some addresses to validate
address1 = avs_request.create_wsdl_object_of_type('AddressToValidate')
address1.ClientReferenceId = "Your ID for the Recipient"
address1.Address.StreetLines = ['155 Old Greenville Hwy', 'Suite 103']
address1.Address.City = 'Clemson'
address1.Address.StateOrProvinceCode = 'SC'
address1.Address.PostalCode = 29631
address1.Address.CountryCode = 'US'
address1.Address.Residential = False

address1.Contact.PersonName = 'Recipient Name'
address1.Contact.CompanyName = 'Company Name'
address1.Contact.PhoneNumber = '999-123-5343'
address1.Contact.EMailAddress = 'example_recipient@email.com'
avs_request.add_address(address1)

address2 = avs_request.create_wsdl_object_of_type('AddressToValidate')
address2.Address.StreetLines = ['320 S Cedros', '#200']
address2.Address.City = 'Solana Beach'
address2.Address.StateOrProvinceCode = 'CA'
address2.Address.PostalCode = 92075
address2.Address.CountryCode = 'US'
avs_request.add_address(address2)

# If you'd like to see some documentation on the ship service WSDL, un-comment
# this line. (Spammy).
# print(avs_request.client)

# Un-comment this to see your complete, ready-to-send request as it stands
# before it is actually sent. This is useful for seeing what values you can
# change.
# print(avs_request.AddressesToValidate)
# print(avs_request.ClientDetail)
# print(avs_request.TransactionDetail)

# Fires off the request, sets the 'response' attribute on the object.
avs_request.send_request()

# good to un-comment to see the variables returned by the Fedex reply.
# print(avs_request.response)

# This will convert the response to a python dict object. To
# make it easier to work with.
# from fedex.tools.conversion import basic_sobject_to_dict
# print(basic_sobject_to_dict(avs_request.response))

# This will dump the response data dict to json.
# from fedex.tools.conversion import sobject_to_json
# print(sobject_to_json(avs_request.response))

# Overall end result of the query
for i in range(len(avs_request.response.AddressResults)):

    print("Details for Address {}".format(i + 1))
    print("The validated street is: {}"
          "".format(avs_request.response.AddressResults[i].EffectiveAddress.StreetLines))
    print("The validated city is: {}"
          "".format(avs_request.response.AddressResults[i].EffectiveAddress.City))
    print("The validated state code is: {}"
          "".format(avs_request.response.AddressResults[i].EffectiveAddress.StateOrProvinceCode))
    print("The validated postal code is: {}"
          "".format(avs_request.response.AddressResults[i].EffectiveAddress.PostalCode))
    print("The validated country code is: {}"
          "".format(avs_request.response.AddressResults[i].EffectiveAddress.CountryCode))

    # Can be used to determine the address classification to figure out if Residential fee should apply.
    # MIXED, RESIDENTIAL, UNKNOWN, BUSINESS
    print("The validated address is residential: {}"
          "".format(avs_request.response.AddressResults[i].Classification != 'BUSINESS'))

    # Getting the optional attributes if available
    for j in range(len(avs_request.response.AddressResults[i].Attributes)):
        cur_attribute = avs_request.response.AddressResults[i].Attributes[j]
        if cur_attribute.Name == "CountrySupported":
            print("Supported Country: {}".format(cur_attribute.Value == 'true'))
        if cur_attribute.Name == "SuiteRequiredButMissing":
            print("Missing Suite: {}".format(cur_attribute.Value == 'true'))
        if cur_attribute.Name == "InvalidSuiteNumber":
            print("Invalid Suite: {}".format(cur_attribute.Value == 'true'))
        if cur_attribute.Name == "MultipleMatches":
            print("Multiple Matches: {}".format(cur_attribute.Value == 'true'))
        if cur_attribute.Name == "POBox":
            print("Is POBox: {}".format(cur_attribute.Value == 'true'))
    print("")
