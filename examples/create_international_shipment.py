"""
This example shows how to create an international shipment and generate a waybill as output.
The example takes outset in a real practical use case, where electronic trade documents are
used and an existing PDF commercial invoice is added along with product descriptions via ETD.
Further, it adds event notifications to allow for emails to be sent to the end recipient.

The script is comprised of a FedExLabelHelper class with all core functions, and a use case
example with minimal dummy data
"""
from example_config import CONFIG_OBJ
from pathlib import Path
import binascii
import datetime
from fedex.services.ship_service import FedexProcessShipmentRequest

# ----------------------------------------------------
# FedEx class for creating shipments
class FedexLabelHelper:
    mCommodities = []

    def __init__(self):
        pass

    # ----------------------------------------------------
    # set overall shipment configuration
    def setShipmentConfig(
        self,
        CONFIG_OBJ,
        invoice_info,
        cust_tran_id="*** ShipService Request v17 using Python ***",
        dropoffType="BUSINESS_SERVICE_CENTER",
        shippingPaymentType="SENDER",
        labelFormatType="COMMON2D",
        labelSpecificationImageType="PDF",
        labelSpecificationStockType="PAPER_7X4.75",
        labelPrintingOrientation="TOP_EDGE_OF_TEXT_FIRST",
        LabelOrder="SHIPPING_LABEL_FIRST",
    ):
        self.invoice_info = invoice_info
        self.dropoffType = dropoffType
        self.serviceType = "INTERNATIONAL_PRIORITY" if invoice_info["ShippingExpress"] == True else "INTERNATIONAL_ECONOMY"
        self.mCommodities.clear()
        self.CONFIG_OBJ = CONFIG_OBJ
        self.shipment = FedexProcessShipmentRequest(CONFIG_OBJ, customer_transaction_id=cust_tran_id)

        self.shipment.RequestedShipment.DropoffType = dropoffType
        self.shipment.RequestedShipment.ServiceType = self.serviceType
        self.shipment.RequestedShipment.ShippingChargesPayment.Payor.ResponsibleParty.AccountNumber = CONFIG_OBJ.account_number
        self.shipment.RequestedShipment.ShippingChargesPayment.Payor.ResponsibleParty.Address.CountryCode = "DK"
        self.shipment.RequestedShipment.ShippingChargesPayment.PaymentType = shippingPaymentType

        labelSpecification = self.shipment.create_wsdl_object_of_type("LabelSpecification")
        labelSpecification.LabelFormatType = labelFormatType
        labelSpecification.LabelStockType = labelSpecificationStockType
        labelSpecification.ImageType = labelSpecificationImageType
        labelSpecification.LabelOrder = LabelOrder
        labelSpecification.LabelPrintingOrientation = labelPrintingOrientation
        self.shipment.RequestedShipment.LabelSpecification = labelSpecification

    # ----------------------------------------------------
    # set sender information
    def setSenderInfo(self, sender):

        self.shipment.RequestedShipment.Shipper.Contact.PersonName = sender["Name"]
        self.shipment.RequestedShipment.Shipper.Contact.CompanyName = sender["Company"]
        self.shipment.RequestedShipment.Shipper.Contact.PhoneNumber = sender["Phone"]
        self.shipment.RequestedShipment.Shipper.Contact.EMailAddress = sender["Email"]
        self.shipment.RequestedShipment.Shipper.Address.StreetLines = sender["Address"]
        self.shipment.RequestedShipment.Shipper.Address.City = sender["City"]
        self.shipment.RequestedShipment.Shipper.Address.StateOrProvinceCode = sender["Region"]
        self.shipment.RequestedShipment.Shipper.Address.PostalCode = sender["Zip"]
        self.shipment.RequestedShipment.Shipper.Address.CountryCode = sender["CountryCode"]
        self.shipment.RequestedShipment.Shipper.Address.Residential = sender["Residential"]

        ti = self.shipment.create_wsdl_object_of_type("TaxpayerIdentification")
        ti.Number = sender["VAT"]
        ti.TinType = "BUSINESS_NATIONAL"
        self.shipment.RequestedShipment.Shipper.Tins = ti

    # ----------------------------------------------------
    # upload all documents (invoice and product information)
    def upload_all_documents(self):
        doc_ids = []
        doc_ids.append(self.upload_document(self.invoice_info["InvoicePath"], "COMMERCIAL_INVOICE"))

        for pdf in self.invoice_info["Pdfs"]:
            doc_ids.append(self.upload_document(pdf, "OTHER"))

        return doc_ids

    # ----------------------------------------------------
    # function for uploading documents as electronic trade documents and getting the response doc IDs
    def upload_document(self, path, type):
        from fedex.services.document_service import FedexDocumentServiceRequest

        # specify prefix for use in attachment naming
        if type == "COMMERCIAL_INVOICE":
            prefix = "invoice_"
        else:
            prefix = "product_description_"

        uploadRequest = FedexDocumentServiceRequest(self.CONFIG_OBJ)
        uploadRequest.OriginCountryCode = "DK"
        uploadRequest.DestinationCountryCode = self.shipment.RequestedShipment.Recipient.Address.CountryCode
        uploadRequest.Usage = "ELECTRONIC_TRADE_DOCUMENTS"

        clientdetails = uploadRequest.create_wsdl_object_of_type("ClientDetail")
        clientdetails.AccountNumber = self.CONFIG_OBJ.account_number
        clientdetails.MeterNumber = self.CONFIG_OBJ.meter_number
        uploadRequest.ClientDetail = clientdetails

        webAuthDetails = uploadRequest.create_wsdl_object_of_type("WebAuthenticationDetail")
        webAuthDetails.ParentCredential.Key = self.CONFIG_OBJ.key
        webAuthDetails.ParentCredential.Password = self.CONFIG_OBJ.password
        webAuthDetails.UserCredential.Key = self.CONFIG_OBJ.key
        webAuthDetails.UserCredential.Password = self.CONFIG_OBJ.password
        uploadRequest.WebAuthenticationDetail = webAuthDetails

        docdetails = uploadRequest.create_wsdl_object_of_type("UploadDocumentDetail")
        docdetails.LineNumber = 1
        docdetails.DocumentType = type
        docdetails.FileName = prefix + path
        fileContent = open(path, "rb").read()
        fileBase64 = binascii.b2a_base64(fileContent)
        docdetails.DocumentContent = fileBase64.decode("cp1250")
        uploadRequest.Documents = docdetails

        uploadRequest.send_request()

        doc_id = uploadRequest.response.DocumentStatuses[0].DocumentId

        return doc_id

    # ----------------------------------------------------
    # set recipient information
    def setRecipientInfo(self, recipient):
        self.shipment.RequestedShipment.Recipient.Contact.PersonName = recipient["Name"]
        self.shipment.RequestedShipment.Recipient.Contact.CompanyName = recipient["Company"]
        self.shipment.RequestedShipment.Recipient.Contact.PhoneNumber = recipient["Phone"]
        self.shipment.RequestedShipment.Recipient.Contact.EMailAddress = recipient["Email"]
        self.shipment.RequestedShipment.Recipient.Address.StreetLines = recipient["Address"]
        self.shipment.RequestedShipment.Recipient.Address.City = recipient["City"]
        self.shipment.RequestedShipment.Recipient.Address.StateOrProvinceCode = recipient["Region"]
        self.shipment.RequestedShipment.Recipient.Address.PostalCode = recipient["Zip"]
        self.shipment.RequestedShipment.Recipient.Address.CountryCode = recipient["CountryCode"]
        self.shipment.RequestedShipment.Recipient.Address.Residential = recipient["Residential"]

        ti = self.shipment.create_wsdl_object_of_type("TaxpayerIdentification")
        ti.Number = recipient["VAT"]
        ti.TinType = "BUSINESS_NATIONAL"
        self.shipment.RequestedShipment.Recipient.Tins = ti

    # ----------------------------------------------------
    # add "commercial invoice" reference as the only commodity
    def add_ci_commodity(self):

        self.addCommodity(
            cCustomsValueAmnt=self.invoice_info["Value"],
            cCustomsValueCurrency=self.invoice_info["Currency"],
            cWeightValue=self.invoice_info["Weight"],
            cDescription="See attached commercial invoice",
            cQuantity=self.invoice_info["Quantity"],
            cExportLicenseNumber=self.shipment.RequestedShipment.Shipper.Tins.Number,
            cPartNumber=1,
        )

    # ----------------------------------------------------
    # add commodity to shipment (for now, just add 1 commodity to refer to attached CI)
    def addCommodity(
        self, cCustomsValueAmnt, cCustomsValueCurrency, cWeightValue, cDescription, cQuantity, cExportLicenseNumber, cPartNumber,
    ):

        commodity = self.shipment.create_wsdl_object_of_type("Commodity")
        commodity.NumberOfPieces = str(cQuantity)
        commodity.Description = cDescription
        commodity.Quantity = cQuantity
        commodity.QuantityUnits = "EA"
        commodity.ExportLicenseNumber = cExportLicenseNumber
        commodity.PartNumber = cPartNumber
        commodity.CountryOfManufacture = "DK"

        mCustomsValue = self.shipment.create_wsdl_object_of_type("Money")
        mCustomsValue.Amount = cCustomsValueAmnt
        mCustomsValue.Currency = cCustomsValueCurrency
        commodity.CustomsValue = mCustomsValue

        commodity_weight = self.shipment.create_wsdl_object_of_type("Weight")
        commodity_weight.Value = cWeightValue
        commodity_weight.Units = "KG"
        commodity.Weight = commodity_weight

        munitPrice = self.shipment.create_wsdl_object_of_type("Money")
        munitPrice.Amount = float(round((cCustomsValueAmnt / cQuantity), 2))
        munitPrice.Currency = cCustomsValueCurrency
        commodity.UnitPrice = munitPrice

        self.mCommodities.append(commodity)

    # ----------------------------------------------------
    # add package to shipment
    def set_packaging_info(self):
        weight = self.invoice_info["Weight"]

        type = "BOX" if weight > 0.5 else "ENVELOPE"
        weight_final = float(round(weight + 0.2, 2)) if weight > 0.5 else 0.4

        self.addShippingPackage(packageWeight=weight_final, physicalPackagingType=type, packagingType=f"FEDEX_{type}")

    # ----------------------------------------------------
    # add package to shipment
    def addShippingPackage(self, packageWeight, physicalPackagingType, packagingType, packageWeightUnit="KG"):
        package_weight = self.shipment.create_wsdl_object_of_type("Weight")
        package_weight.Value = packageWeight
        package_weight.Units = packageWeightUnit

        package = self.shipment.create_wsdl_object_of_type("RequestedPackageLineItem")
        package.PhysicalPackaging = physicalPackagingType
        package.Weight = package_weight

        self.shipment.add_package(package)
        self.shipment.RequestedShipment.TotalWeight = package_weight
        self.shipment.RequestedShipment.PackagingType = packagingType

    # ----------------------------------------------------
    # add information on duties
    def setDutiesPaymentInfo(self):
        mParty = self.shipment.create_wsdl_object_of_type("Party")
        mParty.AccountNumber = self.CONFIG_OBJ.account_number
        mParty.Address = self.shipment.RequestedShipment.Recipient.Address

        mPayor = self.shipment.create_wsdl_object_of_type("Payor")
        mPayor.ResponsibleParty = mParty

        mPayment = self.shipment.create_wsdl_object_of_type("Payment")
        mPayment.PaymentType = "RECIPIENT"  # change if sender should pay duties
        mPayment.Payor = mPayor

        mCustomsValue = self.shipment.create_wsdl_object_of_type("Money")
        mCustomsValue.Amount = self.invoice_info["Value"]
        mCustomsValue.Currency = self.invoice_info["Currency"]

        ccd = self.shipment.create_wsdl_object_of_type("CustomsClearanceDetail")
        ccd.Commodities = self.mCommodities
        ccd.CustomsValue = mCustomsValue
        ccd.DutiesPayment = mPayment
        self.shipment.RequestedShipment.CustomsClearanceDetail = ccd

    # ----------------------------------------------------
    # Set ETD (electronic trade documents) settings
    def setSpecialServices(self, doc_ids):
        # construct objects
        ssr = self.shipment.create_wsdl_object_of_type("ShipmentSpecialServicesRequested")
        ssr.SpecialServiceTypes.append("ELECTRONIC_TRADE_DOCUMENTS")
        ssr.SpecialServiceTypes.append("EVENT_NOTIFICATION")

        # set up ETD details
        etd = self.shipment.create_wsdl_object_of_type("EtdDetail")
        etd.RequestedDocumentCopies = "COMMERCIAL INVOICE"

        for i, doc_id in enumerate(doc_ids, start=0):
            udrd = self.shipment.create_wsdl_object_of_type("UploadDocumentReferenceDetail")
            udrd.DocumentType = "COMMERCIAL_INVOICE" if i == 0 else "OTHER"
            udrd.DocumentId = doc_id
            udrd.Description = "Commercial_Invoice" if i == 0 else "Product_Description"
            udrd.DocumentIdProducer = "CUSTOMER"
            ssr.EtdDetail.DocumentReferences.append(udrd)

        self.shipment.RequestedShipment.SpecialServicesRequested = ssr

        # set Event Notification details
        send = self.shipment.create_wsdl_object_of_type("ShipmentEventNotificationDetail")
        send.AggregationType = "PER_SHIPMENT"

        sens = self.shipment.create_wsdl_object_of_type("ShipmentEventNotificationSpecification")
        sens.NotificationDetail.NotificationType = "EMAIL"
        sens.NotificationDetail.EmailDetail.EmailAddress = self.shipment.RequestedShipment.Recipient.Contact.EMailAddress
        sens.NotificationDetail.EmailDetail.Name = self.shipment.RequestedShipment.Recipient.Contact.PersonName
        sens.NotificationDetail.Localization.LanguageCode = "EN"
        sens.Role = "SHIPPER"
        sens.Events.append("ON_SHIPMENT")
        sens.Events.append("ON_EXCEPTION")
        sens.Events.append("ON_DELIVERY")
        sens.FormatSpecification.Type = "HTML"
        send.EventNotifications = sens
        self.shipment.RequestedShipment.SpecialServicesRequested.EventNotificationDetail = send

    # ----------------------------------------------------
    # process the shipment
    def processInternationalShipment(self):
        from shutil import copyfile

        self.shipment.RequestedShipment.ShipTimestamp = datetime.datetime.now().replace(microsecond=0).isoformat()

        # print(" ---- **** DETAILS ---- ****")
        # print(self.shipment.RequestedShipment)
        # print(self.shipment.ClientDetail)
        # print(self.shipment.TransactionDetail)
        # print("REQUESTED SHIPMENT\n\n", self.shipment.RequestedShipment)

        self.shipment.send_request()

        # print("RESPONSE\n\n", self.shipment.response)

        status = self.shipment.response.HighestSeverity

        if status == "SUCCESS" and "CompletedShipmentDetail" in self.shipment.response:
            shipment_details = self.shipment.response.CompletedShipmentDetail
            package_details = shipment_details.CompletedPackageDetails[0]
            tracking_id = package_details.TrackingIds[0].TrackingNumber
            email = self.shipment.RequestedShipment.Recipient.Contact.EMailAddress
            fedex_cost = "N/A"

            if hasattr(package_details, "PackageRating"):
                fedex_cost = package_details.PackageRating.PackageRateDetails[0].NetCharge.Amount

            # create the shipping PDF label
            ascii_label_data = package_details.Label.Parts[0].Image
            label_binary_data = binascii.a2b_base64(ascii_label_data)
            out_path = self.invoice_info["InvoiceId"] + f"_shipment_label_{tracking_id}.pdf"

            out_file = open(out_path, "wb")
            out_file.write(label_binary_data)
            out_file.close()

            # print output information
            print(
                f"- SUCCESS: Created FedEx label for invoice {self.invoice_info['InvoiceId']}\n     tracking ID: {tracking_id}\n     email: {email}\n     FedEx cost: {fedex_cost}\n     Customs value: {self.invoice_info['Value']} {self.invoice_info['Currency']}\n     Weight: {self.invoice_info['Weight']}\n     output path: {out_path}"
            )


# ----------------------------------------------------
# main script
commercial_invoice_path = "commercial_invoice_test.pdf"
product_description_1_path = "product_description_test.pdf"

sender = {
    "Company": "Sender Company",
    "Name": "Mr Smith",
    "Address": ["Address 1", "Address 2"],
    "Region": "",
    "Zip": "8230",
    "City": "Abyhoj",
    "Country": "Denmark",
    "Phone": "12345678",
    "Email": "mail@mail.com",
    "CountryCode": "DK",
    "Currency": "EUR",
    "VAT": "DK12345678",
    "Residential": False,
}

recipient = {
    "Company": "Recipient Co",
    "Name": "Contact Name",
    "Address": ["Adr1, Adr2"],
    "Region": "MN",
    "Zip": "55420",
    "City": "Bloomington",
    "Country": "United States",
    "Phone": "0123456789",
    "Email": "mail@mail.com",
    "CountryCode": "US",
    "Currency": "EUR",
    "VAT": "",
    "Residential": False,
}

invoice_info = {
    "InvoiceId": "14385",
    "Weight": 0.11,
    "Quantity": 2,
    "Value": 20.0,
    "Shipping": 25.0,
    "ShippingExpress": True,
    "Currency": "EUR",
    "InvoicePath": commercial_invoice_path,
    "Pdfs": [product_description_1_path],
}

# print output
print(f"\n- recipient: {recipient}\n- invoice_info: {invoice_info}\n")

# create FedEx Label Helper and set configuration
flh = FedexLabelHelper()
flh.setShipmentConfig(CONFIG_OBJ=CONFIG_OBJ, invoice_info=invoice_info)

# add sender & recipient info to FedEx shipment
flh.setSenderInfo(sender)
flh.setRecipientInfo(recipient)

# set packaging based on weight
flh.set_packaging_info()

# add reference to CI as only commodity info
flh.add_ci_commodity()

# set duties payment information
flh.setDutiesPaymentInfo()

# upload documents
doc_ids = flh.upload_all_documents()

# link uploaded documents as ETD and setup event notifications
flh.setSpecialServices(doc_ids)

# process shipments and create shipping labels
flh.processInternationalShipment()
