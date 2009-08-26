"""
Ship Service Module
===================
This package contains the shipping and tracking methods defined by Fedex's 
ShipService WSDL file. Each is encapsulated in a class for easy access. 
For more details on each, refer to the respective class's documentation.
"""
from .. base_service import FedexBaseService

class FedexTrackRequest(FedexBaseService):
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
        self._version_info = {'service_id': 'trck', 'major': '4', 
                             'intermediate': '0', 'minor': '0'}
        # Call the parent FedexBaseService class for basic setup work.
        super(FedexTrackRequest, self).__init__(self._config_obj, 
                                                'TrackService_v4.wsdl',
                                                *args, **kwargs)

        # Important request-specific instance variables.
        self.package_identifier = package_identifier
        """@ivar: Determines what L{tracking_value} is, be it a tracking number,
            purchase order, or other things."""
        self.tracking_value = tracking_value
        """@ivar: This is typically a Fedex tracking number, but setting 
            L{package_identifier} to other values makes this change."""
        
    def __set_track_package_identifier(self):
        """
        This sets the package identifier information. This may be a tracking
        number or a few different things as per the Fedex spec.
        """
        TrackPackageIdentifier = self.client.factory.create('TrackPackageIdentifier')
        TrackPackageIdentifier.Type = self.package_identifier
        TrackPackageIdentifier.Value = self.tracking_value
        self.logger.debug(TrackPackageIdentifier)
        self.TrackPackageIdentifier = TrackPackageIdentifier
        
    def _assemble_and_send_request(self):
        """
        Fires off the Fedex request.
        
        @warning: NEVER CALL THIS METHOD DIRECTLY. CALL send_request(), WHICH RESIDES
            ON FedexBaseService AND IS INHERITED.
        """
        self.__set_track_package_identifier()
        client = self.client
        # Fire off the query.
        response = client.service.track(WebAuthenticationDetail=self.WebAuthenticationDetail,
                                        ClientDetail=self.ClientDetail,
                                        TransactionDetail=self.TransactionDetail,
                                        Version=self.VersionId,
                                        CarrierCodeType=self.CarrierCodeType,
                                        PackageIdentifier=self.TrackPackageIdentifier)
        return response