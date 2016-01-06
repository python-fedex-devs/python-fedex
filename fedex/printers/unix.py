"""
This module provides a label printing wrapper class for Unix-based
installations. By "Unix", we mean Linux, Mac OS, BSD, and various flavors
of Unix.
"""

import binascii


class DirectDevicePrinter(object):
    """
    This class pipes the label data directly through a /dev/* entry.
    Consequently, this is very Unix/Linux specific. It *MAY* work on Mac too.
    """

    def __init__(self, shipment, device="/dev/ttyS0"):
        """
        Instantiates from a shipment object. You may optionally specify
        a path to a /dev/ device. Defaults to /dev/ttyS0.
        
        @type shipment: L{FedexProcessShipmentRequest}
        @param shipment: A Fedex ProcessShipmentRequest object to pull the
                         printed label data from.
        """

        self.device = device
        """@ivar: A string with the path to the device to print to."""
        self.shipment = shipment
        """@ivar: A reference to the L{FedexProcessShipmentRequest} to print."""

    def print_label(self, package_num=None):
        """
        Prints all of a shipment's labels, or optionally just one.
        
        @type package_num: L{int}
        @param package_num: 0-based index of the package to print. This is
                            only useful for shipments with more than one package.
        """

        if package_num:
            packages = [
                self.shipment.response.CompletedShipmentDetail.CompletedPackageDetails[package_num]
            ]
        else:
            packages = self.shipment.response.CompletedShipmentDetail.CompletedPackageDetails

        for package in packages:
            label_binary = binascii.a2b_base64(package.Label.Parts[0].Image)
            self._print_base64(label_binary)

    def _print_base64(self, base64_data):
        """
        Pipe the binary directly to the label printer. Works under Linux
        without requiring PySerial. This is not typically something you
        should call directly, unless you have special needs.
        
        @type base64_data: L{str}
        @param base64_data: The base64 encoded string for the label to print.
        """

        label_file = open(self.device, "w")
        label_file.write(base64_data)
        label_file.close()
