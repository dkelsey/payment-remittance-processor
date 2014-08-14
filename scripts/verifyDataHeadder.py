#!/usr/bin/env python

'''
headderTemplate: an immutale tuple listing, in order, the expected headders
'''
headderTemplate = (
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

'''
headderConverters: a dictionary key'd on the Headder title.  the value is a lambda to format data values
'''
headderConverters = {
   "Invoice Number"   : (lambda x: "".join(x)),
   "Order Type"       : (lambda x: x),
   "Order Number"     : (lambda x: x),
   "Store"            : (lambda x: x),
   "Bill of Lading"   : (lambda x: x),
   "Transaction Date" : (lambda x: '{0}-{1}-{2}'.format(x[0:4], x[4:6], x[6:])),
   "Batch Date"       : (lambda x: '{0}-{1}-{2}'.format(x[0:4], x[4:6], x[6:])),
   "SKU"              : (lambda x: x),
   "Product"          : (lambda x: x),
   "UPC"              : (lambda x: x),
   "Size"             : (lambda x: x),
   "Supplier ID"      : (lambda x: x),
   "Supplier Name"    : (lambda x: x),
   "Reason"           : (lambda x: x),
   "Reference"        : (lambda x: x),
   "Quantity"         : (lambda x: x),
   "UOM"              : (lambda x: x),
   "Cost"             : (lambda x: x),
   "GST"              : (lambda x: x),
   "Container Deposit": (lambda x: x),
   "Freight Allowance": (lambda x: x),
   "Total"            : (lambda x: x),
   }

'''
Perform some preliminary validataion of the input file
'''
csvfile = 'BCLDB_Payment_Remittance_74596_2014-7-31.csv'
#f = open ('BCLDB_Payment_Remittance_75249_2014-8-11.csv', 'r')
#f = open ('BCLDB_Payment_Remittance_73976_2014-7-15.csv', 'r')
f = open (csvfile, 'r')
line = f.readlines()[6:7]
headders = tuple(''.join(line).replace('"','').strip().split(','))
f.close()

'''
validate the input file has the correct number of data headders
'''
if (len(headderTemplate) == len(headders)) :
   print "File has same number of headders"
else:
   print "File has different headders"
   raise NameError('wrong number of headders')

'''
validate that the input file has the correct headders in the correct order
'''
for f, b in zip(headderTemplate,headders):
   if (f != b) :
      raise NameError('Headder Problems f != b: {0}, {1}'.format(f, b))
print "File has correct Headder in correct order"

'''
Everything seems ok so proceed with processing the file so that it is ready for import 
into MySQL.
'''
# preproces file for import and write new file
# convert Transation Date and Batch Date to usable date types.

f = open (csvfile, 'r')

for line in f.readlines()[7:-3]:
   data = ''.join(line).replace('"','').strip().split(',')
   print ','.join([ headderConverters[h](v) for h,v in zip(headders, data)])
