"""
The L{base_service} module contains classes that form the low level foundations
of the Web Service API. Things that many different kinds of requests have in
common may be found here.

In particular, the L{FedexBaseService} class handles most of the basic,
repetetive setup work that most requests do.
"""
import os
import logging
from suds.client import Client

class FedexBaseServiceException(Exception):
    """
    Serves as the base exception that other service-related exception objects
    are sub-classed from.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class FedexFailure(FedexBaseServiceException):
    """
    The request could not be handled at this time. This is generally a server
    problem.
    """
    def __init__(self):
        self.value = "Your request could not be handled at this time. This is likely Fedex server problems, try again later."

class FedexBaseService(object):
    """
    This class is the master class for all Fedex request objects. It gets all
    of the common SOAP objects created via suds and populates them with
    values from a L{FedexConfig} object, along with keyword arguments
    via L{__init__}.
    
    @note: This object should never be used directly, use one of the included
        sub-classes.
    """
    def __init__(self, config_obj, wsdl_name, *args, **kwargs):
        """
        This constructor should only be called by children of the class. As is
        such, only the optional keyword arguments caught by C{**kwargs} will
        be documented.
        
        @type customer_transaction_id: L{str}
        @keyword customer_transaction_id: A user-specified identifier to
            differentiate this transaction from others. This value will be
            returned with the response from Fedex.
        @type carrier_code: L{str}
        @keyword carrier_code: The carrier code to use for this query. In most
            cases, this will be FDXE (Fedex Express). Must be one of the
            following four-letter codes:
                - FDXC (Fedex Cargo)
                - FDXE (Fedex Express)
                - FDXG (Fedex Ground)
                - FXCC (Fedex Custom Critical)
                - FXFR (Fedex Freight)
                - FXSP (Fedex Smartpost)
        """
        self.config_obj = config_obj
        self.wsdl_path = os.path.join(config_obj.wsdl_path, wsdl_name)
        self.client = Client('file://%s' % self.wsdl_path)
        self.logger = logging.getLogger('fedex')
        self.response = None
        """@ivar: The response from Fedex. You will want to pick what you
            want out here here. This object does have a __str__() method,
            you'll want to print or log it to see what possible values
            you can pull."""
        
        self.logger.debug(self.client)
        self.__set_web_authentication_detail()
        self.__set_client_detail()
        self.__set_version_id()
        self.__set_carrier_code_type(*args, **kwargs)
        self.__set_transaction_detail(*args, **kwargs)
        
    def __set_web_authentication_detail(self):
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
        
    def __set_client_detail(self):
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
        
    def __set_transaction_detail(self, *args, **kwargs):
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
            
    def __set_carrier_code_type(self, *args, **kwargs):
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
    
    def __set_version_id(self):
        """
        Pulles the versioning info for the request from the child request.
        """
        VersionId = self.client.factory.create('VersionId')
        VersionId.ServiceId = self._version_info['service_id']
        VersionId.Major = self._version_info['major']
        VersionId.Intermediate = self._version_info['intermediate']
        VersionId.Minor = self._version_info['minor']
        self.logger.debug(VersionId)
        self.VersionId = VersionId
        
    def __check_response_for_fedex_error(self):
        """
        This checks the response for general Fedex errors that aren't related
        to any one WSDL.
        """
        if self.response.HighestSeverity == "FAILURE":
            raise FedexFailure()
        
    def send_request(self):
        """
        Sends the assembled request on the child object.
        """
        self.response = self._assemble_and_send_request()
        self.__check_response_for_fedex_error()
        self.logger.info("== FEDEX QUERY RESULT ==")
        self.logger.info(self.response)