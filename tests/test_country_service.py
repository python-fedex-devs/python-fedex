"""
Test module for the Fedex CountryService WSDL.
"""

import unittest
import logging
import sys

sys.path.insert(0, '..')
from fedex.services.country_service import FedexValidatePostalRequest

# Common global config object for testing.
from tests.common import get_fedex_config

CONFIG_OBJ = get_fedex_config()

logging.getLogger('suds').setLevel(logging.ERROR)
logging.getLogger('fedex').setLevel(logging.INFO)


@unittest.skipIf(not CONFIG_OBJ.account_number, "No credentials provided.")
class PackageMovementServiceTests(unittest.TestCase):
    """
    These tests verify that the country service WSDL is in good shape.
    """

    def test_postal_inquiry(self):
        inquiry = FedexValidatePostalRequest(CONFIG_OBJ)
        inquiry.Address.PostalCode = '29631'
        inquiry.Address.CountryCode = 'US'

        inquiry.send_request()

        assert inquiry.response
        assert inquiry.response.HighestSeverity == 'SUCCESS'


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    unittest.main()
