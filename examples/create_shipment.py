#!/usr/bin/env python
"""
This example shows how to ship shipments.
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
ship = FedexProcessShipmentRequest(config_obj)

# This is very generalized, top-level information.
# REGULAR_PICKUP, REQUEST_COURIER, DROP_BOX, BUSINESS_SERVICE_CENTER or STATION
ship.RequestedShipment.DropoffType = 'REGULAR_PICKUP'

# See page 355 in WS_ShipService.pdf for a full list. Here are the common ones:
# STANDARD_OVERNIGHT, PRIORITY_OVERNIGHT, FEDEX_GROUND, FEDEX_EXPRESS_SAVER
ship.RequestedShipment.ServiceType = 'PRIORITY_OVERNIGHT'

# What kind of package this will be shipped in.
# FEDEX_BOX, FEDEX_PAK, FEDEX_TUBE, YOUR_PACKAGING
ship.RequestedShipment.PackagingType = 'FEDEX_PAK'

# No idea what this is.
# INDIVIDUAL_PACKAGES, PACKAGE_GROUPS, PACKAGE_SUMMARY 
ship.RequestedShipment.PackageDetail = 'INDIVIDUAL_PACKAGES'

# Shipper contact info.
ship.ShipperContact.PersonName = 'Sender Name'
ship.ShipperContact.CompanyName = 'Some Company'
ship.ShipperContact.PhoneNumber = '9012638716'

# Shipper address.
ship.ShipperAddress.StreetLines = ['Address Line 1']
ship.ShipperAddress.City = 'Herndon'
ship.ShipperAddress.StateOrProvinceCode = 'VA'
ship.ShipperAddress.PostalCode = '20171'
ship.ShipperAddress.CountryCode = 'US'
ship.ShipperAddress.Residential = True

# Recipient contact info.
ship.RecipientContact.PersonName = 'Recipient Name'
ship.RecipientContact.CompanyName = 'Recipient Company'
ship.RecipientContact.PhoneNumber = '9012637906'

# Recipient address
ship.RecipientAddress.StreetLines = ['Address Line 1']
ship.RecipientAddress.City = 'Herndon'
ship.RecipientAddress.StateOrProvinceCode = 'VA'
ship.RecipientAddress.PostalCode = '20171'
ship.RecipientAddress.CountryCode = 'US'
# This is needed to ensure an accurate rate quote with the response.
ship.RecipientAddress.Residential = True

# RECIPIENT, SENDER or THIRD_PARTY
ship.ShippingChargesPayment.PaymentType = 'SENDER' 

# These are example label values. You'll want to adjust these to fit your
# usage case.
ship.LabelSpecification.LabelFormatType = 'COMMON2D'
ship.LabelSpecification.ImageType = 'PNG'
ship.LabelSpecification.LabelStockType = 'PAPER_7X4.75'

package1_weight = ship.create_wsdl_object_of_type('Weight')
# Weight, in pounds.
package1_weight.Value = 1.0
package1_weight.Units = "LB"

package1 = ship.create_wsdl_object_of_type('RequestedPackageLineItem')
package1.Weight = package1_weight
#print package1

ship.add_package(package1)

# If you'd like to see some documentation on the ship service WSDL, un-comment
# this line. (Spammy).
#print ship.client

# Un-comment this to see your complete, ready-to-send request as it stands
# before it is actually sent. This is useful for seeing what values you can
# change.
#print ship.RequestedShipment

# Fires off the request, sets the 'response' attribute on the object.
ship.send_request()

# This will show the reply to your shipment being sent. You can access the
# attributes through the response attribute on the request object.
print ship.response

# Get the label image in ASCII format from the reply. Note the list indices
# we're using. You'll need to adjust or iterate through these if your shipment
# has multiple packages.
ascii_label_data = ship.response.CompletedShipmentDetail.CompletedPackageDetails[0].Label.Parts[0].Image
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