import unittest, random  
from services import *
import datetime
class GetCurrentPriceHistoryTestCase(unittest.TestCase):
  	def test_number_get_current_pricehistory_id(self):
  		place_id = 1
   		self.assertIsInstance(get_current_pricehistory_id(place_id), str, "get_current_pricehistory_id function returns incorrent value." + str(type(get_current_pricehistory_id(place_id)))) 

   	def test_none_get_current_pricehistory_id(self):
  		place_id = None
   		self.assertTrue(get_current_pricehistory_id(place_id) == None, "get_current_pricehistory_id  function returns incorrent value.") 


class GetCurrentTariffMatrixTestCase(unittest.TestCase):
  	def test_number_get_current_tariff_matrix(self):
  		lot_id = 1
   		self.assertTrue(get_current_tariff_matrix(lot_id) != None, "get_current_tariff_matrix function returns incorrent value." + str(type(get_current_tariff_matrix(lot_id)))) 

   	def test_none_get_current_tariff_matrix(self):
  		lot_id = None
   		self.assertTrue(get_current_pricehistory_id(lot_id) == None, "get_current_tariff_matrix  function returns incorrent value.") 


class CalculateEstimatedTimeTestCase(unittest.TestCase):
  	def test_normal_calculate_estimated_time(self):
  		time_start = datetime.datetime.now()
  		cost = 10 
  		place_id = 1
   		self.assertTrue(calculate_estimated_time(time_start, cost, place_id) is datetime.datetime, "calculate_estimated_time function returns incorrent value.") 

   	def test_error_calculate_estimated_time(self):
  		time_start = "some string"
  		cost = 10 
  		place_id = 1
   		self.assertFalse(calculate_estimated_time(time_start, cost, place_id) is datetime.datetime, "calculate_estimated_time function returns incorrent value.") 

class CalculateTotalPriceTestCase(unittest.TestCase):
  	def test_normal_calculate_total_price(self):
  		place_id = 1 
  		time_finish = datetime.datetime.now()
   		self.assertIsInstance(calculate_total_price(place_id, time_finish), int, "calculate_total_price function returns incorrent value.") 

   	def test_error_calculate_total_price(self):
  		place_id = 1 
  		time_finish = "somestring"
   		self.assertNotIsInstance(calculate_total_price(place_id, time_finish), int, "calculate_total_price function returns incorrent value.") 


class GetParkedCarOnLotTestCase(unittest.TestCase):
  	def test_normal_get_parked_car_on_lot(self):
  		place_id = 1 
   		self.assertIsInstance(get_parked_car_on_lot(place_id), list, "get_parked_car_on_lot function returns incorrent value.") 

   	def test_error_get_parked_car_on_lot(self):
  		place_id = "some invalid id" 
   		self.assertFalse(len(get_parked_car_on_lot(place_id)) > 0, "get_parked_car_on_lot function returns incorrent value.") 

class GetListOfPlacesTestCase(unittest.TestCase):
  	def test_normal_get_list_of_places(self):
   		self.assertIsInstance(get_list_of_places(), list, "get_payment_by_date function returns incorrent value.") 


class GetPaymentByDateTestCase(unittest.TestCase):
  	def test_normal_get_payment_by_date(self):
   		place = 1
   		date_tmp = str(datetime.date.today())
   		self.assertIsInstance(get_payment_by_date(place, date_tmp), list, "get_payment_by_date function returns incorrent value.") 


class GetPricesParkingLotTestCase(unittest.TestCase):
  	def test_normal_get_priced_parking_lot(self):
   		price_min = 10
   		price_max = 50
   		self.assertIsInstance(get_priced_parking_lot(price_min, price_max), list, "get_priced_parking_lot function returns incorrent value.") 

class GetPlaceidByPlacenameTestCase(unittest.TestCase):
  	def test_normal_get_placeid_by_placename(self):
   		place_name = "somename"
   		self.assertTrue(get_placeid_by_placename(place_name) != None, "get_placeid_by_placename function returns incorrent value.") 

class InsertPaymentTestCase(unittest.TestCase):
  	def test_normal_insert_payment(self):
   		car_number = "ol755olo" 
   		cost = 50
   		expiration_time = datetime.datetime.now() 
   		transaction = "string" 
   		place_id = 1
   		pricehistory_id=5
   		self.assertTrue(insert_payment(car_number, cost, expiration_time, transaction, place_id, pricehistory_id), "insert_payment function returns incorrent value.") 

class CalculateMinutesCostTestCase(unittest.TestCase):
  	def test_normal_calculate_minutes_cost(self):
   		price_of_hour = 10
   		minutes = 15
   		self.assertIsInstance(calculate_minutes_cost(price_of_hour, minutes), (float,int), "calculate_minutes_cost function returns incorrent value.") 

class CalculateEstimatedTimeInLastHourTestCase(unittest.TestCase):
  	def test_normal_calculate_estimated_time_in_last_hour(self):
   		estimated_money = 40
   		price_of_hour = 10
   		self.assertIsInstance(calculate_estimated_time_in_last_hour(estimated_money, price_of_hour), (float, int), "calculate_estimated_time_in_last_hour function returns incorrent value.") 

class ParseTariffToListTestCase(unittest.TestCase):
  	def test_normal_parse_tariff_to_list(self):
   		tariff = "10;50"
   		self.assertIsInstance(parse_tariff_to_list(tariff), tuple, "parse_tariff_to_list function returns incorrent value.") 



#parse_tariff_to_list(tariff)
"""
  	def test_not_number_income(self):
  		income = random.randint(0,10000)
    	str_income = "Text string"
  		self.assertFalse(str_income == fee(income), "Fee function returns incorrent value when string is income.") 
"""
