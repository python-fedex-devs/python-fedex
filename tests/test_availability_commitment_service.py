"""
Test module for the Fedex ShipService WSDL.
"""

import unittest
import logging
import sys

sys.path.insert(0, '..')
from fedex.services.availability_commitment_service import FedexAvailabilityCommitmentRequest

# Common global config object for testing.
from tests.common import get_fedex_config

CONFIG_OBJ = get_fedex_config()

logging.getLogger('suds').setLevel(logging.ERROR)
logging.getLogger('fedex').setLevel(logging.INFO)


@unittest.skipIf(not CONFIG_OBJ.account_number, "No credentials provided.")
class AvailabilityCommitmentServiceTests(unittest.TestCase):
    """
    These tests verify that the shipping service WSDL is in good shape.
    """

    def test_track(self):
        # Test shipment tracking. Query for a tracking number and make sure the
        # first (and hopefully only) result matches up.

        avc_request = FedexAvailabilityCommitmentRequest(CONFIG_OBJ)

        avc_request.Origin.PostalCode = 'M5V 3A4'
        avc_request.Origin.CountryCode = 'CA'

        avc_request.Destination.PostalCode = '27577'  # 29631
        avc_request.Destination.CountryCode = 'US'

        avc_request.send_request()
        assert avc_request.response


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    unittest.main()
