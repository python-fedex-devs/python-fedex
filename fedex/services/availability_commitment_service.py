"""
Service Availability and Commitment Module

This package contains the shipping methods defined by Fedex's 
ValidationAvailabilityAndCommitmentService WSDL file. Each is encapsulated in a class for
easy access. For more details on each, refer to the respective class's 
documentation.
"""

import datetime
from ..base_service import FedexBaseService


class FedexAvailabilityCommitmentRequest(FedexBaseService):
    """
    This class allows you validate service availability
    """

    def __init__(self, config_obj, *args, **kwargs):
        """
        @type config_obj: L{FedexConfig}
        @param config_obj: A valid FedexConfig object.        
        """

        self._config_obj = config_obj
        # Holds version info for the VersionId SOAP object.
        self._version_info = {
            'service_id': 'vacs',
            'major': '8',
            'intermediate': '0',
            'minor': '0'
        }

        self.CarrierCode = None
        """@ivar: Carrier Code Default to Fedex (FDXE), or can bbe FDXG."""

        self.Origin = None
        """@ivar: Holds Origin Address WSDL object."""

        self.Destination = None
        """@ivar: Holds Destination Address WSDL object."""

        self.ShipDate = None
        """@ivar: Ship Date date WSDL object."""

        self.Service = None
        """@ivar: Service type, if set to None will get all available service information."""

        self.Packaging = None
        """@ivar: Type of packaging to narrow down available shipping options or defaults to YOUR_PACKAGING."""

        # Call the parent FedexBaseService class for basic setup work.
        # Shortened the name of the wsdl, otherwise suds did not load it properly.
        # Suds throws the following error when using the long file name from FedEx:
        #
        # File "/Library/Python/2.7/site-packages/suds/wsdl.py", line 878, in resolve
        # raise Exception("binding '%s', not-found" % p.binding)
        # Exception: binding 'ns:ValidationAvailabilityAndCommitmentServiceSoapBinding', not-found

        super(FedexAvailabilityCommitmentRequest, self).__init__(
                self._config_obj, 'ValidationAvailabilityAndCommitmentService_v8.wsdl', *args, **kwargs)

    def _prepare_wsdl_objects(self):
        """
        Create the data structure and get it ready for the WSDL request.
        """
        self.CarrierCode = 'FDXE'
        self.Origin = self.client.factory.create('Address')
        self.Destination = self.client.factory.create('Address')
        self.ShipDate = datetime.date.today().isoformat()
        self.Service = None
        self.Packaging = 'YOUR_PACKAGING'

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
        return self.client.service.serviceAvailability(
                WebAuthenticationDetail=self.WebAuthenticationDetail,
                ClientDetail=self.ClientDetail,
                TransactionDetail=self.TransactionDetail,
                Version=self.VersionId,
                Origin=self.Origin,
                Destination=self.Destination,
                ShipDate=self.ShipDate,
                CarrierCode=self.CarrierCode,
                Service=self.Service,
                Packaging=self.Packaging)
