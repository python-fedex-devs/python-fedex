"""
Document Service Module

This package contains the shipping methods defined by Fedex's
DocumentService WSDL file. Each is encapsulated in a class for
easy access. For more details on each, refer to the respective class's
documentation.
"""

import datetime
from ..base_service import FedexBaseService


class FedexDocumentServiceRequest(FedexBaseService):
        """
        This class allows you to submit the document.
        You will need to populate the data structures in self.UploadDocumentsRequest,
        then send the request.
        """

        def __init__(self, config_obj, *args, **kwargs):
            """
            The optional keyword args detailed on L{FedexBaseService}
            apply here as well.
            @type config_obj: L{FedexConfig}
            @param config_obj: A valid FedexConfig object.
            """

            self._config_obj = config_obj

            # Holds version info for the VersionId SOAP object.
            self._version_info = {'service_id': 'cdus', 'major': '11',
                                  'intermediate': '0', 'minor': '0'}

            self.UploadDocumentsRequest = None
            """@ivar: Holds the UploadDocumentsRequest WSDL object including the shipper, recipient and shipt time."""
            super(FedexDocumentServiceRequest, self).__init__(
                    self._config_obj, 'UploadDocumentService_v11.wsdl', *args, **kwargs)
            """@ivar: Holds the express region code from the config object."""

        def _prepare_wsdl_objects(self):
            """
            This is the data that will be used to create your shipment. Create
            the data structure and get it ready for the WSDL request.
            """
            self.UploadDocumentsRequest = self.client.factory.create('UploadDocumentsRequest')
            self.OriginCountryCode  =None
            self.DestinationCountryCode  =None
            self.Usage  ='ELECTRONIC_TRADE_DOCUMENTS'#Default Usage
            self.Documents = []
            self.UploadDocumentsRequest.Documents = []
            self.logger.debug(self.UploadDocumentsRequest)

        def _assemble_and_send_request(self):
            """
            Fires off the Fedex request.

            @warning: NEVER CALL THIS METHOD DIRECTLY. CALL send_request(),
                WHICH RESIDES ON FedexBaseService AND IS INHERITED.
            """

            # Fire off the query.
            return self.client.service.uploadDocuments(
                    WebAuthenticationDetail=self.WebAuthenticationDetail,
                    ClientDetail=self.ClientDetail,
                    TransactionDetail=self.TransactionDetail,
                    Version=self.VersionId,
                    Documents=self.Documents,
                    Usage = self.Usage,
                    OriginCountryCode = self.OriginCountryCode,
                    DestinationCountryCode = self.DestinationCountryCode,
                )
        def get_document(self, line_number,customer_reference,
            document_type , file_name, document_content, expiration_date =None
            ):
            document_item = self.client.factory.create('UploadDocumentDetail')
            document_item.LineNumber = line_number
            document_item.CustomerReference = customer_reference
            document_item.DocumentType = document_type
            document_item.FileName = file_name
            document_item.DocumentContent = document_content
            document_item.ExpirationDate = expiration_date
            return document_item
        def add_documents(self, document_item):
            self.Documents.append(document_item)
