"""
Test module for the Fedex CountryService WSDL.
"""

import unittest

import sys

sys.path.insert(0, '..')
from fedex.services.country_service import FedexValidatePostalRequest

# Common global config object for testing.
from common import get_test_config

CONFIG_OBJ = get_test_config()


@unittest.skipIf(not CONFIG_OBJ.account_number, "No credentials provided.")
class PackageMovementServiceTests(unittest.TestCase):
    """
    These tests verify that the package movement service WSDL is in good shape.
    """

    def test_postal_inquiry(self):
        inquiry = FedexValidatePostalRequest(CONFIG_OBJ)
        inquiry.Address.PostalCode = '29631'
        inquiry.Address.CountryCode = 'US'

        inquiry.send_request()

        assert inquiry.response
        assert inquiry.response.HighestSeverity == 'SUCCESS'


if __name__ == "__main__":
    unittest.main()
