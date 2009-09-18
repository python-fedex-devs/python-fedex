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
from fedex.services.ship_service import FedexProcessShipmentRequest
from fedex.config import FedexConfig

# Set this to the INFO level to see the response from Fedex printed in stdout.
logging.basicConfig(level=logging.ERROR)

# FedexConfig objects should generally only be instantiated once and re-used
# amongst different queries. They hold static data like account number.
config_obj = FedexConfig(key='ZyNQQFdcxUATOx9L',
                         password='GtngmKzs4Dk4RYmrlAjrLykwi',
                         account_number='510087780',
                         meter_number='118501898',
                         use_test_server=True)

# This is the object that will be handling our tracking request.
shipment = FedexProcessShipmentRequest(config_obj)

# This is very generalized, top-level information.
# REGULAR_PICKUP, REQUEST_COURIER, DROP_BOX, BUSINESS_SERVICE_CENTER or STATION
shipment.RequestedShipment.DropoffType = 'REGULAR_PICKUP'

# See page 355 in WS_ShipService.pdf for a full list. Here are the common ones:
# STANDARD_OVERNIGHT, PRIORITY_OVERNIGHT, FEDEX_GROUND, FEDEX_EXPRESS_SAVER
shipment.RequestedShipment.ServiceType = 'PRIORITY_OVERNIGHT'

# What kind of package this will be shipped in.
# FEDEX_BOX, FEDEX_PAK, FEDEX_TUBE, YOUR_PACKAGING
shipment.RequestedShipment.PackagingType = 'FEDEX_PAK'

# No idea what this is.
# INDIVIDUAL_PACKAGES, PACKAGE_GROUPS, PACKAGE_SUMMARY 
shipment.RequestedShipment.PackageDetail = 'INDIVIDUAL_PACKAGES'

# Shipper contact info.
shipment.ShipperContact.PersonName = 'Sender Name'
shipment.ShipperContact.CompanyName = 'Some Company'
shipment.ShipperContact.PhoneNumber = '9012638716'

# Shipper address.
shipment.ShipperAddress.StreetLines = ['Address Line 1']
shipment.ShipperAddress.City = 'Herndon'
shipment.ShipperAddress.StateOrProvinceCode = 'VA'
shipment.ShipperAddress.PostalCode = '20171'
shipment.ShipperAddress.CountryCode = 'US'
shipment.ShipperAddress.Residential = True

# Recipient contact info.
shipment.RecipientContact.PersonName = 'Recipient Name'
shipment.RecipientContact.CompanyName = 'Recipient Company'
shipment.RecipientContact.PhoneNumber = '9012637906'

# Recipient address
shipment.RecipientAddress.StreetLines = ['Address Line 1']
shipment.RecipientAddress.City = 'Herndon'
shipment.RecipientAddress.StateOrProvinceCode = 'VA'
shipment.RecipientAddress.PostalCode = '20171'
shipment.RecipientAddress.CountryCode = 'US'
# This is needed to ensure an accurate rate quote with the response.
shipment.RecipientAddress.Residential = True

# RECIPIENT, SENDER or THIRD_PARTY
shipment.ShippingChargesPayment.PaymentType = 'SENDER' 

# These are example label values. You'll want to adjust these to fit your
# usage case.
shipment.LabelSpecification.LabelFormatType = 'COMMON2D'
shipment.LabelSpecification.ImageType = 'PNG'
shipment.LabelSpecification.LabelStockType = 'PAPER_7X4.75'

package1_weight = shipment.create_wsdl_object_of_type('Weight')
# Weight, in pounds.
package1_weight.Value = 1.0
package1_weight.Units = "LB"

package1 = shipment.create_wsdl_object_of_type('RequestedPackageLineItem')
package1.Weight = package1_weight
#print package1

shipment.add_package(package1)

# If you'd like to see some documentation on the ship service WSDL, un-comment
# this line. (Spammy).
#print shipment.client

# Un-comment this to see your complete, ready-to-send request as it stands
# before it is actually sent. This is useful for seeing what values you can
# change.
#print shipment.RequestedShipment

# Fires off the request, sets the 'response' attribute on the object.
shipment.send_request()

# This will show the reply to your shipment being sent. You can access the
# attributes through the response attribute on the request object. This is
# good to un-comment to see the variables returned by the Fedex reply.
#print shipment.response

# Here is the overall end result of the query.
print "HighestSeverity:", shipment.response.HighestSeverity
# Getting the tracking number from the new shipment.
print "Tracking #:", shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].TrackingIds[0].TrackingNumber
# Net shipping costs.
print "Net Shipping Cost (US$):", shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].PackageRating.PackageRateDetails[0].NetCharge.Amount

# Get the label image in ASCII format from the reply. Note the list indices
# we're using. You'll need to adjust or iterate through these if your shipment
# has multiple packages.
ascii_label_data = shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].Label.Parts[0].Image
# Convert the ASCII data to binary.
label_binary_data = binascii.a2b_base64(ascii_label_data)

"""
This is an example of how to dump a label to a PNG file.
"""
# This will be the file we write the label out to.
png_file = open('example_shipment_label.png', 'wb')
png_file.write(label_binary_data)
png_file.close()

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