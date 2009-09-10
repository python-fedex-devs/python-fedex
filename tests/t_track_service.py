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
        tracking_num = '1777768882'
        tracking_num = '799428562846'
        tracking_num = '111111111111'
        tracking_num = '012301230123'

        track_request = FedexTrackRequest(CONFIG_OBJ, tracking_num)
        track_request.send_request()
        
        print track_request.response
            
        for match in track_request.response.TrackDetails:
            # This should be the same tracking number on the response that we
            # asked for in the request.
            self.assertEqual(match.TrackingNumber, tracking_num)