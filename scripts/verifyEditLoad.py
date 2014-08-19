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

"""Verify format of BCLD Remittance csv file(s) and load into a MySQL DB.

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

   CREATE TABLE `paymentremittance` (
     `paymentremittanceid` int(11) NOT NULL AUTO_INCREMENT,
     `payeename` varchar(64) DEFAULT NULL,
     `payeeid` int(11) DEFAULT NULL,
     `payeesite` varchar(64) DEFAULT NULL,
     `paymentnumber` int(11) DEFAULT NULL,
     `paymentdate` date DEFAULT NULL,
     `filename` varchar(32) DEFAULT NULL,
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

Dependencies:

  Connector/Python driver: http://dev.mysql.com/downloads/connector/python/
  A running MySQL DB containing a schema with the appropriate tables.

"""

import os
import re
import sys
import datetime
import mysql.connector
from utils.parsers import string_to_date

cnx = mysql.connector.connect(user='root', database='bvb')
cursor = cnx.cursor()

#
# headerTemplate: an immutale tuple listing, in order, the expected headers
#
headerTemplate = (
   "Payee Name:     ",
   "Payee ID:       ",
   "Payee Site:     ",
   "Payment Number: ",
   "Payment Date:   ",
   )
#
# headerConverters: a dictionary key'd on the Header title.  the value is a lambda to format data values
#
headerConverters = {
   "Payee Name:     " : (lambda x: x),
   "Payee ID:       " : (lambda x: x),
   "Payee Site:     " : (lambda x: x),
   "Payment Number: " : (lambda x: x),
   "Payment Date:   " : string_to_date,
   }
headerTitle2DBColumnName = {
   "Payee Name:     " : 'payeename',
   "Payee ID:       " : 'payeeid',
   "Payee Site:     " : 'payeesite',
   "Payment Number: " : 'paymentnumber',
   "Payment Date:   " : 'paymentdate',
   }

headerTemplate2 = (
   "Supplier: ",
   "Supplier Number: ",
   "Payment Number: ",
   )
#
# headerConverters: a dictionary key'd on the Header title.  the value is a lambda to format data values
#
headerConverters2 = {
   "Supplier: ":        (lambda x: x),
   "Supplier Number: ": (lambda x: x),
   "Payment Number: ":  (lambda x: x),
   }
header2Title2DBColumnName = {
   "Supplier: ":        'payeename',
   "Supplier Number: ": 'payeeid',
   "Payment Number: ":  'paymentnumber',
   }
#
#
#   VALIDATE Data Header (7th line of input file)
#
#   HeaderTemplate: an immutale tuple listing, in order, the expected headders
#
#
dataHeaderTemplate = (
   "Invoice Number",
   "Order Type",
   "Order Number",
   "Store",
   "Bill of Lading",
   "Transaction Date",
   "Batch Date",
   "SKU",
   "Product",
   "UPC",
   "Size",
   "Supplier ID",
   "Supplier Name",
   "Reason",
   "Reference",
   "Quantity",
   "UOM",
   "Cost",
   "GST",
   "Container Deposit",
   "Freight Allowance",
   "Total",
   )
#
#  headderConverters: a dictionary key'd on the Headder title.  the value is a lambda to format data values
#
#
dataHeaderConverters = {
   "Invoice Number"   : (lambda x: x),
   "Order Type"       : (lambda x: x),
   "Order Number"     : (lambda x: x),
   "Store"            : (lambda x: x),
   "Store Number"     : (lambda x: x),
   "Bill of Lading"   : (lambda x: x),
   "Transaction Date" : string_to_date,
   "Batch Date"       : string_to_date,
   "SKU"              : (lambda x: x),
   "Product"          : (lambda x: x),
   "Product Description" : (lambda x: x),
   "UPC"              : (lambda x: x),
   "Size"             : (lambda x: x),
   "Pack"             : (lambda x: x),
   "Supplier ID"      : (lambda x: x),
   "Supplier Name"    : (lambda x: x),
   "Reason"           : (lambda x: x),
   "Reference"        : (lambda x: x),
   "Quantity"         : (lambda x: x),
   "UOM"              : (lambda x: x),
   "Cost"             : (lambda x: x),
   "Item Cost"        : (lambda x: x),
   "GST"              : (lambda x: x),
   "Container Deposit": (lambda x: x),
   "Freight Allowance": (lambda x: x),
   "Total"            : (lambda x: x),
   }
dataHeader2DBColumnName = {
   "Invoice Number"   : 'invoiceNumber',
   "Order Type"       : 'orderType',
   "Order Number"     : 'orderNumber',
   "Store"            : 'store',
   "Store Number"     : 'store',
   "Bill of Lading"   : 'billOfLading',
   "Transaction Date" : 'transactionDate',
   "Batch Date"       : 'batchDate',
   "SKU"              : 'SKU',
   "Product"          : 'product',
   "Product Description" : 'product',
   "UPC"              : 'UPC',
   "Size"             : 'size',
   "Pack"             : 'size',
   "Supplier ID"      : 'supplierID',
   "Supplier Name"    : 'supplierName',
   "Reason"           : 'reason',
   "Reference"        : 'reference',
   "Quantity"         : 'quantity',
   "UOM"              : 'UOM',
   "Cost"             : 'cost',
   "Item Cost"        : 'cost',
   "GST"              : 'GST',
   "Container Deposit": 'containerDeposit',
   "Freight Allowance": 'freightAllowance',
   "Total"            : 'total',
   }


def validate_and_get_header(fn, h, hv):
   """Validate that the file has the correct header names and load header names and values.
   
   Args:
      fn: A string nameing a file.
       h:  a reference to a list that will store Header Names.
      hv: A reference to a list that will store Header Values.
   
   Returns:
      The list of header names is returned by the reference to h, and 
      the list of header values is returned by the reference to hv
   
      h  = ['Payee Name', 'Payee Id', 'Payee Site']
      hv = ['Barkervill Brewing', '172053', 'Quisnel']
   
   Raises:
      NameError: The number or the value of header names were not expected values.
  """
   pattern = r'^,+$'
   print fn
   f = open(fn, 'r')
   for line in f:
      m = re.match(pattern,line.rstrip())
      if line.rstrip() and m is None:
        h.append( line.replace('"','').rstrip().split(',')[0] )
        hv.append( line.replace('"','').rstrip().split(',')[1] )
      else:
        break
   f.close()
   if len(headerTemplate) == len(h):
      for f, b in zip(headerTemplate,h):
         if (f != b) :
            raise NameError('{0}: header Problems: {1} != {2}'.format(fn, f,b))
   elif len(headerTemplate2) == len(h):
      for f, b in zip(headerTemplate2,h):
         if (f != b) :
            raise NameError('{0}: header Problems: {1} != {2}'.format(fn, f,b))
   else:
      raise NameError('{0}: wrong number of headers: {1}'.format(fn,len(h)))


def validate_and_get_dataheader(fn, dh):
   """Validate that the file has the correct header names  for the data section and load names.
   
   Args:
      fn: A string nameing a file.
      dh: A reference to a list that will store Data Header Names.
   
   Returns:
      The list of Data Header names is returned by the reference to dh.
   
      dh  = ['Invoice Number', 'Order Type', 'Order Number', 'Store', 'Bill of Lading',
             'Transaction Date', 'Batch Date', 'SKU', 'Product', 'UPC', 'Size', 
             'Supplier ID', 'Supplier Name', 'Reason', 'Reference', 'Quantity',
             'UOM', 'Cost', 'GST', 'Container Deposit', 'Freight Allowance', 'Total'
      ]
   
   Raises:
      NameError: The number or the value of data header names were not expected values.
  """
   f = open(fn, 'r')
   if len(headerTemplate) == len(header):
      line = f.readlines()[6:7]
      dh.extend( ''.join(line).replace('"','').strip().split(',') )
      if len(dataHeaderTemplate) < len(dh) :
         print '{0} has wrong number of data headers; has {1}; expectin {2}'.format(fn,len(dh),len(dataHeaderTemplate))
         print dataHeaderTemplate
         print dh
         raise NameError('{0}: wrong number of data headers; has {1}'.format(fn,len(dh)))
   elif len(headerTemplate2) == len(header):
      line = f.readlines()[4:5]
      dh.extend( ''.join(line).replace('"','').strip().split(',') )
      if len(dataHeaderTemplate) < len(dh):
         print '{0} has wrong number of data headers; has {1}; expectin {2}'.format(fn,len(dh),len(dataHeaderTemplate))
         print dataHeaderTemplate
         print dh
         raise NameError('{0}: wrong number of data headers; has {1}'.format(fn,len(dh)))
   f.close()


for fname in sys.argv[1:]:
   header = []
   headerValues = []
   dataHeader = []
   
   validate_and_get_header(fname, header, headerValues)
   validate_and_get_dataheader(fname, dataHeader)
   
   add_paymentremittance = (
     "INSERT INTO paymentremittance "
     " (payeename, payeeid, payeesite, paymentnumber, paymentdate, filename ) "
     " VALUES ( %(payeename)s, %(payeeid)s, %(payeesite)s, %(paymentnumber)s, %(paymentdate)s, %(filename)s)" )
   
   data_paymentremittance = {
      "payeename"    : '',
      "payeeid"      : 0,
      "payeesite"    : '',
      "paymentnumber": 0,
      "paymentdate"  : datetime.datetime.strptime('01-JAN-2000', "%d-%b-%Y").date(),
      "filename"     : 'N/A',
   }
   
   if os.path.isfile(fname) :
      data_paymentremittance['filename'] = os.path.basename(fname)
   
   if len(header) == len(headerTemplate2):  # does the file have a header with only 3 records
      for h, v in zip(header,headerValues):
         data_paymentremittance[ header2Title2DBColumnName[h]] = headerConverters2[h](v)
   else:
      for h, v in zip(header,headerValues):
         data_paymentremittance[headerTitle2DBColumnName[h]] = headerConverters[h](v)
   
   cursor.execute(add_paymentremittance,data_paymentremittance)
   cnx.commit()
   paymentremittanceid = cursor.lastrowid
   
   add_paymentremittancedata = (
      "INSERT INTO paymentremittancedata "
      " (paymentremittanceid, "
      " invoiceNumber, "
      " orderType, "
      " orderNumber, "
      " store, "
      " billOfLading, "
      " transactionDate, "
      " batchDate, "
      " SKU, "
      " product, "
      " UPC, "
      " size, "
      " supplierID, "
      " supplierName, "
      " reason, "
      " reference, "
      " quantity, "
      " UOM, "
      " cost, "
      " GST, "
      " containerDeposit, "
      " freightAllowance, "
      " total)"
      "VALUES ("
      " %(paymentremittanceid)s, "
      " %(invoiceNumber)s, "
      " %(orderType)s, "
      " %(orderNumber)s, "
      " %(store)s, "
      " %(billOfLading)s, "
      " %(transactionDate)s, "
      " %(batchDate)s, "
      " %(SKU)s, "
      " %(product)s, "
      " %(UPC)s, "
      " %(size)s, "
      " %(supplierID)s, "
      " %(supplierName)s, "
      " %(reason)s, "
      " %(reference)s, "
      " %(quantity)s, "
      " %(UOM)s, "
      " %(cost)s, "
      " %(GST)s, "
      " %(containerDeposit)s, "
      " %(freightAllowance)s, "
      " %(total)s)" )
   data_paymentremittancedataTemplate = {
      "paymentremittanceid"  : paymentremittanceid,
      "invoiceNumber"        : 'N/A',
      "orderType"            : 'N/A',
      "orderNumber"          : 'N/A',
      "store"                : 0,
      "billOfLading"         : 0,
      "transactionDate"      : datetime.datetime.strptime('20000101', "%Y%m%d").date(),
      "batchDate"            : datetime.datetime.strptime('20000101', "%Y%m%d").date(),
      "SKU"                  : 0,
      "product"              : 'N/A',
      "UPC"                  : 'N/A',
      "size"                 : 0,
      "supplierID"           : 0,
      "supplierName"         : 'N/A',
      "reason"               : 'N/A',
      "reference"            : 'N/A',
      "quantity"             : 0,
      "UOM"                  : 0,
      "cost"                 : 0,
      "GST"                  : 0,
      "containerDeposit"     : 'N/A',
      "freightAllowance"     : 'N/A',
      "total"                : 0
   }
   if len(header) == len(headerTemplate2): # does the file only have the 3 column header
      f = open(fname, 'r')
      for line in f.readlines()[5:-3]:
         dataValues = ()
         dataValues = tuple(line.replace('"','').strip().split(','))
         dataValues = tuple(d.strip() for d in dataValues)
         data_paymentremittancedata = data_paymentremittancedataTemplate.copy()
         for h,v in zip(dataHeader,dataValues):
            data_paymentremittancedata[dataHeader2DBColumnName[h]] = dataHeaderConverters[h](v)
         cursor.execute(add_paymentremittancedata,data_paymentremittancedata)
         cnx.commit()
      f.close()
   else:
      f = open(fname, 'r')
      for line in f.readlines()[7:-3]: 
         dataValues = ()
         dataValues = tuple(line.replace('"','').strip().split(','))
         dataValues = tuple(d.strip() for d in dataValues)
         data_paymentremittancedata = data_paymentremittancedataTemplate.copy()
         for h,v in zip(dataHeader,dataValues):
            data_paymentremittancedata[dataHeader2DBColumnName[h]] = dataHeaderConverters[h](v)
         cursor.execute(add_paymentremittancedata,data_paymentremittancedata)
         cnx.commit()
      f.close()
cursor.close()
cnx.close()
