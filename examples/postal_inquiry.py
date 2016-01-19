#!/usr/bin/env python
"""
ValidatePostalRequest classes are used to validate and receive additional
information about postal codes.
"""
import logging
from example_config import CONFIG_OBJ
from fedex.services.country_service import FedexValidatePostalRequest

# Set this to the INFO level to see the response from Fedex printed in stdout.
logging.basicConfig(level=logging.INFO)

# We're using the FedexConfig object from example_config.py in this dir.
customer_transaction_id = "*** ValidatePostal Request v4 using Python ***"  # Optional transaction_id
inquiry = FedexValidatePostalRequest(CONFIG_OBJ, customer_transaction_id=customer_transaction_id)
inquiry.Address.PostalCode = '29631'
inquiry.Address.CountryCode = 'US'
inquiry.Address.StreetLines = ['104 Knox Road']
inquiry.Address.City = 'Clemson'
inquiry.Address.StateOrProvinceCode = 'SC'

# If you'd like to see some documentation on the country service WSDL, un-comment
# this line. (Spammy).
# print(inquiry.client)

# Un-comment this to see your complete, ready-to-send request as it stands
# before it is actually sent. This is useful for seeing what values you can
# change.
# print(inquiry.CarrierCode)
# print(inquiry.Address)
# print(inquiry.ShipDateTime)
# print(inquiry.CheckForMismatch)
# print(inquiry.RoutingCode)

# Fires off the request, sets the 'response' attribute on the object.
inquiry.send_request()

# See the response printed out.
print(inquiry.response)

# Here is the overall end result of the query.
print("HighestSeverity: {}".format(inquiry.response.HighestSeverity))
print("")

print("State/Province: {}".format(inquiry.response.PostalDetail.StateOrProvinceCode))
print("City First Initial: {}".format(inquiry.response.PostalDetail.CityFirstInitials))
print("Clean Postal Code: {}".format(inquiry.response.PostalDetail.CleanedPostalCode))

for loc_description in inquiry.response.PostalDetail.LocationDescriptions:
    print("Location ID: {}".format(loc_description.LocationId))
    print("Location No.: {}".format(loc_description.LocationNumber))
    print("Country Code: {}".format(loc_description.CountryCode))
    print("Postal Code: {}".format(loc_description.PostalCode))
    print("Service Area: {}".format(loc_description.ServiceArea))
    print("Airport ID: {}".format(loc_description.AirportId))
    print("FedEx Europe First Origin: {}".format(loc_description.FedExEuropeFirstOrigin))
