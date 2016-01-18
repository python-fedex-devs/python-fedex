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
from fedex.tools.conversion import sobject_to_dict

# Un-comment to see the response from Fedex printed in stdout.
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
# For LocationTypesToInclude, see FedExLocationType definition.
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

# This will convert the response to a python dict object. To
# make it easier to work with.
# from fedex.tools.response_tools import basic_sobject_to_dict
# print(basic_sobject_to_dict(location_request.response))

# This will dump the response data dict to json.
# from fedex.tools.response_tools import sobject_to_json
# print(sobject_to_json(location_request.response))

# Here is the overall end result of the query.
print("HighestSeverity: {}".format(location_request.response.HighestSeverity))
print("TotalResultsAvailable: {}".format(location_request.response.TotalResultsAvailable))
print("ResultsReturned: {}".format(location_request.response.ResultsReturned))

result = location_request.response.AddressToLocationRelationships[0]
print("MatchedAddress: {}, {} Residential: {}".format(result.MatchedAddress.PostalCode,
                                                      result.MatchedAddress.CountryCode,
                                                      result.MatchedAddress.Residential))
print("MatchedAddressGeographicCoordinates: {}".format(result.MatchedAddressGeographicCoordinates.strip("/")))

# Locations sorted by closest found to furthest.
locations = result.DistanceAndLocationDetails
for location in locations:
    print("Distance: {}{}".format(location.Distance.Value, location.Distance.Units))

    location_detail = location.LocationDetail
    print("LocationID: {}".format(location_detail.LocationId))
    print("StoreNumber: {}".format(location_detail.StoreNumber))

    if hasattr(location_detail, 'LocationContactAndAddress'):
        contact_and_address = location_detail.LocationContactAndAddress
        contact_and_address = sobject_to_dict(contact_and_address)
        print("LocationContactAndAddress Dict: {}".format(contact_and_address))

    print("GeographicCoordinates {}".format(getattr(location_detail, 'GeographicCoordinates')))
    print("LocationType {}".format(getattr(location_detail, 'LocationType')))

    if hasattr(location_detail, 'Attributes'):
        for attribute in location_detail.Attributes:
            print("Attribute: {}".format(attribute))

    print("MapUrl {}".format(getattr(location_detail, 'MapUrl')))

    if hasattr(location_detail, 'NormalHours'):
        for open_time in location_detail.NormalHours:
            print("NormalHours Dict: {}".format(sobject_to_dict(open_time)))

    if hasattr(location_detail, 'HoursForEffectiveDate'):
        for effective_open_time in location_detail.HoursForEffectiveDate:
            print("HoursForEffectiveDate Dict: {}".format(sobject_to_dict(effective_open_time)))

    if hasattr(location_detail, 'CarrierDetails'):
        for carrier_detail in location_detail.CarrierDetails:
            print("CarrierDetails Dict: {}".format(sobject_to_dict(carrier_detail)))

    print("")
