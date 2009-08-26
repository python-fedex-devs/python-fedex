import os
import logging
from suds.client import Client

class FedexBaseService(object):
    def __init__(self, config_obj, wsdl_name, *args, **kwargs):
        self.config_obj = config_obj
        self.wsdl_path = os.path.join(config_obj.wsdl_path, wsdl_name)
        self.client = Client('file://%s' % self.wsdl_path)
        self.logger = logging.getLogger('fedex')
        
        self.logger.debug(self.client)
        self.set_web_authentication_detail()
        self.set_client_detail()
        self.set_version_id()
        self.set_carrier_code_type(*args, **kwargs)
        self.set_transaction_detail(*args, **kwargs)
        
    def set_web_authentication_detail(self):
        """
        Sets up the WebAuthenticationDetail node. This is required for all
        requests.
        """
        # Start of the authentication stuff.
        WebAuthenticationCredential = self.client.factory.create('WebAuthenticationCredential')
        WebAuthenticationCredential.Key = self.config_obj.key
        WebAuthenticationCredential.Password = self.config_obj.password
        
        # Encapsulates the auth credentials.
        WebAuthenticationDetail = self.client.factory.create('WebAuthenticationDetail')
        WebAuthenticationDetail.UserCredential = WebAuthenticationCredential
        self.logger.debug(WebAuthenticationDetail)
        self.WebAuthenticationDetail = WebAuthenticationDetail
        
    def set_client_detail(self):
        """
        Sets up the ClientDetail node, which is required for all shipping
        related requests.
        """
        ClientDetail = self.client.factory.create('ClientDetail')
        ClientDetail.AccountNumber = self.config_obj.account_number
        ClientDetail.MeterNumber = self.config_obj.meter_number
        ClientDetail.IntegratorId = self.config_obj.integrator_id
        self.logger.debug(ClientDetail)
        self.ClientDetail = ClientDetail
        
    def set_transaction_detail(self, *args, **kwargs):
        """
        Checks kwargs for 'customer_transaction_id' and sets it if present.
        """
        customer_transaction_id = kwargs.get('customer_transaction_id', False)
        if customer_transaction_id:
            TransactionDetail = client.factory.create('TransactionDetail')
            TransactionDetail.CustomerTransactionId = customer_transaction_id
            self.logger.debug(TransactionDetail)
            self.TransactionDetail = TransactionDetail
        else:
            self.TransactionDetail = None
            
    def set_carrier_code_type(self, *args, **kwargs):
        """
        Checks kwargs for 'carrier_code' and sets it if present. 
        """
        carrier_code = kwargs.get('carrier_code', False)
        if carrier_code:
            CarrierCodeType = self.client.factory.create('CarrierCodeType')
            CarrierCodeType.Type = carrier_code
            self.logger.debug(CarrierCodeType)
            self.CarrierCodeType = CarrierCodeType
        else:
            self.CarrierCodeType = None
    
    def set_version_id(self):
        """
        Pulles the versioning info for the request from the child request.
        """
        VersionId = self.client.factory.create('VersionId')
        VersionId.ServiceId = self.version_info['service_id']
        VersionId.Major = self.version_info['major']
        VersionId.Intermediate = self.version_info['intermediate']
        VersionId.Minor = self.version_info['minor']
        self.logger.debug(VersionId)
        self.VersionId = VersionId
        
    def send_request(self):
        """
        Sends the assembled request on the child object.
        """
        self.response = self.assemble_and_send_request()
        self.logger.info("== FEDEX QUERY RESULT ==")
        self.logger.info(self.response)