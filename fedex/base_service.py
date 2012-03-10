"""
The L{base_service} module contains classes that form the low level foundations
of the Web Service API. Things that many different kinds of requests have in
common may be found here.

In particular, the L{FedexBaseService} class handles most of the basic,
repetetive setup work that most requests do.
"""
import os
import logging
import suds
from suds.client import Client

class FedexBaseServiceException(Exception):
    """
    Exception: Serves as the base exception that other service-related
    exception objects are sub-classed from.
    """
    def __init__(self, error_code, value):
        self.error_code = error_code
        self.value = value
    def __unicode__(self):
        return "%s (Error code: %s)" % (repr(self.value), self.error_code)
    def __str__(self):
        return self.__unicode__()

class FedexFailure(FedexBaseServiceException):
    """
    Exception: The request could not be handled at this time. This is generally
    a server problem.
    """
    pass

class FedexError(FedexBaseServiceException):
    """
    Exception: These are generally problems with the client-provided data.
    """
    pass

class SchemaValidationError(FedexBaseServiceException):
    """
    Exception: There is probably a problem in the data you provided.
    """
    def __init__(self):
        self.error_code = -1
        self.value = "suds encountered an error validating your data against this service's WSDL schema. Please double-check for missing or invalid values, filling all required fields."

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
        """
        self.logger = logging.getLogger('fedex')
        """@ivar: Python logger instance with name 'fedex'."""
        self.config_obj = config_obj
        """@ivar: The FedexConfig object to pull auth info from."""

        # If the config object is set to use the test server, point
        # suds at the test server WSDL directory.
        if config_obj.use_test_server:
            self.logger.info("Using test server.")
            self.wsdl_path = os.path.join(config_obj.wsdl_path,
                                          'test_server_wsdl', wsdl_name)
        else:
            self.logger.info("Using production server.")
            self.wsdl_path = os.path.join(config_obj.wsdl_path, wsdl_name)

        self.client = Client('file:///%s' % self.wsdl_path.lstrip('/'))

        #print self.client

        self.VersionId = None
        """@ivar: Holds details on the version numbers of the WSDL."""
        self.WebAuthenticationDetail = None
        """@ivar: WSDL object that holds authentication info."""
        self.ClientDetail = None
        """@ivar: WSDL object that holds client account details."""
        self.response = None
        """@ivar: The response from Fedex. You will want to pick what you
            want out here here. This object does have a __str__() method,
            you'll want to print or log it to see what possible values
            you can pull."""
        self.TransactionDetail = None
        """@ivar: Holds customer-specified transaction IDs."""

        self.__set_web_authentication_detail()
        self.__set_client_detail()
        self.__set_version_id()
        self.__set_transaction_detail(*args, **kwargs)
        self._prepare_wsdl_objects()

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
        if hasattr(ClientDetail, 'Region'):
            ClientDetail.Region = self.config_obj.express_region_code
        self.ClientDetail = ClientDetail

    def __set_transaction_detail(self, *args, **kwargs):
        """
        Checks kwargs for 'customer_transaction_id' and sets it if present.
        """
        customer_transaction_id = kwargs.get('customer_transaction_id', False)
        if customer_transaction_id:
            TransactionDetail = self.client.factory.create('TransactionDetail')
            TransactionDetail.CustomerTransactionId = customer_transaction_id
            self.logger.debug(TransactionDetail)
            self.TransactionDetail = TransactionDetail

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

    def __prepare_wsdl_objects(self):
        """
        This method should be over-ridden on each sub-class. It instantiates
        any of the required WSDL objects so the user can just print their
        __str__() methods and see what they need to fill in.
        """
        pass

    def __check_response_for_fedex_error(self):
        """
        This checks the response for general Fedex errors that aren't related
        to any one WSDL.
        """
        if self.response.HighestSeverity == "FAILURE":
            for notification in self.response.Notifications:
                if notification.Severity == "FAILURE":
                    raise FedexFailure(notification.Code,
                                       notification.Message)

    def _check_response_for_request_errors(self):
        """
        Override this in each service module to check for errors that are
        specific to that module. For example, invalid tracking numbers in
        a Tracking request.
        """
        if self.response.HighestSeverity == "ERROR":
            for notification in self.response.Notifications:
                if notification.Severity == "ERROR":
                    raise FedexError(notification.Code,
                                     notification.Message)

    def create_wsdl_object_of_type(self, type_name):
        """
        Creates and returns a WSDL object of the specified type.
        """
        return self.client.factory.create(type_name)

    def send_request(self, send_function=None):
        """
        Sends the assembled request on the child object.
        @type send_function: function reference
        @keyword send_function: A function reference (passed without the
            parenthesis) to a function that will send the request. This
            allows for overriding the default function in cases such as
            validation requests.
        """
        # Send the request and get the response back.
        try:
            # If the user has overridden the send function, use theirs
            # instead of the default.
            if send_function:
                # Follow the overridden function.
                self.response = send_function()
            else:
                # Default scenario, business as usual.
                self.response = self._assemble_and_send_request()
        except suds.WebFault:
            # When this happens, throw an informative message reminding the
            # user to check all required variables, making sure they are
            # populated and valid.
            raise SchemaValidationError()

        # Check the response for general Fedex errors/failures that aren't
        # specific to any given WSDL/request.
        self.__check_response_for_fedex_error()
        # Check the response for errors specific to the particular request.
        # This is handled by an overridden method on the child object.
        self._check_response_for_request_errors()

        # Debug output.
        self.logger.debug("== FEDEX QUERY RESULT ==")
        self.logger.debug(self.response)
