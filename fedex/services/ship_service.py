"""
Ship Service Module
===================
This package contains the shipping methods defined by Fedex's 
ShipService WSDL file. Each is encapsulated in a class for easy access. 
For more details on each, refer to the respective class's documentation.
"""
from datetime import datetime
from .. base_service import FedexBaseService

class FedexProcessShipmentRequest(FedexBaseService):
    """
    This class allows you to track shipments by providing a tracking
    number or other identifying features. By default, you
    can simply pass a tracking number to the constructor. If you would like
    to query shipments based on something other than tracking number, you will
    want to read the documentation for the L{__init__} method. 
    Particularly, the tracking_value and package_identifier arguments.
    """
    def __init__(self, config_obj, *args, **kwargs):
        """
        Sends a shipment tracking request. The optional keyword args
        detailed on L{FedexBaseService} apply here as well.

        @type config_obj: L{FedexConfig}
        @param config_obj: A valid FedexConfig object.        
        """
        self._config_obj = config_obj
        
        # Holds version info for the VersionId SOAP object.
        self._version_info = {'service_id': 'ship', 'major': '7', 
                             'intermediate': '0', 'minor': '0'}
        # Call the parent FedexBaseService class for basic setup work.
        super(FedexProcessShipmentRequest, self).__init__(self._config_obj, 
                                                         'ShipService_v7.wsdl',
                                                         *args, **kwargs)
        # Prepare the data structures.
        self.__set_requested_shipment()
        
    def __set_requested_shipment(self):
        """
        This is the data that will be used to create your shipment. Create
        the data structure and get it ready for the WSDL request.
        """
        # This is the primary data structure for processShipment requests.
        self.RequestedShipment = self.client.factory.create('RequestedShipment')
        self.RequestedShipment.ShipTimestamp = datetime.now()
        
        self.Weight = self.client.factory.create('Weight')
        # Start at nothing.
        self.Weight.Value = 0.0
        # Default to pounds.
        self.Weight.Units = 'LB'
        # This is the total weight of the entire shipment. Shipments may
        # contain more than one package.
        self.RequestedShipment.TotalWeight = self.Weight
        
        """
        Begin shipper info.
        """
        self.ShipperContact = self.client.factory.create('Contact')
        self.ShipperAddress = self.client.factory.create('Address')
        
        # This is the top level data structure for Shipper information.
        self.ShipperParty = self.client.factory.create('Party')
        self.ShipperParty.Address = self.ShipperAddress
        self.ShipperParty.Contact = self.ShipperContact
        
        # Link the ShipperParty to our master data structure.
        self.RequestedShipment.Shipper = self.ShipperParty
        """
        End shipper info.
        """
        
        """
        Begin recipient info.
        """
        self.RecipientContact = self.client.factory.create('Contact')
        self.RecipientAddress = self.client.factory.create('Address')
        
        # This is the top level data structure for Recipient information.
        self.RecipientParty = self.client.factory.create('Party')
        self.RecipientParty.Contact = self.RecipientContact
        self.RecipientParty.Address = self.RecipientAddress
        
        # Link the RecipientParty object to our master data structure.
        self.RequestedShipment.Recipient = self.RecipientParty
        """
        End recipient info.
        """
                
        self.Payor = self.client.factory.create('Payor')
        # Grab the account number from the FedexConfig object by default.
        self.Payor.AccountNumber = self._config_obj.account_number
        # Assume US.
        self.Payor.CountryCode = 'US'
        
        self.ShippingChargesPayment = self.client.factory.create('Payment')
        self.ShippingChargesPayment.Payor = self.Payor
        self.RequestedShipment.ShippingChargesPayment = self.ShippingChargesPayment
        
        self.LabelSpecification = self.client.factory.create('LabelSpecification')
        self.RequestedShipment.LabelSpecification = self.LabelSpecification
        
        self.RequestedShipment.RateRequestTypes = ['ACCOUNT'] # ACCOUNT and LIST
        
        # Start with no packages, user must add them.
        self.RequestedShipment.PackageCount = 0
        self.RequestedShipment.RequestedPackageLineItems = []
                
        # This is good to review if you'd like to see what the data structure
        # looks like.
        self.logger.info(self.RequestedShipment)
        
    def _assemble_and_send_request(self):
        """
        Fires off the Fedex request.
        
        @warning: NEVER CALL THIS METHOD DIRECTLY. CALL send_request(), WHICH RESIDES
            ON FedexBaseService AND IS INHERITED.
        """
        # Fire off the query.
        response = self.client.service.processShipment(WebAuthenticationDetail=self.WebAuthenticationDetail,
                                        ClientDetail=self.ClientDetail,
                                        TransactionDetail=self.TransactionDetail,
                                        Version=self.VersionId,
                                        RequestedShipment=self.RequestedShipment)
        return response
    
    def add_package(self, package_item):
        """
        Adds a package to the ship request.
        
        @type package_item: L{RequestedPackageLineItem}
        @keyword package_item: A L{RequestedPackageLineItem}, created by
            calling create_wsdl_object_of_type('RequestedPackageLineItem') on
            this ShipmentRequest object. See examples/create_shipment.py for
            more details.
        """
        self.RequestedShipment.RequestedPackageLineItems.append(package_item)
        package_weight = package_item.Weight.Value
        self.RequestedShipment.TotalWeight.Value += package_weight
        self.RequestedShipment.PackageCount += 1