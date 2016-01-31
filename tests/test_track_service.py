"""
Test module for the Fedex TrackService WSDL.
"""

import unittest
import logging
import sys

sys.path.insert(0, '..')
from fedex.services.track_service import FedexTrackRequest

# Common global config object for testing.
from tests.common import get_fedex_config

CONFIG_OBJ = get_fedex_config()

logging.getLogger('suds').setLevel(logging.ERROR)
logging.getLogger('fedex').setLevel(logging.INFO)


@unittest.skipIf(not CONFIG_OBJ.account_number, "No credentials provided.")
class TrackServiceTests(unittest.TestCase):
    """
    These tests verify that the shipping service WSDL is in good shape.
    """

    def test_track(self):
        # Test shipment tracking. Query for a tracking number and make sure the
        # first (and hopefully only) result matches up.

        tracking_num = '781820562774'

        track = FedexTrackRequest(CONFIG_OBJ)

        # Track by Tracking Number
        track.SelectionDetails.PackageIdentifier.Type = 'TRACKING_NUMBER_OR_DOORTAG'
        track.SelectionDetails.PackageIdentifier.Value = tracking_num

        # FedEx operating company or delete
        del track.SelectionDetails.OperatingCompany

        track.send_request()

        assert track.response

        # Uncomment below if testing in production with a valid tracking number
        # for match in track.response.CompletedTrackDetails[0].TrackDetails:
        # This should be the same tracking number on the response that we
        # asked for in the request.
        # assert match.TrackingNumber == tracking_num


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    unittest.main()
