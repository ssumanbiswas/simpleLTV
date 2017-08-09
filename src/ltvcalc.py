import sys
import json
from collections import defaultdict
from schema import customer,siteVisit,image,order
from datetime import datetime, timedelta
import simpleltv

#validate the argument list
if len(sys.argv)!=3:
	print 'Pleas provide two argument 1) File name 2) Number of coustomer record'
	sys.exit()
filename=sys.argv[1]
top_Customer=int(sys.argv[2])
#Declare dictonary to store all coustomer information
dict={}

#Read the Jason file and store in a variable 
with open (filename) as file:
	data=json.load(file)
	#print data
	file.close()
	
#call Ingest method to load the data in Dictionary
dict=simpleltv.Ingest(data,dict)
#call topXSimpleLTVCustomers method to calculate LTV value and write them in a file
#Reference algorithem https://blog.kissmetrics.com/how-to-calculate-lifetime-value
simpleltv.topXSimpleLTVCustomers(top_Customer,dict)
