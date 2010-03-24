#!/usr/bin/env python
"""
This module prints a label used to certify International Priority shipments.
"""
import logging
from cert_config import CONFIG_OBJ, SHIPPER_CONTACT_INFO, SHIPPER_ADDRESS, LABEL_SPECIFICATION
from cert_config import transfer_config_dict
from cert_config import LabelPrinterClass
from fedex.services.ship_service import FedexProcessShipmentRequest
from fedex.printers.unix import DirectDevicePrinter

logging.basicConfig(level=logging.INFO)

shipment = FedexProcessShipmentRequest(CONFIG_OBJ)
shipment.RequestedShipment.DropoffType = 'REGULAR_PICKUP'
shipment.RequestedShipment.ServiceType = 'INTERNATIONAL_PRIORITY'
shipment.RequestedShipment.PackagingType = 'YOUR_PACKAGING'
shipment.RequestedShipment.PackageDetail = 'INDIVIDUAL_PACKAGES'

# Shipper contact info.
transfer_config_dict(shipment.RequestedShipment.Shipper.Contact, 
                     SHIPPER_CONTACT_INFO)

# Shipper address.
transfer_config_dict(shipment.RequestedShipment.Shipper.Address, 
                     SHIPPER_ADDRESS)

# Recipient contact info.
shipment.RequestedShipment.Recipient.Contact.PersonName = 'Some Guy'
#shipment.RequestedShipment.Recipient.Contact.CompanyName = 'Recipient Company'
shipment.RequestedShipment.Recipient.Contact.PhoneNumber = '8646336010'

# Recipient address
shipment.RequestedShipment.Recipient.Address.StreetLines = ['77 Foo Young']
shipment.RequestedShipment.Recipient.Address.City = 'Taipei'
shipment.RequestedShipment.Recipient.Address.PostalCode = '115'
shipment.RequestedShipment.Recipient.Address.CountryCode = 'TW'

shipment.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER' 

# Label config.
transfer_config_dict(shipment.RequestedShipment.LabelSpecification, 
                     LABEL_SPECIFICATION)

package1_weight = shipment.create_wsdl_object_of_type('Weight')
package1_weight.Value = 10.0
package1_weight.Units = "LB"

package1 = shipment.create_wsdl_object_of_type('RequestedPackageLineItem')
package1.Weight = package1_weight

shipment.add_package(package1)

shipment.RequestedShipment.InternationalDetail.DocumentContent = "NON_DOCUMENTS"
shipment.RequestedShipment.InternationalDetail.CustomsValue.Currency = "USD"
shipment.RequestedShipment.InternationalDetail.CustomsValue.Amount = "10.00"

commod = shipment.create_wsdl_object_of_type('Commodity')
commod.NumberOfPieces = "1"
commod.Description = "Technical Book"
commod.CountryOfManufacture = "US"
commod.Weight.Units = "LB"
commod.Weight.Value = "5.0"
commod.Quantity = "1"
commod.QuantityUnits = "EA"
commod.UnitPrice.Currency = "USD"
commod.UnitPrice.Amount = "10.00"
shipment.RequestedShipment.InternationalDetail.Commodities.append(commod)

shipment.RequestedShipment.InternationalDetail.DutiesPayment.PaymentType = "SENDER"
shipment.RequestedShipment.InternationalDetail.DutiesPayment.Payor.AccountNumber = CONFIG_OBJ.account_number
shipment.RequestedShipment.InternationalDetail.DutiesPayment.Payor.CountryCode = "US"

shipment.send_request()

print shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].TrackingIds

device = LabelPrinterClass(shipment)
device.print_label()
