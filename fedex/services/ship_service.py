"""
Ship Service Module

This package contains the shipping methods defined by Fedex's 
ShipService WSDL file. Each is encapsulated in a class for easy access. 
For more details on each, refer to the respective class's documentation.
"""

import datetime
from ..base_service import FedexBaseService


class FedexProcessShipmentRequest(FedexBaseService):
    """
    This class allows you to process (create) a new FedEx shipment. You will
    need to populate the data structures in self.RequestedShipment, then
    send the request. Label printing is supported and very configurable,
    returning an ASCII representation with the response as well.
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
        self._version_info = {
            'service_id': 'ship',
            'major': '23',
            'intermediate': '0',
            'minor': '0'
        }
        self.RequestedShipment = None
        """@ivar: Holds the RequestedShipment WSDL object."""
        # Call the parent FedexBaseService class for basic setup work.
        super(FedexProcessShipmentRequest, self).__init__(
                self._config_obj, 'ShipService_v23.wsdl', *args, **kwargs)

    def _prepare_wsdl_objects(self):
        """
        This is the data that will be used to create your shipment. Create
        the data structure and get it ready for the WSDL request.
        """

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

        # This is the top level data structure Shipper Party information.
        shipper_party = self.client.factory.create('Party')
        shipper_party.Address = self.client.factory.create('Address')
        shipper_party.Contact = self.client.factory.create('Contact')

        # Link the Shipper Party to our master data structure.
        self.RequestedShipment.Shipper = shipper_party

        # This is the top level data structure for RecipientParty information.
        recipient_party = self.client.factory.create('Party')
        recipient_party.Contact = self.client.factory.create('Contact')
        recipient_party.Address = self.client.factory.create('Address')

        # Link the RecipientParty object to our master data structure.
        self.RequestedShipment.Recipient = recipient_party

        payor = self.client.factory.create('Payor')
        # Grab the account number from the FedexConfig object by default.
        # Assume US.
        payor.ResponsibleParty = self.client.factory.create('Party')
        payor.ResponsibleParty.Address = self.client.factory.create('Address')
        payor.ResponsibleParty.Address.CountryCode = 'US'

        # ShippingChargesPayment WSDL object default values.
        shipping_charges_payment = self.client.factory.create('Payment')
        shipping_charges_payment.Payor = payor
        shipping_charges_payment.PaymentType = 'SENDER'
        self.RequestedShipment.ShippingChargesPayment = shipping_charges_payment

        self.RequestedShipment.LabelSpecification = self.client.factory.create('LabelSpecification')

        # NONE, PREFERRED or LIST
        self.RequestedShipment.RateRequestTypes = ['PREFERRED']

        # Start with no packages, user must add them.
        self.RequestedShipment.PackageCount = 0
        self.RequestedShipment.RequestedPackageLineItems = []

        # This is good to review if you'd like to see what the data structure
        # looks like.
        self.logger.debug(self.RequestedShipment)

    def send_validation_request(self):
        """
        This is very similar to just sending the shipment via the typical
        send_request() function, but this doesn't create a shipment. It is
        used to make sure "good" values are given by the user or the
        application using the library.
        """

        self.send_request(send_function=self._assemble_and_send_validation_request)

    def _assemble_and_send_validation_request(self):
        """
        Fires off the Fedex shipment validation request.
        
        @warning: NEVER CALL THIS METHOD DIRECTLY. CALL 
            send_validation_request(), WHICH RESIDES ON FedexBaseService 
            AND IS INHERITED.
        """

        # Fire off the query.
        return self.client.service.validateShipment(
                WebAuthenticationDetail=self.WebAuthenticationDetail,
                ClientDetail=self.ClientDetail,
                TransactionDetail=self.TransactionDetail,
                Version=self.VersionId,
                RequestedShipment=self.RequestedShipment)

    def _assemble_and_send_request(self):
        """
        Fires off the Fedex request.
        
        @warning: NEVER CALL THIS METHOD DIRECTLY. CALL send_request(), 
            WHICH RESIDES ON FedexBaseService AND IS INHERITED.
        """

        # Fire off the query.
        return self.client.service.processShipment(
                WebAuthenticationDetail=self.WebAuthenticationDetail,
                ClientDetail=self.ClientDetail,
                TransactionDetail=self.TransactionDetail,
                Version=self.VersionId,
                RequestedShipment=self.RequestedShipment)

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


class FedexDeleteShipmentRequest(FedexBaseService):
    """
    This class allows you to delete a shipment, given a tracking number.
    """

    def __init__(self, config_obj, *args, **kwargs):
        """
        Deletes a shipment via a tracking number.
        """

        self._config_obj = config_obj

        # Holds version info for the VersionId SOAP object.
        self._version_info = {'service_id': 'ship', 'major': '23',
                              'intermediate': '0', 'minor': '0'}
        self.DeletionControlType = None
        """@ivar: Holds the DeletrionControlType WSDL object."""
        self.TrackingId = None
        """@ivar: Holds the TrackingId WSDL object."""
        # Call the parent FedexBaseService class for basic setup work.
        super(FedexDeleteShipmentRequest, self).__init__(self._config_obj,
                                                         'ShipService_v23.wsdl',
                                                         *args, **kwargs)

    def _prepare_wsdl_objects(self):
        """
        Preps the WSDL data structures for the user.
        """

        self.DeletionControlType = self.client.factory.create('DeletionControlType')
        self.TrackingId = self.client.factory.create('TrackingId')
        self.TrackingId.TrackingIdType = self.client.factory.create('TrackingIdType')

    def _assemble_and_send_request(self):
        """
        Fires off the Fedex request.
        
        @warning: NEVER CALL THIS METHOD DIRECTLY. CALL send_request(), WHICH RESIDES
            ON FedexBaseService AND IS INHERITED.
        """

        client = self.client
        # Fire off the query.
        return client.service.deleteShipment(
                WebAuthenticationDetail=self.WebAuthenticationDetail,
                ClientDetail=self.ClientDetail,
                TransactionDetail=self.TransactionDetail,
                Version=self.VersionId,
                ShipTimestamp=datetime.datetime.now(),
                TrackingId=self.TrackingId,
                DeletionControl=self.DeletionControlType)
