"""
Test module for the Fedex ShipService WSDL.
"""

import unittest
import logging
import sys

sys.path.insert(0, '..')
from fedex.services.ship_service import FedexProcessShipmentRequest
from fedex.services.ship_service import FedexDeleteShipmentRequest

# Common global config object for testing.
from tests.common import get_fedex_config

CONFIG_OBJ = get_fedex_config()

logging.getLogger('suds').setLevel(logging.ERROR)
logging.getLogger('fedex').setLevel(logging.INFO)


@unittest.skipIf(not CONFIG_OBJ.account_number, "No credentials provided.")
class ShipServiceTests(unittest.TestCase):
    """
    These tests verify that the ship service WSDL is in good shape.
    """

    def test_create_delete_shipment(self):
        shipment = FedexProcessShipmentRequest(CONFIG_OBJ)

        shipment.RequestedShipment.DropoffType = 'REGULAR_PICKUP'
        shipment.RequestedShipment.ServiceType = 'FEDEX_GROUND'
        shipment.RequestedShipment.PackagingType = 'YOUR_PACKAGING'

        shipment.RequestedShipment.Shipper.Contact.PersonName = 'Sender Name'
        shipment.RequestedShipment.Shipper.Contact.PhoneNumber = '9012638716'

        shipment.RequestedShipment.Shipper.Address.StreetLines = ['Address Line 1']
        shipment.RequestedShipment.Shipper.Address.City = 'Herndon'
        shipment.RequestedShipment.Shipper.Address.StateOrProvinceCode = 'VA'
        shipment.RequestedShipment.Shipper.Address.PostalCode = '20171'
        shipment.RequestedShipment.Shipper.Address.CountryCode = 'US'

        shipment.RequestedShipment.Recipient.Contact.PersonName = 'Recipient Name'
        shipment.RequestedShipment.Recipient.Contact.PhoneNumber = '9012637906'

        shipment.RequestedShipment.Recipient.Address.StreetLines = ['Address Line 1']
        shipment.RequestedShipment.Recipient.Address.City = 'Herndon'
        shipment.RequestedShipment.Recipient.Address.StateOrProvinceCode = 'VA'
        shipment.RequestedShipment.Recipient.Address.PostalCode = '20171'
        shipment.RequestedShipment.Recipient.Address.CountryCode = 'US'
        shipment.RequestedShipment.EdtRequestType = 'NONE'

        shipment.RequestedShipment.ShippingChargesPayment.Payor.ResponsibleParty.AccountNumber \
            = CONFIG_OBJ.account_number

        shipment.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'

        shipment.RequestedShipment.LabelSpecification.LabelFormatType = 'COMMON2D'
        shipment.RequestedShipment.LabelSpecification.ImageType = 'PNG'
        shipment.RequestedShipment.LabelSpecification.LabelStockType = 'PAPER_7X4.75'
        shipment.RequestedShipment.LabelSpecification.LabelPrintingOrientation = 'BOTTOM_EDGE_OF_TEXT_FIRST'

        # Use order if setting multiple labels or delete
        del shipment.RequestedShipment.LabelSpecification.LabelOrder

        package1_weight = shipment.create_wsdl_object_of_type('Weight')
        package1_weight.Value = 2.0
        package1_weight.Units = "LB"
        package1 = shipment.create_wsdl_object_of_type('RequestedPackageLineItem')
        package1.PhysicalPackaging = 'ENVELOPE'
        package1.Weight = package1_weight
        shipment.add_package(package1)

        shipment.send_validation_request()
        shipment.send_request()

        assert shipment.response
        assert shipment.response.HighestSeverity in ['SUCCESS', 'WARNING']
        track_id = shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].TrackingIds[0].TrackingNumber
        assert track_id

        del_shipment = FedexDeleteShipmentRequest(CONFIG_OBJ)
        del_shipment.DeletionControlType = "DELETE_ALL_PACKAGES"
        del_shipment.TrackingId.TrackingNumber = track_id
        del_shipment.TrackingId.TrackingIdType = 'EXPRESS'

        del_shipment.send_request()

        assert del_shipment.response


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    unittest.main()
