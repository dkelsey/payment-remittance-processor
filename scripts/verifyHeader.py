#!/usr/bin/env python

'''
headderTemplate: an immutale tuple listing, in order, the expected headders
'''
headderTemplate = (
   "Payee Name:     ",
   "Payee ID:       ",
   "Payee Site:     ",
   "Payment Number: ",
   "Payment Date:   ",
   )
'''
headderConverters: a dictionary key'd on the Headder title.  the value is a lambda to format data values
'''
headderConverters = {
   "Payee Name:     " : (lambda x: x),
   "Payee ID:       " : (lambda x: x),
   "Payee Site:     " : (lambda x: x),
   "Payment Number: " : (lambda x: x),
   "Payment Date:   " : (lambda x: x),
   }
'''
Perform some preliminary validataion of the input file
'''
csvfile = 'BCLDB_Payment_Remittance_74596_2014-7-31.csv'
#f = open ('BCLDB_Payment_Remittance_75249_2014-8-11.csv', 'r')
#f = open ('BCLDB_Payment_Remittance_73976_2014-7-15.csv', 'r')
f = open (csvfile, 'r')
headders = ()
for l in f.readlines()[0:5]:
   # make a list and slice the first value out and append to another tuple
   headders = headders + (''.join(l).replace('"','').strip().split(',')[0],)
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
data = []
for h, l in zip(headders,f.readlines()[0:5]):
   # parse out the data from the line
   d = ''.join(l).replace('"','').strip().split(',')[1]
   # apply any formatting from he headderConverters and append to data
   data = data + [','.join([ headderConverters[h](d) ])]
#   print ','.join([ headderConverters[h](d) ])
print ','.join(data)
