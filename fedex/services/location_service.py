"""
Location Service Module
=================================
This package contains the shipping methods defined by Fedex's 
LocationService WSDL file. Each is encapsulated in a class for
easy access. For more details on each, refer to the respective class's 
documentation.
"""

from ..base_service import FedexBaseService


class FedexSearchLocationRequest(FedexBaseService):
    """
    This class allows you to figure out a FedEx location closest
    to a specified location, based on location type. The response includes
    location details like operating times, directions and a map link.
    """

    def __init__(self, config_obj, *args, **kwargs):
        """
        @type config_obj: L{FedexConfig}
        @param config_obj: A valid FedexConfig object.        
        """

        self._config_obj = config_obj
        # Holds version info for the VersionId SOAP object.
        self._version_info = {
            'service_id': 'locs',
            'major': '3',
            'intermediate': '0',
            'minor': '0'
        }

        """@ivar: set default objects."""
        self.Address = None
        self.PhoneNumber = None
        self.MultipleMatchesAction = None
        self.Constraints = []
        self.LocationsSearchCriterion = None

        """@ivar: Holds the WSDL object."""

        super(FedexSearchLocationRequest, self).__init__(
            self._config_obj, 'LocationsService_v3.wsdl', *args, **kwargs)

    def _prepare_wsdl_objects(self):
        """
        Create the data structure and get it ready for the WSDL request.
        """
        self.MultipleMatchesAction = 'RETURN_ALL'
        self.Constraints = self.create_wsdl_object_of_type('SearchLocationConstraints')
        self.Address = self.create_wsdl_object_of_type('Address')

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
        return self.client.service.searchLocations(
            WebAuthenticationDetail=self.WebAuthenticationDetail,
            ClientDetail=self.ClientDetail,
            TransactionDetail=self.TransactionDetail,
            Version=self.VersionId,
            LocationsSearchCriterion=self.LocationsSearchCriterion,
            PhoneNumber=self.PhoneNumber,
            MultipleMatchesAction=self.MultipleMatchesAction,
            Constraints=self.Constraints,
            Address=self.Address)
