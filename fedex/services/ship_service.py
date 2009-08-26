from .. base_service import FedexBaseService

class FedexTrackRequest(FedexBaseService):
    def __init__(self, config_obj, tracking_value,
                 package_identifier='TRACKING_NUMBER_OR_DOORTAG',
                 *args, **kwargs):
        """
        Sends a shipment tracking request.
        
        package_identifier: (str) Determines what you are using to query for
                                  the shipment. The default assumes that
                                  tracking_value will be a Fedex tracking #.
        tracking_value: (str) Based on the value of package_identifier, this
                              will be anything from a tracking number to 
                              a purchase order number.
        """
        self.config_obj = config_obj
        # Holds version info for the VersionId SOAP object.
        self.version_info = {'service_id': 'trck', 'major': '4', 
                             'intermediate': '0', 'minor': '0'}
        # Call the parent FedexBaseService class for basic setup work.
        super(FedexTrackRequest, self).__init__(config_obj, 
                                                'TrackService_v4.wsdl',
                                                *args, **kwargs)
        # Start preparing the Fedex-specific things.
        self.tracking_value = tracking_value
        self.package_identifier = package_identifier
        self.set_track_package_identifier()
        
    def set_track_package_identifier(self):
        """
        This sets the package identifier information. This may be a tracking
        number or a few different things as per the Fedex spec.
        """
        TrackPackageIdentifier = self.client.factory.create('TrackPackageIdentifier')
        TrackPackageIdentifier.Type = self.package_identifier
        TrackPackageIdentifier.Value = self.tracking_value
        self.logger.debug(TrackPackageIdentifier)
        self.TrackPackageIdentifier = TrackPackageIdentifier
        
    def assemble_and_send_request(self):
        """
        Fires off the Fedex request.
        NEVER CALL THIS METHOD DIRECTLY. CALL SEND_REQUEST(), WHICH RESIDES
        ON FedexBaseService AND IS INHERITED.
        """
        client = self.client
        # Fire off the query.
        response = client.service.track(WebAuthenticationDetail=self.WebAuthenticationDetail,
                                        ClientDetail=self.ClientDetail,
                                        TransactionDetail=self.TransactionDetail,
                                        Version=self.VersionId,
                                        CarrierCodeType=self.CarrierCodeType,
                                        PackageIdentifier=self.TrackPackageIdentifier)
        return response