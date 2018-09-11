"""
Country Service Module

This package contains the shipping methods defined by Fedex's 
CountryService WSDL file. Each is encapsulated in a class for
easy access. For more details on each, refer to the respective class's 
documentation.
"""

import datetime
from ..base_service import FedexBaseService


class FedexValidatePostalRequest(FedexBaseService):
    """
    This class allows you validate an address.
    https://www.fedex.com/us/developer/WebHelp/ws/2015/html/WebServicesHelp/WSDVG/47_Country_Service.htm
    """

    def __init__(self, config_obj, *args, **kwargs):
        """
        @type config_obj: L{FedexConfig}
        @param config_obj: A valid FedexConfig object.        
        """

        self._config_obj = config_obj
        # Holds version info for the VersionId SOAP object.
        self._version_info = {
            'service_id': 'cnty',
            'major': '8',
            'intermediate': '0',
            'minor': '0'
        }

        self.CarrierCode = None
        """@ivar: Carrier Code Default to Fedex (FDXE), or can bbe FDXG."""

        self.RoutingCode = None
        """@ivar: Routing Code Default to FDSD."""

        self.Address = None
        """@ivar: Holds Address WSDL objects."""

        self.ShipDateTime = None
        """@ivar: Holds the ShipDateTime date time objects."""

        self.CheckForMismatch = 1
        """@ivar: Holds the CheckForMismatch boolean objects."""

        super(FedexValidatePostalRequest, self).__init__(
                self._config_obj, 'CountryService_v8.wsdl', *args, **kwargs)

    def _prepare_wsdl_objects(self):
        """
        Create the data structure and get it ready for the WSDL request.
        """
        self.CarrierCode = 'FDXE'
        self.RoutingCode = 'FDSD'
        self.Address = self.client.factory.create('Address')
        self.ShipDateTime = datetime.datetime.now().isoformat()

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
        return self.client.service.validatePostal(
                WebAuthenticationDetail=self.WebAuthenticationDetail,
                ClientDetail=self.ClientDetail,
                TransactionDetail=self.TransactionDetail,
                Version=self.VersionId,
                Address=self.Address,
                ShipDateTime=self.ShipDateTime,
                CarrierCode=self.CarrierCode,
                CheckForMismatch=self.CheckForMismatch,
                RoutingCode=self.RoutingCode)
