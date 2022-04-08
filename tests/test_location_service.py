"""
Test module for the Fedex LocationService WSDL.
"""

import unittest
import logging
import sys

sys.path.insert(0, '..')
from fedex.services.location_service import FedexSearchLocationRequest

# Common global config object for testing.
from tests.common import get_fedex_config

CONFIG_OBJ = get_fedex_config()

logging.getLogger('suds').setLevel(logging.ERROR)


@unittest.skipIf(not CONFIG_OBJ.account_number, "No credentials provided.")
class SearchLocationServiceTests(unittest.TestCase):
    """
    These tests verify that the shipping service WSDL is in good shape.
    """

    def test_location_phone_search(self):
        # Test location service phone query

        location_request = FedexSearchLocationRequest(CONFIG_OBJ)

        location_request.LocationsSearchCriterion = 'PHONE_NUMBER'
        location_request.PhoneNumber = '4169297819'
        location_request.MultipleMatchesAction = 'RETURN_ALL'

        location_request.Constraints.LocationTypesToInclude = ['FEDEX_AUTHORIZED_SHIP_CENTER']

        location_request.Address.PostalCode = 'M5V 1Z0'
        location_request.Address.CountryCode = 'CA'

        location_request.send_request()

        assert location_request.response

    def test_location_address_search(self):
        # Test search by address, using minimum parameters

        location_request = FedexSearchLocationRequest(CONFIG_OBJ)
        location_request.Address.PostalCode = '38119'
        location_request.Address.CountryCode = 'US'
        
    def test_location_coordinates_search(self):
        # Test search by geo coordinates
        # https://www.fedex.com/us/developer/webhelp/ws/2020/US/FedEx_WebServices_2020_Developer_Guide.htm#t=wsdvg%2FLocation_Request_Coding_Details.htm
        
        location_request = FedexSearchLocationRequest(CONFIG_OBJ)
        location_request.LocationsSearchCriterion = 'GEOGRAPHIC_COORDINATES'
        location_request.Address.CountryCode = 'US'
        location_request.GeographicCoordinates = '34.074866096127096-118.40365442768258/'

        location_request.send_request()
        assert location_request.response.HighestSeverity == 'SUCCESS'

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    unittest.main()
