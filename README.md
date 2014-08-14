payment-remittance-processor
============================

Script which parses, verifies and loads British Columbia Liquor Distribution (BCLD) Payment Remittance reports into a DB

#Usage:

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
   paymentremittance     : represents paymentremittance file.
                           contains the header data
                           paymentremittanceid uniquely identifies each record.
   paymentremittancedata : represents paymentremittance data.
                           paymentremittanceid relates each record to the source file.

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

#Dependancies:

- Connector/Python driver: http://dev.mysql.com/downloads/connector/python/
- A running MySQL DB containing a schema with the appropriate tables.
