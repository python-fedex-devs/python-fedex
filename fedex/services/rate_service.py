"""
Rate Service Module

This package contains classes to request pre-ship rating information and to
determine estimated or courtesy billing quotes. Time in Transit can be
returned with the rates if it is specified in the request.
"""

import datetime
from ..base_service import FedexBaseService


class FedexRateServiceRequest(FedexBaseService):
    """
    This class allows you to get the shipping charges for a particular address. 
    You will need to populate the data structures in self.RequestedShipment, 
    then send the request.
    """

    def __init__(self, config_obj, *args, **kwargs):
        """
        The optional keyword args detailed on L{FedexBaseService} 
        apply here as well.

        @type config_obj: L{FedexConfig}
        @param config_obj: A valid FedexConfig object.        
        """

        self._config_obj = config_obj

        # Holds version info for the VersionId SOAP object.
        self._version_info = {'service_id': 'crs', 'major': '24',
                              'intermediate': '0', 'minor': '0'}

        self.RequestedShipment = None
        """@ivar: Holds the RequestedShipment WSDL object including the shipper, recipient and shipt time."""
        # Call the parent FedexBaseService class for basic setup work.
        super(FedexRateServiceRequest, self).__init__(
                self._config_obj, 'RateService_v24.wsdl', *args, **kwargs)
        self.ClientDetail.Region = config_obj.express_region_code
        """@ivar: Holds the express region code from the config object."""

    def _prepare_wsdl_objects(self):
        """
        This is the data that will be used to create your shipment. Create
        the data structure and get it ready for the WSDL request.
        """

        # Default behavior is to not request transit information
        self.ReturnTransitAndCommit = False

        # This is the primary data structure for processShipment requests.
        self.RequestedShipment = self.client.factory.create('RequestedShipment')
        self.RequestedShipment.ShipTimestamp = datetime.datetime.now()

        # Defaults for TotalWeight wsdl object.
        total_weight = self.client.factory.create('Weight')
        # Start at nothing.
        total_weight.Value = 0.0
        # Default to pounds.
        total_weight.Units = 'LB'
        # This is the total weight of the entire shipment. Shipments may
        # contain more than one package.
        self.RequestedShipment.TotalWeight = total_weight

        # This is the top level data structure for Shipper information.
        shipper = self.client.factory.create('Party')
        shipper.Address = self.client.factory.create('Address')
        shipper.Contact = self.client.factory.create('Contact')

        # Link the ShipperParty to our master data structure.
        self.RequestedShipment.Shipper = shipper

        # This is the top level data structure for Recipient information.
        recipient_party = self.client.factory.create('Party')
        recipient_party.Contact = self.client.factory.create('Contact')
        recipient_party.Address = self.client.factory.create('Address')
        # Link the RecipientParty object to our master data structure.
        self.RequestedShipment.Recipient = recipient_party

        # Make sender responsible for payment by default.
        self.RequestedShipment.ShippingChargesPayment = self.create_wsdl_object_of_type('Payment')
        self.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'

        # Start with no packages, user must add them.
        self.RequestedShipment.PackageCount = 0
        self.RequestedShipment.RequestedPackageLineItems = []

        # This is good to review if you'd like to see what the data structure
        # looks like.
        self.logger.debug(self.RequestedShipment)

    def _assemble_and_send_request(self):
        """
        Fires off the Fedex request.
        
        @warning: NEVER CALL THIS METHOD DIRECTLY. CALL send_request(), 
            WHICH RESIDES ON FedexBaseService AND IS INHERITED.
        """

        # Fire off the query.
        return self.client.service.getRates(
                WebAuthenticationDetail=self.WebAuthenticationDetail,
                ClientDetail=self.ClientDetail,
                TransactionDetail=self.TransactionDetail,
                Version=self.VersionId,
                RequestedShipment=self.RequestedShipment,
                ReturnTransitAndCommit=self.ReturnTransitAndCommit)

    def add_package(self, package_item):
        """
        Adds a package to the ship request.
        
        @type package_item: WSDL object, type of RequestedPackageLineItem 
            WSDL object.
        @keyword package_item: A RequestedPackageLineItem, created by
            calling create_wsdl_object_of_type('RequestedPackageLineItem') on
            this ShipmentRequest object. See examples/create_shipment.py for
            more details.
        """

        self.RequestedShipment.RequestedPackageLineItems.append(package_item)
        package_weight = package_item.Weight.Value
        self.RequestedShipment.TotalWeight.Value += package_weight
        self.RequestedShipment.PackageCount += 1
