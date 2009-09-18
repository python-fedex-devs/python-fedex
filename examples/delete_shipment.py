#!/usr/bin/env python
"""
This example shows how to delete existing shipments.
"""
import logging
from example_config import CONFIG_OBJ
from fedex.services.ship_service import FedexDeleteShipmentRequest

# Set this to the INFO level to see the response from Fedex printed in stdout.
logging.basicConfig(level=logging.INFO)

# This is the object that will be handling our tracking request.
# We're using the FedexConfig object from example_config.py in this dir.
del_request = FedexDeleteShipmentRequest(CONFIG_OBJ)

# Either delete all packages in a shipment, or delete an individual package.
# DELETE_ALL_PACKAGES, DELETE_ONE_PACKAGE
del_request.DeletionControlType = "DELETE_ALL_PACKAGES"

# The tracking number of the shipment to delete.
del_request.TrackingId.TrackingNumber = '794798682968'

# What kind of shipment the tracking number used.
# EXPRESS, GROUND, or USPS
del_request.TrackingId.TrackingIdType = 'EXPRESS'

# Fires off the request, sets the 'response' attribute on the object.
del_request.send_request()

# See the response printed out.
print del_request.response
