import logging
import sys

from example_config import CONFIG_OBJ
from fedex.services.availability_commitment_service import FedexAvailabilityCommitmentRequest
from fedex.tools.conversion import sobject_to_dict

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

avc_request = FedexAvailabilityCommitmentRequest(CONFIG_OBJ)

# .StateOrProvinceCode available as well
avc_request.Origin.PostalCode = '60634'
avc_request.Origin.CountryCode = 'US'
avc_request.Destination.PostalCode = '19106'
avc_request.Destination.CountryCode = 'US'
avc_request.Service = 'FEDEX_GROUND'

avc_request.send_request()
response_dict = sobject_to_dict(avc_request.response)

# output display formatting
origin_str = '%s, %s' % (
    avc_request.Origin.PostalCode,
    avc_request.Origin.CountryCode)
destination_str = '%s, %s' % (
    avc_request.Destination.PostalCode,
    avc_request.Destination.CountryCode)

logging.info('origin: %s' % origin_str)
logging.info('destination: %s' % destination_str)
for option in response_dict['Options']:
    if option['Service'] == 'FEDEX_GROUND':
        logging.info('TransitTime: %s' % option['TransitTime'])
    else:
        logging.warning('No Fedex Ground Service found.')
