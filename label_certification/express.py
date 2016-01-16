#!/usr/bin/env python
"""
This module prints three FedEx Express shipping labels for the label
certification process. See your FedEx Label Developer Tool Kit documentation
for more details.
"""

import logging
from cert_config import CONFIG_OBJ, SHIPPER_CONTACT_INFO, SHIPPER_ADDRESS, LABEL_SPECIFICATION
from cert_config import transfer_config_dict
from cert_config import LabelPrinterClass
from fedex.services.ship_service import FedexProcessShipmentRequest

logging.basicConfig(level=logging.INFO)

shipment = FedexProcessShipmentRequest(CONFIG_OBJ)
shipment.RequestedShipment.DropoffType = 'REGULAR_PICKUP'
shipment.RequestedShipment.ServiceType = 'PRIORITY_OVERNIGHT'
shipment.RequestedShipment.PackagingType = 'YOUR_PACKAGING'

# Shipper contact info.
transfer_config_dict(shipment.RequestedShipment.Shipper.Contact,
                     SHIPPER_CONTACT_INFO)

# Shipper address.
transfer_config_dict(shipment.RequestedShipment.Shipper.Address,
                     SHIPPER_ADDRESS)

# Recipient contact info.
shipment.RequestedShipment.Recipient.Contact.PersonName = 'Recipient Name'
shipment.RequestedShipment.Recipient.Contact.CompanyName = 'Recipient Company'
shipment.RequestedShipment.Recipient.Contact.PhoneNumber = '9012637906'

# Recipient address
shipment.RequestedShipment.Recipient.Address.StreetLines = ['Address Line 1']
shipment.RequestedShipment.Recipient.Address.City = 'Herndon'
shipment.RequestedShipment.Recipient.Address.StateOrProvinceCode = 'VA'
shipment.RequestedShipment.Recipient.Address.PostalCode = '20171'
shipment.RequestedShipment.Recipient.Address.CountryCode = 'US'

shipment.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'

# Senders account information
shipment.RequestedShipment.ShippingChargesPayment.Payor.ResponsibleParty.AccountNumber = CONFIG_OBJ.account_number

# Label config.
transfer_config_dict(shipment.RequestedShipment.LabelSpecification,
                     LABEL_SPECIFICATION)

package1_weight = shipment.create_wsdl_object_of_type('Weight')
package1_weight.Value = 1.0
package1_weight.Units = "LB"
package1 = shipment.create_wsdl_object_of_type('RequestedPackageLineItem')
package1.Weight = package1_weight
shipment.add_package(package1)

if __name__ == "__main__":
    shipment.send_request()
    device = LabelPrinterClass(shipment)
    device.print_label()

    shipment.RequestedShipment.Recipient.Address.StreetLines = ['456 Peach St']
    shipment.RequestedShipment.Recipient.Address.City = 'Atlanta'
    shipment.RequestedShipment.Recipient.Address.StateOrProvinceCode = 'GA'
    shipment.RequestedShipment.Recipient.Address.PostalCode = '30303'
    shipment.RequestedShipment.Recipient.Address.CountryCode = 'US'

    shipment.send_request()
    device = LabelPrinterClass(shipment)
    device.print_label()

    shipment.RequestedShipment.Recipient.Address.StreetLines = ['987 Main St']
    shipment.RequestedShipment.Recipient.Address.City = 'Boston'
    shipment.RequestedShipment.Recipient.Address.StateOrProvinceCode = 'MA'
    shipment.RequestedShipment.Recipient.Address.PostalCode = '02115'
    shipment.RequestedShipment.Recipient.Address.CountryCode = 'US'

    shipment.send_request()
    device = LabelPrinterClass(shipment)
    device.print_label()
