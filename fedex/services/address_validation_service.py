"""
Address Validation Service Module
=================================
This package contains the shipping methods defined by Fedex's 
AddressValidationService WSDL file. Each is encapsulated in a class for 
easy access. For more details on each, refer to the respective class's 
documentation.
"""
from datetime import datetime
from .. base_service import FedexBaseService

class FedexAddressValidationRequest(FedexBaseService):
    """
    This class allows you validate anywhere from one to a hundred addresses
    in one go. Create AddressToValidate WSDL objects and add them to each
    instance of this request using add_address().
    """
    def __init__(self, config_obj, *args, **kwargs):
        """
        @type config_obj: L{FedexConfig}
        @param config_obj: A valid FedexConfig object.        
        """
        self._config_obj = config_obj
        
        # Holds version info for the VersionId SOAP object.
        self._version_info = {'service_id': 'aval', 'major': '2', 
                             'intermediate': '0', 'minor': '0'}
        
        self.AddressValidationOptions = None
        """@ivar: Holds the AddressValidationOptions WSDL object."""
        self.addresses_to_validate = []
        """@ivar: Holds the AddressToValidate WSDL object."""
        # Call the parent FedexBaseService class for basic setup work.
        super(FedexAddressValidationRequest, self).__init__(self._config_obj, 
                                                         'AddressValidationService_v2.wsdl',
                                                         *args, **kwargs)
        
    def _prepare_wsdl_objects(self):
        """
        Create the data structure and get it ready for the WSDL request.
        """
        # This holds some optional options for the request..
        self.AddressValidationOptions = self.client.factory.create('AddressValidationOptions')
                               
        # This is good to review if you'd like to see what the data structure
        # looks like.
        self.logger.debug(self.AddressValidationOptions)
    
    def _assemble_and_send_request(self):
        """
        Fires off the Fedex request.
        
        @warning: NEVER CALL THIS METHOD DIRECTLY. CALL send_request(), 
            WHICH RESIDES ON FedexBaseService AND IS INHERITED.
        """
        # We get an exception like this when specifying an IntegratorId:
        # suds.TypeNotFound: Type not found: 'IntegratorId'
        # Setting it to None does not seem to appease it.
        del self.ClientDetail.IntegratorId
        self.logger.debug(self.WebAuthenticationDetail)
        self.logger.debug(self.ClientDetail)
        self.logger.debug(self.TransactionDetail)
        self.logger.debug(self.VersionId)
        # Fire off the query.
        response = self.client.service.addressValidation(WebAuthenticationDetail=self.WebAuthenticationDetail,
                                        ClientDetail=self.ClientDetail,
                                        TransactionDetail=self.TransactionDetail,
                                        Version=self.VersionId,
                                        RequestTimestamp=datetime.now(),
                                        Options=self.AddressValidationOptions,
                                        AddressesToValidate=self.addresses_to_validate)
        return response

    def add_address(self, address_item):
        """
        Adds an address to self.addresses_to_validate.
        
        @type address_item: WSDL object, type of AddressToValidate WSDL object.
        @keyword address_item: A AddressToValidate, created by
            calling create_wsdl_object_of_type('AddressToValidate') on
            this FedexAddressValidationRequest object. 
            See examples/create_shipment.py for more details.
        """
        self.addresses_to_validate.append(address_item)