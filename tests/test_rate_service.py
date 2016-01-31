"""
Test module for the Fedex RateService WSDL.
"""

import unittest
import logging
import sys

sys.path.insert(0, '..')
from fedex.services.rate_service import FedexRateServiceRequest

# Common global config object for testing.
from tests.common import get_fedex_config

CONFIG_OBJ = get_fedex_config()

logging.getLogger('suds').setLevel(logging.ERROR)
logging.getLogger('fedex').setLevel(logging.INFO)


@unittest.skipIf(not CONFIG_OBJ.account_number, "No credentials provided.")
class RateServiceTests(unittest.TestCase):
    """
    These tests verify that the rate service WSDL is in good shape.
    """

    def test_rate(self):
        rate = FedexRateServiceRequest(CONFIG_OBJ)

        rate.RequestedShipment.DropoffType = 'REGULAR_PICKUP'
        rate.RequestedShipment.ServiceType = 'FEDEX_GROUND'
        rate.RequestedShipment.PackagingType = 'YOUR_PACKAGING'

        rate.RequestedShipment.Shipper.Address.StateOrProvinceCode = 'SC'
        rate.RequestedShipment.Shipper.Address.PostalCode = '29631'
        rate.RequestedShipment.Shipper.Address.CountryCode = 'US'

        rate.RequestedShipment.Recipient.Address.StateOrProvinceCode = 'NC'
        rate.RequestedShipment.Recipient.Address.PostalCode = '27577'
        rate.RequestedShipment.Recipient.Address.CountryCode = 'US'

        rate.RequestedShipment.EdtRequestType = 'NONE'
        rate.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'

        package1_weight = rate.create_wsdl_object_of_type('Weight')
        package1_weight.Value = 1.0
        package1_weight.Units = "LB"
        package1 = rate.create_wsdl_object_of_type('RequestedPackageLineItem')
        package1.Weight = package1_weight
        package1.PhysicalPackaging = 'BOX'
        package1.GroupPackageCount = 1
        rate.add_package(package1)

        rate.send_request()

        assert rate.response.HighestSeverity == 'SUCCESS', rate.response.Notifications[0].Message


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    unittest.main()
