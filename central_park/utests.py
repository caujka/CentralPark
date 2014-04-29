import unittest, random  
from services import *
from datetime import datetime, date


class GetCurrentPriceHistoryTestCase(unittest.TestCase):
    def test_number_get_current_pricehistory_id(self):
        place_id = 1
        self.assertIsInstance(get_current_pricehistory_id(place_id), int, "get_current_pricehistory_id function returns incorrent value.")

    def test_none_get_current_pricehistory_id(self):
        place_id = None
        self.assertTrue(get_current_pricehistory_id(place_id) == None, "get_current_pricehistory_id  function returns incorrent value.")

    def test_placeid_not_in_db_get_current_pricehistory_i(self):
        place_id = 999
        self.assertTrue(get_current_pricehistory_id(place_id) == None, "get_current_pricehistory_id  function returns incorrent value.")


class GetCurrentTariffMatrixTestCase(unittest.TestCase):
    def test_number_get_current_tariff_matrix(self):
        place_id = 1
        self.assertTrue(get_current_tariff_matrix(place_id) != None, "get_current_tariff_matrix function returns incorrent value.")

    def test_none_get_current_tariff_matrix(self):
        place_id = None
        self.assertTrue(get_current_pricehistory_id(place_id) == None, "get_current_tariff_matrix  function returns incorrent value.")

    def test_placeid_not_in_db_get_current_tariff_matrix(self):
        place_id = 999
        self.assertTrue(get_current_pricehistory_id(place_id) == None, "get_current_tariff_matrix  function returns incorrent value.")


class CalculateEstimatedTimeTestCase(unittest.TestCase):
    def test_normal_calculate_estimated_time(self):
        time_start = datetime.now()
        cost = 10
        place_id = 1
        self.assertIsInstance(calculate_estimated_time(time_start, cost, place_id), datetime, "calculate_estimated_time function returns incorrent value.")

    def test_error_calculate_estimated_time(self):
        time_start = datetime.now()
        cost = 10
        place_id = "olololo"
        self.assertTrue(calculate_estimated_time(time_start, cost, place_id) == None, "calculate_estimated_time function returns incorrent value.")


class CalculateTotalPriceTestCase(unittest.TestCase):
    def test_normal_calculate_total_price(self):
        place_id = 1
        time_finish = datetime.now()
        self.assertIsInstance(calculate_total_price(place_id, time_finish), int, "calculate_total_price function returns incorrent value.")

    def test_error_calculate_total_price(self):
        place_id = 1
        time_finish = "somestring"
        self.assertIsInstance(calculate_total_price(place_id, time_finish), str, "calculate_total_price function returns incorrent value.")


class GetParkedCarOnLotTestCase(unittest.TestCase):
    def test_normal_get_parked_car_on_lot(self):
        place_id = 1
        self.assertIsInstance(get_parked_car_on_lot(place_id), list, "get_parked_car_on_lot function returns incorrent value.")

    def test_error_get_parked_car_on_lot(self):
        place_id = "some invalid id"
        self.assertFalse(len(get_parked_car_on_lot(place_id)) > 0, "get_parked_car_on_lot function returns incorrent value.")


class GetListOfPlacesTestCase(unittest.TestCase):
    def test_normal_get_list_of_places_id(self):
        self.assertIsInstance(get_list_of_places_id(), list, "get_payment_by_date function returns incorrent value.")


class GetPaymentByDateTestCase(unittest.TestCase):
    def test_normal_get_payment_by_date(self):
        place = 1
        date_tmp = str(date.today())
        self.assertIsInstance(get_payment_by_date(place, date_tmp), list, "get_payment_by_date function returns incorrent value.")

    def test_date_format_error_get_payment_by_date(self):
        place = None
        date_tmp = "dfsffds"
        self.assertRaises(TypeError, lambda: get_payment_by_date(place, date_tmp), "get_payment_by_date function returns incorrent value.")


class GetPricesParkingLotTestCase(unittest.TestCase):
    def test_normal_get_priced_parking_lot(self):
        price_min = 10
        price_max = 50
        self.assertIsInstance(get_priced_parking_lot(price_min, price_max), list, "get_priced_parking_lot function returns incorrent value.")

    def test_type_error_get_priced_parking_lot(self):
        price_min = None
        price_max = "000"
        self.assertRaises(TypeError, lambda: get_priced_parking_lot(price_min, price_max), "get_priced_parking_lot function returns incorrent value.")


class GetPlaceidByPlacenameTestCase(unittest.TestCase):
    def test_normal_get_placeid_by_placename(self):
        place_name = "name01"
        self.assertTrue(get_placeid_by_placename(place_name) != None, "get_placeid_by_placename function returns incorrent value.")


class CreatePaymentRecordTestCase(unittest.TestCase):
    def test_normal_create_payment_record(self):
        car_number = "ff1111oo"
        place_id = 1
        cost = 10
        transaction = "web1"



class IsCarAlreadyParkedHereTestCase(unittest.TestCase):
    def test_normal_is_car_already_parked_here(self):
        place_id = 5
        car_number = "122"
        self.assertIsInstance(is_car_already_parked_here(place_id, car_number), object, "is_car_already_parked_here function returns incorrent value.")


class InsertNewPaymentTestCase(unittest.TestCase):
    def test_normal_insert_new_payment(self):
        car_number = "ol755olo"
        cost = 50
        transaction = "string"
        place_id = 1
        pricehistory_id=5
        self.assertTrue(insert_new_payment(car_number, cost, transaction, place_id, pricehistory_id), "insert_payment function returns incorrent value.")


class ContinueParkingTestCase(unittest.TestCase):
    def test_normal_continue_parking(self):
        parked_car_record = Payment("111", 10, datetime.now(), "111", 1, 1)
        cost = 10
        transaction = "111"
        self.assertTrue(continue_parking(parked_car_record, cost, transaction), "continue_parking return wrong value")

    def test_error_continue_parking(self):
        parked_car_record = None
        cost = 10
        transaction = "111"
        self.assertRaises(StandardError, lambda: continue_parking(parked_car_record, cost, transaction))


class GetEstimatedTimeForGivenCarTestCase(unittest.TestCase):
    def test_normal_get_estimated_time_for_given_car(self):
        car_number = "aa1111aa"
        place_id = 1
        cost = 10
        self.assertIs(type(get_estimated_time_for_given_car(car_number, place_id, cost)),
                      datetime, "get_estimated_time_for_given_car return wrong value")

    def test_placeid_not_in_db_get_estimated_time_for_given_car(self):
        car_number = "aa1111aa"
        place_id = 999
        cost = 10
        self.assertIs(get_estimated_time_for_given_car(car_number, place_id, cost), None)


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
        tariff = "10;50;10;10;10;10;10;10;10;10;10;10;10;10;10;10;10;10;10;10;10;10;10;10"
        self.assertIsInstance(parse_tariff_to_list(tariff), tuple, "parse_tariff_to_list function returns incorrent value.")

    def test_none_parse_tariff_to_list(self):
        tariff = [1, "aaa"]
        self.assertIsNone(parse_tariff_to_list(tariff), "parse_tariff_to_list function returns incorrent value.")


