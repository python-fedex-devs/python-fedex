#!/usr/bin/env python
"""
This example shows how to use the FedEx Location service.
The variables populated below represents minimum required values as
well as those that are optional. Read comments for details.
You will need to specify all required fields, or risk
seeing a SchemaValidationError
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

# Un-comment to specify the type of search and search criteria.
# Can be ADDRESS (default), GEOGRAPHIC_COORDINATES, or PHONE_NUMBER
# location_request.LocationsSearchCriterion = 'PHONE_NUMBER'

# Un-comment when using PHONE_NUMBER search criterion.
# location_request.PhoneNumber = '4169297819'

# Un-comment when using GEOGRAPHIC_COORDINATES search criterion.
# location_request.GeographicCoordinates = '43.6357-79.5373'

# Un-comment to specify how to handle multiple matches.
# Can be set to RETURN_ALL (default), RETURN_ERROR, or RETURN_FIRST
# location_request.MultipleMatchesAction = 'RETURN_FIRST'


# Un-comment to specify FedExLocationType constraint, see FedExLocationType definition.
# Can be set to FEDEX_AUTHORIZED_SHIP_CENTER, FEDEX_EXPRESS_STATION, FEDEX_FREIGHT_SERVICE_CENTER,
# FEDEX_GROUND_TERMINAL, FEDEX_HOME_DELIVERY_STATION, FEDEX_OFFICE, FEDEX_SELF_SERVICE_LOCATION,
# FEDEX_SHIPSITE, or FEDEX_SMART_POST_HUB
# location_request.Constraints.LocationTypesToInclude = ['FEDEX_SELF_SERVICE_LOCATION',
#                                                        'FEDEX_AUTHORIZED_SHIP_CENTER']

# Un-comment to to set a maximum radius for location query.
# This really can narrow down the location results but is not required.
location_request.Constraints.RadiusDistance.Value = 1.5
location_request.Constraints.RadiusDistance.Units = "KM"  # KM or MI

# Un-comment to specify supported redirect to hold services. Only
# supported by certain countries,from testing only US is supported.
# Can be FEDEX_EXPRESS, FEDEX_GROUND, or FEDEX_GROUND_HOME_DELIVERY
# location_request.Constraints.SupportedRedirectToHoldServices = "FEDEX_GROUND"

# Required even if using phone number search
location_request.Address.PostalCode = 'M5V 1Z0'
location_request.Address.CountryCode = 'CA'

# Un-comment to set sort criteria. By default Matching locations sorted by
# DISTANCE and LOWEST_TO_HIGHEST if no sort criteria is specified.
# Crieterion can be LATEST_EXPRESS_DROPOFF_TIME, LATEST_GROUND_DROPOFF_TIME,
# LOCATION_TYPE or DISTANCE (default)
# Order can be LOWEST_TO_HIGHEST (default) or HIGHEST_TO_LOWEST
# location_request.SortDetail.Criterion = 'LATEST_GROUND_DROPOFF_TIME'
# location_request.SortDetail.Order = 'LOWEST_TO_HIGHEST'

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
# from fedex.tools.conversion import basic_sobject_to_dict
# print(basic_sobject_to_dict(location_request.response))

# This will dump the response data dict to json.
# from fedex.tools.conversion import sobject_to_json
# print(sobject_to_json(location_request.response))

# Here is the overall end result of the query.
print("HighestSeverity: {}".format(location_request.response.HighestSeverity))
print("TotalResultsAvailable: {}".format(location_request.response.TotalResultsAvailable))
print("ResultsReturned: {}".format(location_request.response.ResultsReturned))

result = location_request.response.AddressToLocationRelationships[0]
print("MatchedAddress: {}, {} Residential: {}".format(getattr(result.MatchedAddress, 'PostalCode', ''),
                                                      getattr(result.MatchedAddress, 'CountryCode', ''),
                                                      getattr(result.MatchedAddress, 'Residential', '')))
print("MatchedAddressGeographicCoordinates: {}".format(result.MatchedAddressGeographicCoordinates.strip("/")))

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

    print("GeographicCoordinates {}".format(getattr(location_detail, 'GeographicCoordinates', '')))
    print("LocationType {}".format(getattr(location_detail, 'LocationType', '')))

    if hasattr(location_detail, 'Attributes'):
        for attribute in location_detail.Attributes:
            print("Attribute: {}".format(attribute))

    print("MapUrl {}".format(getattr(location_detail, 'MapUrl', '')))

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
