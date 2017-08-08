#List of classes to read the data in below format

"""
Customer
* type *
  * CUSTOMER
* verb *
  * NEW
  * UPDATE
* Additional Data
  * key(customer_id) *
  * event_time *
  * last_name
  * adr_city
  * adr_state
"""  
class customer:
    def __init__(self, key, verb, event_time, last_name, adr_city, adr_state):
        self.key = key
        self.verb = verb
        self.event_time = event_time
        self.last_name = last_name
        self.adr_city = adr_city
        self.adr_state = adr_state


"""
Site Visit
* type *
  * SITE_VISIT
* verb *
  * NEW
* Additional Data
  * key(page_id) *
  * event_time *
  * customer_id *
  * tags (array of name/value properties)
  
 """
class siteVisit:
    def __init__(self, key, verb, event_time, customer_id, tags):
        self.key = key
        self.verb = verb
        self.event_time = event_time
        self.customer_id = customer_id
        self.tags = tags


"""
Image Upload
* type *
  * IMAGE
* verb *
  * UPLOAD
* Additional Data
  * key(image_id) *
  * event_time *
  * customer_id *
  * camera_make
  * camera_model
  """
class image:
    def __init__(self, key, verb, event_time, customer_id, camera_make, camera_model):
        self.key = key
        self.verb = verb
        self.event_time = event_time
        self.customer_id = customer_id
        self.camera_make = camera_make
        self.camera_model = camera_model
		


"""Order
* type *
  * ORDER
* verb *
  * NEW
  * UPDATE
* Additional Data
  * key(order_id) *
  * event_time *
  * customer_id *
  * total_amount *
  """
class order:
    def __init__(self, key, verb, event_time, customer_id, total_amount):
        self.key = key
        self.verb = verb
        self.event_time = event_time
        self.customer_id = customer_id
        self.total_amount = total_amount
