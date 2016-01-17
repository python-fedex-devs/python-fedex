#!/usr/bin/env python
"""
This example shows how to use the FedEx Location service.
The variables populated below represents the minimum required values.
You will need to fill all of these, or risk seeing a SchemaValidationError
exception thrown by suds.

"""
import logging
import sys

from example_config import CONFIG_OBJ
from fedex.services.location_service import FedexSearchLocationRequest

# Set this to the INFO level to see the response from Fedex printed in stdout.
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# This is the object that will be handling our request.
# We're using the FedexConfig object from example_config.py in this dir.
customer_transaction_id = "*** LocationService Request v3 using Python ***"  # Optional transaction_id
location_request = FedexSearchLocationRequest(CONFIG_OBJ, customer_transaction_id=customer_transaction_id)

# Specify the type of search and search criteria.
location_request.LocationsSearchCriterion = 'PHONE_NUMBER'
location_request.PhoneNumber = '4169297819'
location_request.MultipleMatchesAction = 'RETURN_ALL'

# Set constraints, see SearchLocationConstraints definition.
location_request.Constraints.LocationTypesToInclude = ['FEDEX_SELF_SERVICE_LOCATION',
                                                       'FEDEX_AUTHORIZED_SHIP_CENTER']

location_request.Address.PostalCode = '38119'
location_request.Address.CountryCode = 'US'

# If you'd like to see some documentation on the ship service WSDL, un-comment
# this line. (Spammy).
# print(rate_request.client)

# Un-comment this to see your complete, ready-to-send request as it stands
# before it is actually sent. This is useful for seeing what values you can
# change.
# print(location_request.LocationsSearchCriterion)

# Fires off the request, sets the 'response' attribute on the object.
location_request.send_request()

# This will show the reply to your request being sent. You can access the
# attributes through the response attribute on the request object. This is
# good to un-comment to see the variables returned by the FedEx reply.
# print(location_request.response)

# Here is the overall end result of the query.
print("HighestSeverity:", location_request.response.HighestSeverity)
