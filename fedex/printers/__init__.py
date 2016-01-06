"""
Optional classes used for the convenient printing of FedEx labels from
L{FedexProcessShipmentRequest} objects. Each printer class is more or less
the same, following the pattern seen below (unless otherwise documented).::
    from fedex.printers.unix import DirectDevicePrinter
    # Where shipment is an existing L{FedexProcessShipmentRequest} object.
    shipment.send_request()
    device = DirectDevicePrinter(shipment)
    device.print_label()
"""
