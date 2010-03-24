#!/usr/bin/env python
"""
This module prints a label used to certify International Priority shipments.
"""
import logging
from cert_config import CONFIG_OBJ
from fedex.services.ship_service import FedexProcessShipmentRequest
from fedex.printers.unix import DirectDevicePrinter

logging.basicConfig(level=logging.INFO)

shipment = FedexProcessShipmentRequest(CONFIG_OBJ)
shipment.RequestedShipment.DropoffType = 'REGULAR_PICKUP'
shipment.RequestedShipment.ServiceType = 'INTERNATIONAL_PRIORITY'
shipment.RequestedShipment.PackagingType = 'YOUR_PACKAGING'
shipment.RequestedShipment.PackageDetail = 'INDIVIDUAL_PACKAGES'

# Shipper contact info.
shipment.RequestedShipment.Shipper.Contact.PersonName = 'Gregory Taylor'
shipment.RequestedShipment.Shipper.Contact.CompanyName = 'International Paper'
shipment.RequestedShipment.Shipper.Contact.PhoneNumber = '8646336010'

# Shipper address.
shipment.RequestedShipment.Shipper.Address.StreetLines = ['155 Old Greenville Hwy',
                                                          'Suite 103']
shipment.RequestedShipment.Shipper.Address.City = 'Clemson'
shipment.RequestedShipment.Shipper.Address.StateOrProvinceCode = 'SC'
shipment.RequestedShipment.Shipper.Address.PostalCode = '29631'
shipment.RequestedShipment.Shipper.Address.CountryCode = 'US'
shipment.RequestedShipment.Shipper.Address.Residential = False

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

# Specifies the label type to be returned.
# LABEL_DATA_ONLY or COMMON2D
shipment.RequestedShipment.LabelSpecification.LabelFormatType = 'COMMON2D'

# Specifies which format the label file will be sent to you in.
# DPL, EPL2, PDF, PNG, ZPLII
shipment.RequestedShipment.LabelSpecification.ImageType = 'EPL2'

# To use doctab stocks, you must change ImageType above to one of the
# label printer formats (ZPLII, EPL2, DPL).
# See documentation for paper types, there quite a few.
shipment.RequestedShipment.LabelSpecification.LabelStockType = 'STOCK_4X6.75_LEADING_DOC_TAB'

# This indicates if the top or bottom of the label comes out of the 
# printer first.
# BOTTOM_EDGE_OF_TEXT_FIRST or TOP_EDGE_OF_TEXT_FIRST
shipment.RequestedShipment.LabelSpecification.LabelPrintingOrientation = 'BOTTOM_EDGE_OF_TEXT_FIRST'

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

device = DirectDevicePrinter(shipment)
device.print_label()
