from database import db_session
from models import ParkingPlace, PriceHistory, Payment
from sqlalchemy import desc
from datetime import datetime, timedelta, date, time


# FIXED for NEW database
def create_payment_record(car_number, place_id, cost, expiration_time, transaction):
    """
    params:
        car_number(STRING), place_id(INT), cost(INT),
        expiration_time: expiration time, calculated on template (DATETIME)
        transaction: information about type of paying and operation number (STRING)
    return:
        tariff[0].id: id of actual PriceHistory for given ParkingLot (INT)
    """
    already_parked = db_session.query(Payment).filter(Payment.place_id == place_id,
                                                       Payment.car_number == car_number,
                                                       Payment.expiration_time >= datetime.now()).first()
    if already_parked is not None:
        already_parked.expiration_time = expiration_time
        already_parked.cost += cost
        already_parked.transaction += ', '+transaction
        db_session.commit()
    else:
        pricehistory_id = get_current_pricehistory_id(place_id)
        if insert_payment(car_number, cost, expiration_time, transaction, place_id, pricehistory_id):
            return True
        else:
            return False


# FIXED for NEW database
def get_current_pricehistory_id(place_id):
    """
    params:
        lot_id: id of parking lot from ParkingLot (INT)
    return:
        tariff[0].id: id of actual PriceHistory for given ParkingLot (INT)
    """
    i = place_id
    tariff = db_session.query(PriceHistory).filter(PriceHistory.parkingplace_id == i).order_by(desc(PriceHistory.activation_time)).all()

    if len(tariff) > 0:
        return tariff[0].id
    else:
        return None


# FIXED for NEW database
def get_current_tariff_matrix(place_id):
    """
    params:
        lot_id: id of ParkingLot (INT)
    return:
        tariff[0].hourly_rate: actual tariff matrix for given ParkingLot(STRING)
    """
    i = place_id
    tariff = db_session.query(PriceHistory).filter(PriceHistory.parkingplace_id == i).order_by(desc(PriceHistory.activation_time)).all()
    if len(tariff) > 0:
        return tariff[0].hourly_rate
    else:
        return None


# FIXED for NEW database
def calculate_estimated_time(time_start, cost, place_id):
    """
    params:
        cost: payed amount of money (INT)
        lot_id: id of parking lot (INT)
    return:
        time_finish: time expiration of parking (DATETIME)
    """
    tariff = parse_tariff_to_list(get_current_tariff_matrix(place_id))
    if tariff:
        time_finish = time_start
        try:
            cost_in_first_hour = calculate_minutes_cost(tariff[time_start.hour], 60 - time_start.minute)   
        except AttributeError:
            raise AttributeError("AttributeError") 
        if (cost_in_first_hour < cost):
            cost -= cost_in_first_hour
            hour = time_start.hour + 1
            time_finish += timedelta(hours=1)
            time_finish += timedelta(minutes=60-time_finish.minute)
            time_finish += timedelta(minutes=60-time_finish.second)
            while cost > tariff[hour]:
                cost -= tariff[hour % 24]
                time_finish += timedelta(hours=1)
            else:
                minutes_in_last_hour = calculate_estimated_time_in_last_hour(cost, tariff[hour])
                time_finish += timedelta(minutes=minutes_in_last_hour)
        else:# FIXED for NEW database
            minutes_in_last_hour = calculate_estimated_time_in_last_hour(cost, tariff[time_start.hour])
            time_finish += timedelta(minutes=minutes_in_last_hour)
        return time_finish
    else:
        return None

# FIXED for NEW database
def calculate_total_price(place_id, time_finish):
    """
    params:
        lot_id: id of parking lot (INT)
        time_finish: time expiration of parking (DATETIME)
    return:
        cost: total cost for given parking duration (INT)
    """
    if type(time_finish) is not datetime: return "value time_finish is not datetime"

    tariff = parse_tariff_to_list(get_current_tariff_matrix(place_id))
    time_start = datetime.now()
    
    if (time_finish.hour == time_start.hour and time_finish.day == time_start.day):
        return calculate_minutes_cost(time_finish.minute - time_start.minute, tariff[time_start.hour])
    else:
        cost = calculate_minutes_cost(tariff[time_start.hour], 60 - time_start.minute)
        hour = time_start.hour + 1
        time_start += timedelta(hours=1)
        time_start += timedelta(minutes=60-time_start.minute)
        time_start += timedelta(minutes=60-time_start.second)
        while time_start.hour < time_finish.hour:
            cost += tariff[hour % 24]
            time_start += timedelta(hours=1)
        else:
            cost += calculate_minutes_cost(tariff[hour], time_finish.minute - time_start.minute)
            return int(cost)


# FIXED for NEW database
def get_parked_car_on_lot(place_id):
    """
    params:
        place_id: id of parking place (INT)
    return:
        query: list of cars who allowed to be parked for now on given ParkingLor (LIST of dictionaries)
    """
    parked_car = db_session.query(Payment.car_number, Payment.expiration_time, Payment.place_id).\
                                                filter(Payment.expiration_time > datetime.now(),
                                                Payment.place_id == place_id).all()
    place_list = []
    i = 0
    for car in parked_car:
        place_list.append({
            "place_id": car.place_id,
            "car_number": car.car_number,
            "expiration_time": car.expiration_time
        })
        i += 1
    return place_list


# FIXED for NEW database
def get_list_of_places():
    """
    return:
        response: list of all ParkingLot.name (LIST of STR)
    """
    list_of_places_tuples = db_session.query(ParkingPlace.id).all()
    response = []
    for item in list_of_places_tuples:
        response.append(item[0])
    return response


# FIXED for NEW database
def get_payment_by_date(place, date_tmp):
    """
    params:
        lot_id: id of parking lot (INT)
        date: (DATE)
    return:
        query: list of Payment who parked in this date at ParkingLor (LIST of objects)
    """

    date_tmp = datetime.strptime(date_tmp, "%Y-%m-%d")
    list_of_payments = db_session.query(Payment).filter(Payment.activation_time >= date_tmp,
                                             Payment.activation_time <= (date_tmp + timedelta(days=1)),
                                             Payment.place_id == place).all()
    return list_of_payments


# FIXED for NEW database
def get_priced_parking_lot(price_min, price_max):
    """
    params:
        price_min: minimal searching price for current hour(INT)
        price_max: maximal searching price for current hour (INT)
    return:
        lots: list of ParkingLot with price for current hour in given range (LIST of objects)
    """
    current_hour = datetime.now().hour
    query = db_session.query(ParkingPlace)
    places = []
    for item in query:
        tariff = get_current_tariff_matrix(2)
        tariff = parse_tariff_to_list(tariff)
        if ((tariff[current_hour] >= int(price_min)) and (tariff[current_hour] <= int(price_max))):
           places.append({'id': item.id, 'address': item.address, 'name': item.name})
    return places


# FIXED for NEW database
def get_placeid_by_placename(place_name):
    """
    params:
        lot_name: ParkingLot.name of serching ParkingLot (STRING)
    return:
        lot_id: ParkingLot.id of given ParkingLot (INT)
    """
    parking_place = db_session.query(ParkingPlace.id).filter(ParkingPlace.name == place_name)
    return parking_place[0][0]



#some internal functions
#fixed for new database
def insert_payment(car_number, cost, expiration_time, transaction, place_id, pricehistory_id):
    try:
        pay = Payment(car_number, cost, expiration_time, transaction, place_id, pricehistory_id)
        db_session.add(pay)
        db_session.commit()
        return True
    except ValueError:
        return False

def calculate_minutes_cost(price_of_hour, minutes):
    return minutes * price_of_hour / 60


def calculate_estimated_time_in_last_hour(estimated_money, price_of_hour):
    return 60 * estimated_money / price_of_hour


def parse_tariff_to_list(tariff):
    if tariff:
        return tuple([int(x) for x in tariff.split(';')])
    else:
        return None
