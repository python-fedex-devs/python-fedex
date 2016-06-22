from fedex.base_service import FedexBaseService


class FedexCreatePickupRequest(FedexBaseService):

    def __init__(self, config_obj, *args, **kwargs):
        self._config_obj = config_obj
        # Holds version info for the VersionId SOAP object.
        self._version_info = {
            'service_id': 'disp',
            'major': '11',
            'intermediate': '0',
            'minor': '0'
        }
        self.OriginDetail = None
        self.PackageCount = None
        self.TotalWeight = None
        self.CarrierCode = None
        self.OversizePackageCount = None
        self.Remarks = None
        self.CommodityDescription = None
        self.CountryRelationship = None
        self.PickupServiceCategory = None
        super(FedexCreatePickupRequest, self).__init__(self._config_obj, 'PickupService_v11.wsdl', *args, **kwargs)

    def _prepare_wsdl_objects(self):
        self.OriginDetail = self.client.factory.create('PickupOriginDetail')

        self.OriginDetail.PickupLocation = self.client.factory.create('ContactAndAddress')
        self.OriginDetail.PickupLocation.Contact = self.client.factory.create('Contact')
        self.OriginDetail.PickupLocation.Address = self.client.factory.create('Address')
        self.OriginDetail.PackageLocation = None
        self.OriginDetail.BuildingPart = None

        self.TotalWeight = self.client.factory.create('Weight')

        self.CarrierCode = self.client.factory.create('CarrierCodeType')

        self.logger.debug(self.OriginDetail)
        self.logger.debug(self.TotalWeight)
        self.logger.debug(self.CarrierCode)

    def _assemble_and_send_request(self):
        """
        Fires off the Fedex request.

        @warning: NEVER CALL THIS METHOD DIRECTLY. CALL send_request(),
            WHICH RESIDES ON FedexBaseService AND IS INHERITED.
        """

        # Fire off the query.
        return self.client.service.createPickup(
            WebAuthenticationDetail=self.WebAuthenticationDetail,
            ClientDetail=self.ClientDetail,
            TransactionDetail=self.TransactionDetail,
            Version=self.VersionId,
            OriginDetail=self.OriginDetail,
            PickupServiceCategory=self.PickupServiceCategory,
            PackageCount=self.PackageCount,
            TotalWeight=self.TotalWeight,
            CarrierCode=self.CarrierCode,
            OversizePackageCount=self.OversizePackageCount,
            Remarks=self.Remarks,
            CommodityDescription=self.CommodityDescription,
            CountryRelationship=self.CountryRelationship
        )

