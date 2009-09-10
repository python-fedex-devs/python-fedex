"""
Test module for the Fedex ShipService WSDL.
"""
import unittest
from fedex.services.track_service import FedexTrackRequest
import common

# Common global config object for testing.
CONFIG_OBJ = common.get_test_config()

class TrackServiceTests(unittest.TestCase):
    """
    These tests verify that the shipping service WSDL is in good shape.
    """
    def test_track(self):
        """
        Test shipment tracking. Query for a tracking number and make sure the
        first (and hopefully only) result matches up.
        """
        track_request = FedexTrackRequest(CONFIG_OBJ, '1777768882')
        track_request.send_request()
            
        for match in track_request.response.TrackDetails:
            # This should be the same tracking number on the response that we
            # asked for in the request.
            self.assertEqual(match.TrackingNumber, '1777768882')