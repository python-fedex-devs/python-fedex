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
        self.device = device
        self.shipment = shipment
        
    def print_label(self, package_num=None):
        """
        Prints a shipment's labels, or optionally just one.
        
        package_num: (int) 0-based index of the package to print. This is
                           only useful for shipments with more than one package.
        """
        if package_num:
            packages = [self.shipment.response.CompletedShipmentDetail.CompletedPackageDetails[package_num]]
        else:
            packages = self.shipment.response.CompletedShipmentDetail.CompletedPackageDetails

        for package in packages:
            label_binary = binascii.a2b_base64(package.Label.Parts[0].Image)
            self.print_base64(label_binary)
    
    def print_base64(self, base64_data):
        """
        Pipe the binary directly to the label printer. Works under Linux
        without requiring PySerial.
        """
        label_file = open(self.device, "w")
        label_file.write(base64_data)
        label_file.close()