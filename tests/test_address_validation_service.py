"""
Test module for the Fedex AddressValidationService WSDL.
"""

import unittest
import logging
import sys

sys.path.insert(0, '..')
from fedex.services.address_validation_service import FedexAddressValidationRequest

# Common global config object for testing.
from tests.common import get_fedex_config

CONFIG_OBJ = get_fedex_config()

logging.getLogger('suds').setLevel(logging.ERROR)
logging.getLogger('fedex').setLevel(logging.INFO)


@unittest.skipIf(not CONFIG_OBJ.account_number, "No credentials provided.")
class AddressValidationServiceTests(unittest.TestCase):
    """
    These tests verify that the address validation service WSDL is in good shape.
    """

    def test_avs(self):
        avs_request = FedexAddressValidationRequest(CONFIG_OBJ)

        address1 = avs_request.create_wsdl_object_of_type('AddressToValidate')
        address1.Address.StreetLines = ['155 Old Greenville Hwy', 'Suite 103']
        address1.Address.City = 'Clemson'
        address1.Address.StateOrProvinceCode = 'SC'
        address1.Address.PostalCode = 29631
        address1.Address.CountryCode = 'US'
        address1.Address.Residential = False
        avs_request.add_address(address1)

        avs_request.send_request()

        assert avs_request.response


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    unittest.main()
