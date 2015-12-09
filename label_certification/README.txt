FedEx Label Certification
=========================
In order to create FedEx shipments and print labels, you must go through a
label certification process with FedEx. This involves printing labels for
FedEx Express and FedEx Ground.

This module contains scripts to print out these labels for you automatically.
This should save you some time in getting certified and rolling into production.

Step by Step
------------
 * Go to http://fedex.com/developer/, enter the Web Services for Shipping
   section. Follow the 'Move to Production' link. Start the certification
   process there. You should end up with some PDFs on the process.
   You can also just call the FedEx support line and get them to do it if their
   page is too confusing.
 * Open cert_config.py. 
   * Edit CONFIG_OBJ to contain your FedEx TEST credentials.
   * Update SHIPPER_CONTACT_INFO.
   * Set the values needed for your label printer in LABEL_SPECIFICATION.
 * Run express.py to print labels for FedEx Express certification.
 * Run ground.py for FedEx Ground certification.
 * Send your labels to the FedEx certification addresses.
 * Wait a long time. Hopefully they will approve you eventually.

Support
-------
Unless you run into a programmatical problem, please do not create issues in
our python-fedex Google Code tracker. Contact FedEx with certification
problems and questions.