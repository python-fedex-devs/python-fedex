#!/usr/bin/env python
"""
This example shows how to create shipments. The variables populated below
represents the minimum required values. You will need to fill all of these, or
risk seeing a SchemaValidationError exception thrown.

Near the bottom of the module, you'll see some different ways to handle the
label data that is returned with the reply.
"""
import logging
import binascii
from example_config import CONFIG_OBJ
from fedex.services.ship_service import FedexProcessShipmentRequest

# Set this to the INFO level to see the response from Fedex printed in stdout.
#logging.basicConfig(filename="suds.log", level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
# This is the object that will be handling our tracking request.
# We're using the FedexConfig object from example_config.py in this dir.
shipment = FedexProcessShipmentRequest(CONFIG_OBJ)
shipment.RequestedShipment.DropoffType = 'REGULAR_PICKUP'
shipment.RequestedShipment.ServiceType = 'FEDEX_FREIGHT_ECONOMY'
shipment.RequestedShipment.PackagingType = 'YOUR_PACKAGING'

shipment.RequestedShipment.FreightShipmentDetail.FedExFreightAccountNumber = CONFIG_OBJ.freight_account_number

# Shipper contact info.
shipment.RequestedShipment.Shipper.Contact.PersonName = 'Sender Name'
shipment.RequestedShipment.Shipper.Contact.CompanyName = 'Some Company'
shipment.RequestedShipment.Shipper.Contact.PhoneNumber = '9012638716'

# Shipper address.
shipment.RequestedShipment.Shipper.Address.StreetLines = ['1202 Chalet Ln']
shipment.RequestedShipment.Shipper.Address.City = 'Harrison'
shipment.RequestedShipment.Shipper.Address.StateOrProvinceCode = 'AR'
shipment.RequestedShipment.Shipper.Address.PostalCode = '72601'
shipment.RequestedShipment.Shipper.Address.CountryCode = 'US'
shipment.RequestedShipment.Shipper.Address.Residential = True

# Recipient contact info.
shipment.RequestedShipment.Recipient.Contact.PersonName = 'Recipient Name'
shipment.RequestedShipment.Recipient.Contact.CompanyName = 'Recipient Company'
shipment.RequestedShipment.Recipient.Contact.PhoneNumber = '9012637906'

# Recipient address
shipment.RequestedShipment.Recipient.Address.StreetLines = ['2000 Freight LTL Testing']
shipment.RequestedShipment.Recipient.Address.City = 'Harrison'
shipment.RequestedShipment.Recipient.Address.StateOrProvinceCode = 'AR'
shipment.RequestedShipment.Recipient.Address.PostalCode = '72601'
shipment.RequestedShipment.Recipient.Address.CountryCode = 'US'

# This is needed to ensure an accurate rate quote with the response.
shipment.RequestedShipment.Recipient.Address.Residential = False
shipment.RequestedShipment.FreightShipmentDetail.TotalHandlingUnits = 1  
shipment.RequestedShipment.ShippingChargesPayment.Payor.ResponsibleParty.AccountNumber = CONFIG_OBJ.freight_account_number

shipment.RequestedShipment.FreightShipmentDetail.FedExFreightBillingContactAndAddress.Contact.PersonName = 'Sender Name'
shipment.RequestedShipment.FreightShipmentDetail.FedExFreightBillingContactAndAddress.Contact.CompanyName = 'Some Company'
shipment.RequestedShipment.FreightShipmentDetail.FedExFreightBillingContactAndAddress.Contact.PhoneNumber = '9012638716'

shipment.RequestedShipment.FreightShipmentDetail.FedExFreightBillingContactAndAddress.Address.StreetLines = ['2000 Freight LTL Testing']
shipment.RequestedShipment.FreightShipmentDetail.FedExFreightBillingContactAndAddress.Address.City = 'Harrison'
shipment.RequestedShipment.FreightShipmentDetail.FedExFreightBillingContactAndAddress.Address.StateOrProvinceCode = 'AR'
shipment.RequestedShipment.FreightShipmentDetail.FedExFreightBillingContactAndAddress.Address.PostalCode = '72601'
shipment.RequestedShipment.FreightShipmentDetail.FedExFreightBillingContactAndAddress.Address.CountryCode = 'US'
shipment.RequestedShipment.FreightShipmentDetail.FedExFreightBillingContactAndAddress.Address.Residential = False
spec = shipment.create_wsdl_object_of_type('ShippingDocumentSpecification')

spec.ShippingDocumentTypes = [spec.CertificateOfOrigin]
# shipment.RequestedShipment.ShippingDocumentSpecification = spec

role = shipment.create_wsdl_object_of_type('FreightShipmentRoleType')

shipment.RequestedShipment.FreightShipmentDetail.Role = role.SHIPPER
shipment.RequestedShipment.FreightShipmentDetail.CollectTermsType = 'STANDARD'


# Specifies the label type to be returned.
shipment.RequestedShipment.LabelSpecification.LabelFormatType = 'FEDEX_FREIGHT_STRAIGHT_BILL_OF_LADING'

# Specifies which format the label file will be sent to you in.
# DPL, EPL2, PDF, PNG, ZPLII
shipment.RequestedShipment.LabelSpecification.ImageType = 'PDF'

# To use doctab stocks, you must change ImageType above to one of the
# label printer formats (ZPLII, EPL2, DPL).
# See documentation for paper types, there quite a few.
shipment.RequestedShipment.LabelSpecification.LabelStockType = 'PAPER_LETTER'

# This indicates if the top or bottom of the label comes out of the 
# printer first.
# BOTTOM_EDGE_OF_TEXT_FIRST or TOP_EDGE_OF_TEXT_FIRST
shipment.RequestedShipment.LabelSpecification.LabelPrintingOrientation = 'BOTTOM_EDGE_OF_TEXT_FIRST'
shipment.RequestedShipment.EdtRequestType = 'NONE'

package1_weight = shipment.create_wsdl_object_of_type('Weight')
package1_weight.Value = 500.0
package1_weight.Units = "LB"

shipment.RequestedShipment.FreightShipmentDetail.PalletWeight = package1_weight

package1 = shipment.create_wsdl_object_of_type('FreightShipmentLineItem')
package1.Weight = package1_weight
package1.Packaging = 'PALLET'
package1.Description = 'Products'
package1.FreightClass = 'CLASS_500'
package1.HazardousMaterials = None
package1.Pieces = 12


shipment.RequestedShipment.FreightShipmentDetail.LineItems = package1

# If you'd like to see some documentation on the ship service WSDL, un-comment
# this line. (Spammy).
#print shipment.client

# Un-comment this to see your complete, ready-to-send request as it stands
# before it is actually sent. This is useful for seeing what values you can
# change.
#print shipment.RequestedShipment

# If you want to make sure that all of your entered details are valid, you
# can call this and parse it just like you would via send_request(). If
# shipment.response.HighestSeverity == "SUCCESS", your shipment is valid.
#shipment.send_validation_request()

# Fires off the request, sets the 'response' attribute on the object.
shipment.send_request()

# This will show the reply to your shipment being sent. You can access the
# attributes through the response attribute on the request object. This is
# good to un-comment to see the variables returned by the Fedex reply.
print shipment.response
# Here is the overall end result of the query.
# print "HighestSeverity:", shipment.response.HighestSeverity
# # Getting the tracking number from the new shipment.
# print "Tracking #:", shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].TrackingIds[0].TrackingNumber
# # Net shipping costs.
# print "Net Shipping Cost (US$):", shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].PackageRating.PackageRateDetails[0].NetCharge.Amount

# # Get the label image in ASCII format from the reply. Note the list indices
# we're using. You'll need to adjust or iterate through these if your shipment
# has multiple packages.

ascii_label_data = shipment.response.CompletedShipmentDetail.ShipmentDocuments[0].Parts[0].Image

# Convert the ASCII data to binary.
label_binary_data = binascii.a2b_base64(ascii_label_data)

"""
This is an example of how to dump a label to a PNG file.
"""
# This will be the file we write the label out to.
pdf_file = open('example_shipment_label.pdf', 'wb')
pdf_file.write(label_binary_data)
pdf_file.close()

"""
This is an example of how to print the label to a serial printer. This will not
work for all label printers, consult your printer's documentation for more
details on what formats it can accept.
"""
# Pipe the binary directly to the label printer. Works under Linux
# without requiring PySerial. This WILL NOT work on other platforms.
#label_printer = open("/dev/ttyS0", "w")
#label_printer.write(label_binary_data)
#label_printer.close()

"""
This is a potential cross-platform solution using pySerial. This has not been
tested in a long time and may or may not work. For Windows, Mac, and other
platforms, you may want to go this route.
"""
#import serial
#label_printer = serial.Serial(0)
#print "SELECTED SERIAL PORT: "+ label_printer.portstr
#label_printer.write(label_binary_data)
#label_printer.close()