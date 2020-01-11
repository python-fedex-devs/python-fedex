#!/usr/bin/env python
"""
This example shows how to track shipments.
"""
import logging
import sys

from example_config import CONFIG_OBJ
from fedex.services.track_service import FedexTrackRequest

# Un-comment to see the response from Fedex printed in stdout.
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# NOTE: TRACKING IS VERY ERRATIC ON THE TEST SERVERS. YOU MAY NEED TO USE
# PRODUCTION KEYS/PASSWORDS/ACCOUNT #. THE TEST SERVERS OFTEN RETURN A NOT FOUND ERROR.
# WHEN TESTING IN PRODUCTION, GIVE SOME TIME FOR THE TRACKING TO PROPAGATE.


# We're using the FedexConfig object from example_config.py in this dir.
customer_transaction_id = "*** TrackService Request v10 using Python ***"  # Optional transaction_id
track = FedexTrackRequest(CONFIG_OBJ, customer_transaction_id=customer_transaction_id)

# Track by Tracking Number
track.SelectionDetails.PackageIdentifier.Type = 'TRACKING_NUMBER_OR_DOORTAG'
track.SelectionDetails.PackageIdentifier.Value = '781820562774'

# FedEx operating company or delete
del track.SelectionDetails.OperatingCompany

# Can optionally set the TrackingNumberUniqueIdentifier
# del track.SelectionDetails.TrackingNumberUniqueIdentifier

# If you'd like to see some documentation on the ship service WSDL, un-comment
# this line. (Spammy).
# print(track.client)

# Un-comment this to see your complete, ready-to-send request as it stands
# before it is actually sent. This is useful for seeing what values you can
# change.
# print(track.SelectionDetails)
# print(track.ClientDetail)
# print(track.TransactionDetail)


# Fires off the request, sets the 'response' attribute on the object.
track.send_request()

# This will show the reply to your track request being sent. You can access the
# attributes through the response attribute on the request object. This is
# good to un-comment to see the variables returned by the FedEx reply.
print(track.response)

# This will convert the response to a python dict object. To
# make it easier to work with.
# from fedex.tools.conversion import basic_sobject_to_dict
# print(basic_sobject_to_dict(track.response))

# This will dump the response data dict to json.
# from fedex.tools.conversion import sobject_to_json
# print(sobject_to_json(track.response))

# Look through the matches (there should only be one for a tracking number
# query), and show a few details about each shipment.
print("== Results ==")
for match in track.response.CompletedTrackDetails[0].TrackDetails:
    print("Tracking #: {}".format(match.TrackingNumber))
    if hasattr(match, 'TrackingNumberUniqueIdentifier'):
        print("Tracking # UniqueID: {}".format(match.TrackingNumberUniqueIdentifier))
    if hasattr(match, 'StatusDetail'):
        if hasattr(getattr(match, 'StatusDetail'), 'Description'):
            print("Status Description: {}".format(match.StatusDetail.Description))
        if hasattr(getattr(match, 'StatusDetail'), 'AncillaryDetails'):
            print("Status AncillaryDetails Reason: {}".format(match.StatusDetail.AncillaryDetails[-1].Reason))
            print("Status AncillaryDetails Description: {}"
                  "".format(match.StatusDetail.AncillaryDetails[-1].ReasonDescription))
    if hasattr(match, 'ServiceCommitMessage'):
        print("Commit Message: {}".format(match.ServiceCommitMessage))
    if hasattr(match, 'Notification'):
        print("Notification Severity: {}".format(match.Notification.Severity))
        print("Notification Code: {}".format(match.Notification.Code))
        print("Notification Message: {}".format(match.Notification.Message))
    print("")

    event_details = []
    if hasattr(match, 'Events'):
        for j in range(len(match.Events)):
            event_match = match.Events[j]
            event_details.append({'created': event_match.Timestamp, 'type': event_match.EventType,
                                  'description': event_match.EventDescription})

            if hasattr(event_match, 'StatusExceptionDescription'):
                event_details[j]['exception_description'] = event_match.StatusExceptionDescription

            print("Event {}: {}".format(j + 1, event_details[j]))
