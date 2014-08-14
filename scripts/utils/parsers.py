#!/usr/bin/env python

import re
import datetime

def string_to_date(date_string) :
   m = re.match(r'^\d+$',date_string)
   if m is not None:
      paymentdate = datetime.datetime.strptime(date_string, "%Y%m%d")
      return paymentdate
   else:
      m = re.match(r'^\d+-\w\w\w-\d\d\d\d$',date_string)
      if m is not None:
         paymentdate = datetime.datetime.strptime(date_string, "%d-%b-%Y")
         return paymentdate
      else:
         m = re.match(r'^\d+/\d\d/\d\d\d\d$',date_string)
         if m is not None:
            paymentdate = datetime.datetime.strptime(date_string,"%m/%d/%Y")
            return paymentdate
