"""
Ship Service Module
===================
This package contains the shipping methods defined by Fedex's 
ShipService WSDL file. Each is encapsulated in a class for easy access. 
For more details on each, refer to the respective class's documentation.
"""
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
        self._version_info = {'service_id': 'trck', 'major': '7', 
                             'intermediate': '0', 'minor': '0'}
        # Call the parent FedexBaseService class for basic setup work.
        super(FedexShipRequest, self).__init__(self._config_obj, 
                                                'ShipService_v7.wsdl',
                                                *args, **kwargs)
        
    def __set_transactional_detail(self):
        """
        """
        TransactionDetail = self.client.factory.create('TransactionDetail')
        self.logger.info(TransactionDetail)
        self.TransactionDetail = TransactionDetail
        
    def _assemble_and_send_request(self):
        """
        Fires off the Fedex request.
        
        @warning: NEVER CALL THIS METHOD DIRECTLY. CALL send_request(), WHICH RESIDES
            ON FedexBaseService AND IS INHERITED.
        """
        self.__set_transactional_detail()
        client = self.client
        # Fire off the query.
        """
        processShipment(WebAuthenticationDetail WebAuthenticationDetail, 
                        ClientDetail ClientDetail, 
                        TransactionDetail TransactionDetail, 
                        VersionId Version, 
                        RequestedShipment RequestedShipment)
        """
        #return response