"""
Ship Service Module
===================
This package contains the shipping methods defined by Fedex's 
ShipService WSDL file. Each is encapsulated in a class for easy access. 
For more details on each, refer to the respective class's documentation.
"""
from datetime import datetime
from .. base_service import FedexBaseService

class FedexShipRequest(FedexBaseService):
    """
    This class allows you to track shipments by providing a tracking
    number or other identifying features. By default, you
    can simply pass a tracking number to the constructor. If you would like
    to query shipments based on something other than tracking number, you will
    want to read the documentation for the L{__init__} method. 
    Particularly, the tracking_value and package_identifier arguments.
    """
    def __init__(self, config_obj, tracking_value,
                 package_identifier='TRACKING_NUMBER_OR_DOORTAG',
                 *args, **kwargs):
        """
        Sends a shipment tracking request. The optional keyword args
        detailed on L{FedexBaseService} apply here as well.
        
        @type  tracking_value: L{str} 
        @param tracking_value: Based on the value of package_identifier, 
            this will be anything from a tracking number to a purchase order 
            number.
        @type    package_identifier: L{str}
        @keyword package_identifier: Determines what you are using to query for
            the shipment. The default assumes that tracking_value will be a Fedex 
            tracking number.
        """
        self._config_obj = config_obj
        
        # Holds version info for the VersionId SOAP object.
        self._version_info = {'service_id': 'ship', 'major': '7', 
                             'intermediate': '0', 'minor': '0'}
        # Call the parent FedexBaseService class for basic setup work.
        super(FedexShipRequest, self).__init__(self._config_obj, 
                                                'ShipService_v7.wsdl',
                                                *args, **kwargs)
        
    def __set_requested_shipment(self):
        """
        This is the data that will be used to create your shipment. Create
        the data structure and get it ready for the WSDL request.
        """
        RequestedShipment = self.client.factory.create('RequestedShipment')
        RequestedShipment.ShipTimestamp = datetime.now()
        RequestedShipment.DropoffType = 'REGULAR_PICKUP' # REGULAR_PICKUP, REQUEST_COURIER, DROP_BOX, BUSINESS_SERVICE_CENTER and STATION
        RequestedShipment.ServiceType = 'PRIORITY_OVERNIGHT' # valid values STANDARD_OVERNIGHT, PRIORITY_OVERNIGHT, FEDEX_GROUND
        RequestedShipment.PackagingType = 'FEDEX_PAK' # valid values FEDEX_BOX, FEDEX_PAK, FEDEX_TUBE, YOUR_PACKAGING
        
        Weight = self.client.factory.create('Weight')
        Weight.Value = 50.0
        Weight.Units = 'LB' # LB or KG
        # Assemble
        RequestedShipment.TotalWeight = Weight
        
        """
        Begin shipper info.
        """
        ShipperParty = self.client.factory.create('Party')
        ShipperContact = self.client.factory.create('Contact')
        ShipperContact.PersonName = 'Sender Name'
        ShipperContact.CompanyName = 'Some Company'
        ShipperContact.PhoneNumber = '9012638716'
        # Assemble
        ShipperParty.Contact = ShipperContact
        
        ShipperAddress = self.client.factory.create('Address')
        ShipperAddress.StreetLines = ['Address Line 1']
        ShipperAddress.City = 'Herndon'
        ShipperAddress.StateOrProvinceCode = 'VA'
        ShipperAddress.PostalCode = '20171'
        ShipperAddress.CountryCode = 'US'
        ShipperAddress.Residential = True
        # Assemble
        ShipperParty.Address = ShipperAddress
        # Assemble
        RequestedShipment.Shipper = ShipperParty
        """
        End shipper info.
        """
        
        """
        Begin recipient info.
        """
        RecipientParty = self.client.factory.create('Party')
        RecipientContact = self.client.factory.create('Contact')
        RecipientContact.PersonName = 'Recipient Name'
        RecipientContact.CompanyName = 'Recipient Company'
        RecipientContact.PhoneNumber = '9012637906'
        # Assemble
        RecipientParty.Contact = RecipientContact
        
        RecipientAddress = self.client.factory.create('Address')
        RecipientAddress.StreetLines = ['Address Line 1']
        RecipientAddress.City = 'Herndon'
        RecipientAddress.StateOrProvinceCode = 'VA'
        RecipientAddress.PostalCode = '20171'
        RecipientAddress.CountryCode = 'US'
        RecipientAddress.Residential = True
        # Assemble
        RecipientParty.Address = RecipientAddress
        # Assemble
        RequestedShipment.Recipient = RecipientParty
        """
        End recipient info.
        """
        
        ShippingChargesPayment = self.client.factory.create('Payment')
        ShippingChargesPayment.PaymentType = 'SENDER' # RECIPIENT, SENDER and THIRD_PARTY
        Payor = self.client.factory.create('Payor')
        Payor.AccountNumber = self._config_obj.account_number
        Payor.CountryCode = 'US'
        ShippingChargesPayment.Payor = Payor
        # Assemble
        RequestedShipment.ShippingChargesPayment = ShippingChargesPayment
        
        RequestedShipment.RateRequestTypes = ['ACCOUNT'] # ACCOUNT and LIST
        RequestedShipment.PackageCount = 1
        RequestedShipment.PackageDetail = 'INDIVIDUAL_PACKAGES'
                
        self.logger.debug(RequestedShipment)
        self.RequestedShipment = RequestedShipment
        
    def _assemble_and_send_request(self):
        """
        Fires off the Fedex request.
        
        @warning: NEVER CALL THIS METHOD DIRECTLY. CALL send_request(), WHICH RESIDES
            ON FedexBaseService AND IS INHERITED.
        """
        self.__set_requested_shipment()
        client = self.client
        # Fire off the query.
        response = client.service.processShipment(WebAuthenticationDetail=self.WebAuthenticationDetail,
                                        ClientDetail=self.ClientDetail,
                                        TransactionDetail=self.TransactionDetail,
                                        Version=self.VersionId,
                                        RequestedShipment=self.RequestedShipment)
        """
        processShipment(WebAuthenticationDetail WebAuthenticationDetail, 
                        ClientDetail ClientDetail, 
                        TransactionDetail TransactionDetail, 
                        VersionId Version, 
                        RequestedShipment RequestedShipment)
        """
        return response