payment-remittance-processor
============================

Script which parses, verifies and loads British Columbia Liquor Distribution (BCLD) Payment Remittance reports into a DB

Usage: shell> ./verifyEditLoad.py ./BCLDB_Payment_Remittance_75467_2014-8-18.csv

The file is processed in the following manner:

 * It is tested to ensure it contains expected header and data headers.
 * Header data is loaded into a vector and any formatting/converstions applied
 * The header data is loaded into a mysql DB.
 * Each row of data is loaded into a vector, any formatting/converstions applied, and
   the data is loaded into a mysql DB.

DB Schema:
   paymentremittance     : represents paymentremittance file.
                           contains the header data
                           paymentremittanceid uniquely identifies each record.
   paymentremittancedata : represents paymentremittance data.
                           paymentremittanceid relates each record to the source file.

