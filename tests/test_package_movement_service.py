"""
Test module for the Fedex PackageMovementInformationService WSDL.
"""

import unittest
import logging
import sys
import warnings

warnings.simplefilter('always', DeprecationWarning)  # Show deprecation on this module in py2.7.

sys.path.insert(0, '../')
from fedex.services.package_movement import PostalCodeInquiryRequest

# Common global config object for testing.
from tests.common import get_fedex_config

CONFIG_OBJ = get_fedex_config()

logging.getLogger('suds').setLevel(logging.ERROR)
logging.getLogger('fedex').setLevel(logging.INFO)


@unittest.skipIf(not CONFIG_OBJ.account_number, "No credentials provided.")
class PackageMovementServiceTests(unittest.TestCase):
    """
    These tests verify that the package movement service WSDL is in good shape.
    """

    def setUp(self):
        self.config_obj = get_fedex_config()

    def tearDown(self):
        pass

    def test_postal_inquiry(self):
        inquiry = PostalCodeInquiryRequest(self.config_obj)
        inquiry.PostalCode = '29631'
        inquiry.CountryCode = 'US'

        inquiry.send_request()

        assert inquiry.response
        assert inquiry.response.HighestSeverity == 'SUCCESS'


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    unittest.main()
