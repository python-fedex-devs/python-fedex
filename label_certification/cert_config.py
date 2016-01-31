"""
This file holds configuration for your test account. Make SURE to change
the values below to your account's TESTING meter number.
"""
import os
import sys

# Use the fedex directory included in the downloaded package instead of
# any globally installed versions.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fedex.config import FedexConfig
from fedex.printers.unix import DirectDevicePrinter

# Change these values to match your testing account/meter number.
CONFIG_OBJ = FedexConfig(
        key='xxxxxxxxxxxxxxxx',
        password='xxxxxxxxxxxxxxxxxxxxxxxxx',
        account_number='#########',
        meter_number='#########',
        use_test_server=True)

# Change this to whoever should be the contact person for shipments.
SHIPPER_CONTACT_INFO = {
    'PersonName': 'Some Person',
    'CompanyName': 'Your Company',
    'PhoneNumber': '##########'
}

# The dictionary below should be your office/client's address that shipping
# will be originating from.
SHIPPER_ADDRESS = {
    'StreetLines': ['Address Line 1'],
    'City': 'Some City',
    'StateOrProvinceCode': 'SC',
    'PostalCode': '29631',
    'CountryCode': 'US',
    'Residential': False
}

# This contains the configuration for your label printer.
LABEL_SPECIFICATION = {
    # Specifies the label type to be returned.
    # LABEL_DATA_ONLY or COMMON2D
    'LabelFormatType': 'COMMON2D',
    # Specifies which format the label file will be
    # sent to you in.
    # DPL, EPL2, PDF, PNG, ZPLII
    'ImageType': 'EPL2',
    # To use doctab stocks, you must change ImageType above
    # to one of the label printer formats (ZPLII, EPL2, DPL).
    # See documentation for paper types, there quite a few.
    'LabelStockType': 'STOCK_4X6.75_LEADING_DOC_TAB',
    # This indicates if the top or bottom of the label comes
    # out of the printer first.
    # BOTTOM_EDGE_OF_TEXT_FIRST or TOP_EDGE_OF_TEXT_FIRST
    'LabelPrintingOrientation': 'BOTTOM_EDGE_OF_TEXT_FIRST'
}

# This should just be a reference to the correct printer class for your
# label printer. You may find these under the fedex.printers module.
# NOTE: This should NOT be an instance. It should just be a reference.
LabelPrinterClass = DirectDevicePrinter


def transfer_config_dict(soap_object, data_dict):
    """
    This is a utility function used in the certification modules to transfer
    the data dicts above to SOAP objects. This avoids repetition and allows
    us to store all of our variable configuration here rather than in
    each certification script.
    """
    for key, val in data_dict.items():
        # Transfer each key to the matching attribute ont he SOAP object.
        setattr(soap_object, key, val)
