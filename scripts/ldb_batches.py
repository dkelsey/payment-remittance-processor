#!/usr/bin/env python
#
# Copyright 2014 Dave Kelsey.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Verify format and load BCLD invoice (batches) csv file(s) and load into a MySQL DB.

Usage: shell> ./ldb_batches.py ./CSV_4852.csv

The file is processed in the following manner:

 * It is tested to ensure it contains expected header and data headers.
 * Each row of data is loaded into a vector, any formatting/converstions applied, and
   the data is loaded into a mysql DB.

DB Schema:
   ldb_batches           : represents a batch or invoice file.
                           batchid uniquely identifies each record.
   ldb_batchesdata       : represents batch/invoice data. 
                           batchid relates each record to the source file.

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


Dependencies:

  Connector/Python driver: http://dev.mysql.com/downloads/connector/python/
  A running MySQL DB containing a schema with the appropriate tables.

"""
import os
import sys
import datetime
import mysql.connector
from utils.parsers import string_to_date

cnx = mysql.connector.connect(user='root', database='bvb')
cursor = cnx.cursor()

headerTemplate = (
   "Store_Number",
   "Transaction_Type",
   "Transaction_date",
   "Invoice_Reference_Number",
   "Original_Invoice_Number",
   "Customer_Number",
   "Customer_Type",
   "Customer_Name",
   "Customer_Phone_Number",
   "Customer_Address",
   "Customer_City",
   "Customer_Province",
   "Customer_Postal_Code",
   "Payment_Method",
   "SKU",
   "Quantity",
   "Display_Price",
   "Container_Deposit",
   "Total_Doc_Amount",
   "Return_Reason_Code",
   "Pipeline Sales"
)

headerConverters = {
   "Store_Number"             : (lambda x: x),
   "Transaction_Type"         : (lambda x: x),
   "Transaction_date"         : string_to_date,
   "Invoice_Reference_Number" : (lambda x: x),
   "Original_Invoice_Number"  : (lambda x: x),
   "Customer_Number"          : (lambda x: x),
   "Customer_Type"            : (lambda x: x),
   "Customer_Name"            : (lambda x: x),
   "Customer_Phone_Number"    : (lambda x: x),
   "Customer_Address"         : (lambda x: x),
   "Customer_City"            : (lambda x: x),
   "Customer_Province"        : (lambda x: x),
   "Customer_Postal_Code"     : (lambda x: x),
   "Payment_Method"           : (lambda x: x),
   "SKU"                      : (lambda x: x),
   "Quantity"                 : (lambda x: x),
   "Display_Price"            : (lambda x: x),
   "Container_Deposit"        : (lambda x: x),
   "Total_Doc_Amount"         : (lambda x: x),
   "Return_Reason_Code"       : (lambda x: x),
   "Pipeline Sales"           : (lambda x: x),
}

headerTitle2DBColumnName = {
   "batchid"                 : "batchid",
   "Store_Number"            : "store_number",
   "Transaction_Type"        : "transaction_type",
   "Transaction_date"        : "transaction_date",
   "Invoice_Reference_Number": "invoice_reference_number",
   "Original_Invoice_Number" : "original_invoice_number",
   "Customer_Number"         : "customer_number",
   "Customer_Type"           : "customer_type",
   "Customer_Name"           : "customer_name",
   "Customer_Phone_Number"   : "customer_phone_Number",
   "Customer_Address"        : "customer_address",
   "Customer_City"           : "customer_city",
   "Customer_Province"       : "customer_province",
   "Customer_Postal_Code"    : "customer_postal_code",
   "Payment_Method"          : "payment_method",
   "SKU"                     : "SKU",
   "Quantity"                : "quantity",
   "Display_Price"           : "display_price",
   "Container_Deposit"       : "container_deposit",
   "Total_Doc_Amount"        : "total_doc_amount",
   "Return_Reason_Code"      : "return_reason_code",
   "Pipeline Sales"          : "pipeline_sales" 
}

def validate_and_get_header(fn, h):
   f = open(fn, 'r')
   for line in f.readlines()[0:1]:
      #print line
      h.extend( ''.join(line).replace('"','').strip().split(','))
      if len(headerTemplate) < len(h) :
         print '{0} has the wrong numbero of data headers: has {1}; expecting {2}'.format(fn, len(h), len(headerTemplate))
   f.close()
   for f, b in  zip(headerTemplate,h):
      if (f != b) :
         raise NameError('{0}: header problems: {1} != {2}'.format(fn, f, b))

add_batches = (
   "INSERT INTO ldb_batches "
   " (file_name, "
   "process_date) "
   "VALUES ("
   " %(file_name)s, "
   " %(process_date)s) "
)

data_batchesTemplate = {
   "file_name": 'N/A',
   "process_date": datetime.datetime.now()
}

add_batches_data = (
   "INSERT INTO ldb_batchesdata "
   " (batchid, "
   "store_number, "
   "transaction_type, "
   "transaction_date, "
   "invoice_reference_number, "
   "original_invoice_number, "
   "customer_number, "
   "customer_type, "
   "customer_name, "
   "customer_phone_Number, "
   "customer_address, "
   "customer_city, "
   "customer_province, "
   "customer_postal_code, "
   "payment_method, "
   "SKU, "
   "quantity, "
   "display_price, "
   "container_deposit, "
   "total_doc_amount, "
   "return_reason_code, "
   "pipeline_sales) "
   "VALUES ("
   " %(batchid)s, "
   " %(store_number)s, "
   " %(transaction_type)s, "
   " %(transaction_date)s, "
   " %(invoice_reference_number)s, "
   " %(original_invoice_number)s, "
   " %(customer_number)s, "
   " %(customer_type)s, "
   " %(customer_name)s, "
   " %(customer_phone_Number)s, "
   " %(customer_address)s, "
   " %(customer_city)s, "
   " %(customer_province)s, "
   " %(customer_postal_code)s, "
   " %(payment_method)s, "
   " %(SKU)s, "
   " %(quantity)s, "
   " %(display_price)s, "
   " %(container_deposit)s, "
   " %(total_doc_amount)s, "
   " %(return_reason_code)s, "
   " %(pipeline_sales)s) "
)

data_batchesdataTemplate = {
   "batchid"                  : 0,
   "store_number"             : 0,
   "transaction_type"         : "",
   "transaction_date"         : datetime.datetime.strptime('20000101', "%Y%m%d").date,
   "invoice_reference_number" : 0,
   "original_invoice_number"  : 0,
   "customer_number"          : 0,
   "customer_type"            : "",
   "customer_name"            : "",
   "customer_phone_Number"    : "",
   "customer_address"         : "",
   "customer_city"            : "",
   "customer_province"        : "",
   "customer_postal_code"     : "",
   "payment_method"           : "",
   "SKU"                      : 0,
   "quantity"                 : 0,
   "display_price"            : 0.0,
   "container_deposit"        : 0.0,
   "total_doc_amount"         : 0.0,
   "return_reason_code"       : "",
   "pipeline_sales"           : ""
}

for fname in sys.argv[1:]:
   print fname
   header = []
   dataHeader = []
   validate_and_get_header(fname, header)
   data_batches = data_batchesTemplate.copy()
   if os.path.isfile(fname) :
      data_batches['file_name'] = os.path.basename(fname)
   cursor.execute(add_batches, data_batches)
   cnx.commit()
   batchid = cursor.lastrowid
   f = open(fname, 'r')
   data_batchesdataTemplate["batchid"] = batchid
   for line in f.readlines()[1:-3]:
      dataValues = ()
      dataValues = tuple(line.replace('"','').strip().split(','))
      dataValues = tuple(d.strip() for d in dataValues)
      data_batchesdata = data_batchesdataTemplate.copy()
      for h,v in zip(header,dataValues):
         data_batchesdata[headerTitle2DBColumnName[h]] = headerConverters[h](v)
      cursor.execute(add_batches_data,data_batchesdata)
      cnx.commit()
   f.close()
cursor.close()
cnx.close()
