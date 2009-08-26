import logging
from fedex.services.ship_service import FedexTrackRequest
from fedex.config import FedexConfig

# Set this to the INFO level to see the response from Fedex printed in stdout.
logging.basicConfig(level=logging.INFO)

# FedexConfig objects should generally only be instantiated once and re-used
# amongst different queries. They hold static data like account number.
config_obj = FedexConfig(key='ZyNQQFdcxUATOx9L',
                         password='GtngmKzs4Dk4RYmrlAjrLykwi',
                         account_number='510087780',
                         meter_number='118501898')

# This is the object that will be handling our tracking request.
track = FedexTrackRequest(config_obj, '1777768882')
# Fires off the request, sets the 'response' attribute on the object.
track.send_request()

# Look through the matches (there should only be one for a tracking number
# query), and show a few details about each shipment.
for match in track.response.TrackDetails:
    print "TRACKING #:", match.TrackingNumber
    print "STATUS:", match.StatusDescription