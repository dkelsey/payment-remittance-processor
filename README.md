payment-remittance-processor
============================

This project contains two script:
* verifyEditLoad.py  which parses, verifies and loads British Columbia Liquor Distribution (BCLD) Payment Remittance reports
* ldb_batches.py  which parse, verifies and load batches or invoices file into a DB

#Payment Remittance Processor:

```
shell> ./verifyEditLoad.py ./BCLDB_Payment_Remittance_75467_2014-8-18.csv
```


#The file is processed in the following manner:

* It is tested to ensure it contains expected header and data headers.
* Header data is loaded into a vector and any formatting/converstions applied
* The header data is loaded into a mysql DB.
* Each row of data is loaded into a vector, any formatting/converstions applied, and
   the data is loaded into a mysql DB.

#DB Schema:

**paymentremittance:**
* represents paymentremittance file.
* contains the header data.
* paymentremittanceid uniquely identifies each record.

**paymentremittancedata:**
* represents paymentremittance data.
* paymentremittanceid relates each record to the source file.

```sql
   CREATE TABLE `paymentremittance` (
     `paymentremittanceid` int(11) NOT NULL AUTO_INCREMENT,
     `payeename` varchar(64) DEFAULT NULL,
     `payeeid` int(11) DEFAULT NULL,
     `payeesite` varchar(64) DEFAULT NULL,
     `paymentnumber` int(11) DEFAULT NULL,
     `paymentdate` date DEFAULT NULL,
     PRIMARY KEY (`paymentremittanceid`)
   )

   CREATE TABLE `paymentremittancedata` (
     `paymentremittanceid` bigint(20) DEFAULT NULL,
     `invoiceNumber` varchar(32) DEFAULT NULL,
     `orderType` varchar(32) DEFAULT NULL,
     `orderNumber` varchar(32) DEFAULT NULL,
     `store` int(11) DEFAULT NULL,
     `billOfLading` int(11) DEFAULT NULL,
     `transactionDate` date DEFAULT NULL,
     `batchDate` date DEFAULT NULL,
     `SKU` int(11) DEFAULT NULL,
     `product` varchar(64) DEFAULT NULL,
     `UPC` varchar(32) DEFAULT NULL,
     `size` float DEFAULT NULL,
     `supplierID` int(11) DEFAULT NULL,
     `supplierName` varchar(64) DEFAULT NULL,
     `reason` varchar(64) DEFAULT NULL,
     `reference` varchar(64) DEFAULT NULL,
     `quantity` int(11) DEFAULT NULL,
     `UOM` varchar(32) DEFAULT NULL,
     `cost` decimal(15,2) DEFAULT NULL,
     `GST` decimal(15,2) DEFAULT NULL,
     `containerDeposit` varchar(64) DEFAULT NULL,
     `freightAllowance` varchar(64) DEFAULT NULL,
     `total` decimal(15,2) DEFAULT NULL
   )
   ```

#Dependencies:

- Connector/Python driver: http://dev.mysql.com/downloads/connector/python/
- A running MySQL DB containing a schema with the appropriate tables.

#Invoice Processor:
```
shell> ./ldb_batches.py ./CSV_4852.csv
```

#The file is processed in the following manner:

* It is tested to ensure it contains expected header and data headers.
* Each row of data is loaded into a vector, any formatting/converstions applied, and
   the data is loaded into a mysql DB.

#DB Schema:

**ldb_batches:**
* represents a batch or invoice file.
* batchid uniquely identifies each record.

**ldb_batchesdata:**
* represents batch/invoice data. 
* batchid relates each record to the source file.

```sql
   CREATE TABLE `ldb_batches` (
     `batchid` int(11) NOT NULL AUTO_INCREMENT,
     `file_name` varchar(64) DEFAULT NULL,
     `process_date` date DEFAULT NULL,
     PRIMARY KEY (`batchid`)
   )

   CREATE TABLE `ldb_batchesdata` (
     `batchid` int(11) DEFAULT NULL,
     `store_number` int(11) DEFAULT NULL,
     `transaction_type` varchar(32) DEFAULT NULL,
     `transaction_date` date DEFAULT NULL,
     `invoice_reference_number` int(11) DEFAULT NULL,
     `original_invoice_number` int(11) DEFAULT NULL,
     `customer_number` int(11) DEFAULT NULL,
     `customer_type` varchar(32) DEFAULT NULL,
     `customer_name` varchar(32) DEFAULT NULL,
     `customer_phone_Number` varchar(32) DEFAULT NULL,
     `customer_address` varchar(32) DEFAULT NULL,
     `customer_city` varchar(32) DEFAULT NULL,
     `customer_province` varchar(32) DEFAULT NULL,
     `customer_postal_code` varchar(7) DEFAULT NULL,
     `payment_method` varchar(32) DEFAULT NULL,
     `SKU` int(11) DEFAULT NULL,
     `quantity` int(11) DEFAULT NULL,
     `display_price` decimal(15,2) DEFAULT NULL,
     `container_deposit` decimal(15,2) DEFAULT NULL,
     `total_doc_amount` decimal(15,2) DEFAULT NULL,
     `return_reason_code` varchar(32) DEFAULT NULL,
     `pipeline_sales` varchar(64) DEFAULT NULL
   )
   ```


#Dependencies:

- Connector/Python driver: http://dev.mysql.com/downloads/connector/python/
- A running MySQL DB containing a schema with the appropriate tables.

