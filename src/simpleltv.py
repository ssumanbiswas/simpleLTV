import json ;
import sys ;
from collections import defaultdict ;
from schema import customer,siteVisit,image,order ;
from datetime import datetime, timedelta ;


#Function to ingest the in dictonary 
def Ingest(data,dict):
	try:	

		for i in data:
			if i['type']=='CUSTOMER':
						
				key=i['key']
				verb=i['verb']
				event_time=i['event_time']
				last_name=i['last_name']
				adr_city=i['adr_city']
				adr_state=i['adr_state']
				cust_details=customer(key,verb,event_time,last_name,adr_city,adr_state)
				#dict.clear()
				if key not in dict:
					dict[key]=defaultdict(list)
				dict[key]['CUSTOMER'].append(cust_details)

			elif i['type']=='SITE_VISIT':
				
				key=i['key']
				verb=i['verb']
				event_time=i['event_time']
				customer_id=i['customer_id']
				tags=i['tags']
				site_details=siteVisit(key,verb,event_time,customer_id,tags)
				dict[customer_id]['SITE_VISIT'].append(site_details)
				
			elif i['type']=='ORDER':
			
				key=i['key']
				verb=i['verb']
				event_time=i['event_time']
				customer_id=i['customer_id']
				total_amount=i['total_amount']
				order_details=order(key,verb,event_time,customer_id,total_amount)
				dict [customer_id]['ORDER'].append(order_details)				
		
			elif i['type']=='IMAGE':
				
				key=i['key']
				verb=i['verb']
				event_time=i['event_time']
				customer_id=i['customer_id']
				camera_make=i['camera_make']
				camera_model=i['camera_model']
				image_details=image(key,verb,event_time,customer_id,camera_make,camera_model)
				dict[customer_id]['IMAGE'].append(image_details) 
				
		return dict
	except:
		print "\n data_load: Error to read the data \n  please validate the data and rerun the job\n";
		sys.exit();
		
#Function to claculate lTV value 
def topXSimpleLTVCustomers(top_Customer,dict):
	#dictionary to hold customer id and calculated ltv value for coustomers.
	cust_ltv={} 
	t=10  #t is the average customer lifespan. The average lifespan for Shutterfly is 10 years.
	ltv=0
	try:
		for c in dict.keys(): #Going through each and every coustomer in dictionary 
			
			no_of_visit=0
			total_amount=0
			#total amount spent by customer in sigle or multiple transation
			order=dict[c].get('ORDER',None)
			if order is not None:
				for o in order:
					total_amount=total_amount+float(o.total_amount.split(' ')[0].strip())
					#print total_amount
		
			#total number of visits by a coustomer in his life time.
			
			visit=dict[c].get('SITE_VISIT',None)
			if visit is not None:
				no_of_visit=len(visit)
				print no_of_visit
				
			""" Logic to find number week's inbetween coustomer first and last visit
			assume event date is not in sorted order"""
			total_weeks = 0
			#min_cs_event_time = datetime.now().date()
			min_cs_event_time = datetime.strptime("9999-08-02T12:46:46.384Z", '%Y-%m-%dT%H:%M:%S.%fZ').date() #assign a large date in min variable
			#print min_cs_event_time
			#max_cs_event_time = datetime.now().date()
			max_cs_event_time = datetime.strptime("1000-08-02T12:46:46.384Z", '%Y-%m-%dT%H:%M:%S.%fZ').date() # assign a small date in max variable so that first date can be max
			
			
			customer=dict[c].get('CUSTOMER',None)
			if customer is not None:
				for cs in customer:
					cs_event_time = cs.event_time
					#print cs_event_time
					cs_event_time = datetime.strptime(cs_event_time, '%Y-%m-%dT%H:%M:%S.%fZ').date()
			
			
					if cs_event_time < min_cs_event_time:
						min_cs_event_time = cs_event_time
						print min_cs_event_time
					if cs_event_time > max_cs_event_time:
						max_cs_event_time = cs_event_time
						print max_cs_event_time
		
			monday1 = (min_cs_event_time - timedelta(days=min_cs_event_time.weekday()))
			monday2 = (max_cs_event_time - timedelta(days=max_cs_event_time.weekday()))
				
			total_weeks = ( (monday2 - monday1).days / 7 ) + 1
			print total_weeks
			#if total_weeks==0:
			#	total_weeks=1
	 

			
			"""A simple LTV can be calculated using the following equation: `52(a) x t`. Where `a` is the average customer value per week 
			(average customer expenditures per visit (USD) x number of site visits per week) """
			if no_of_visit>0:
				avg_cust_amount=total_amount/no_of_visit
				#print avg_cust_amount
				site_visit_per_week=float(no_of_visit /total_weeks)
				print site_visit_per_week
				a=avg_cust_amount*site_visit_per_week
				#print a
				ltv=52*a*t
				#print ltv
			else:
				ltv=0
			
			cust_ltv[c]=ltv
	except:
			
		print "\n  calculate topXSimpleLTVCustomers: Error in Caculting LTV \n check Division by zero";
		sys.exit();
			
	#sorting the dictionary and write the top X customers value in a file
	result=[]
	if top_Customer >  len(dict):
		top_Customer=len(dict)
	for i in  sorted(cust_ltv,key=cust_ltv.get,reverse=True):
		result.append((i,cust_ltv.get(i)))	
	try:
		output=open('output.txt','w+')
		output.write("***************************Top X Coustomers***************************")
		output.write("\n");
		output.write("Customer ID                                         LTV")
		output.write("\n");
		output.write("#######################################################################")
		output.write("\n");
		for c in range(0,top_Customer):
			output.write((str(result[c][0]))+'                                '+ (str(result[c][1])))
			output.write("\n");
		output.write("***********************End of File**************************************")
		output.close()
	except:
		output.close()
		print "\n writing output in File: There is an error to open/write output in the file"
		sys.exit()
