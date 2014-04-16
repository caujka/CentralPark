from database import db_session
from models import ParkingPlace, PriceHistory, Payment
from sqlalchemy import desc
from datetime import datetime, timedelta, date, time


def create_payment_record(car_number, place_id, cost, transaction):
    id
    car_number
    cost
    date
    expiration_time
    transaction 
    place_id
    pricehistory_id

    return 0


def insert_payment(car_number, cost, expiration_time, transaction, place_id, pricehistory_id):
    try:
        pay = Payment(car_number, cost, expiration_time, transaction, place_id, pricehistory_id)
        db_session.add(pay)
        db_session.commit(pay)
        return True
    except ValueError:
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
    tariff = db_session.query(PriceHistory).filter(PriceHistory.parkingplace_id == i).order_by(desc(PriceHistory.activation_time)).limit(1)
    if tariff[0]:
        return tariff[0].id
    else:
        return None


# FIXED for NEW database
def get_current_tariff_matrix(lot_id):
    """
    params:
        lot_id: id of ParkingLot (INT)
    return:
        tariff[0].hourly_rate: actual tariff matrix for given ParkingLot(STRING)
    """
    i = lot_id
    tariff = db_session.query(PriceHistory).filter(PriceHistory.parkinglot_id == i).order_by(desc(PriceHistory.activation_time)).limit(1)
    if tariff[0]:
        return tariff[0].hourly_rate
    else:
        return None


def calculate_estimated_time(cost, place_id):
    """
    params:
        cost: payed amount of money (INT)
        lot_id: id of parking lot (INT)
    return:
        time_finish: time expiration of parking (DATETIME)
    """
    tariff = get_current_tariff_matrix(place_id)
    tariff = parse_tariff_to_list(tariff)
    time_finish = time_start = datetime.now()
    cost_in_first_hour = calculate_minutes_cost(tariff[time_start.hour], 60 - time_start.minute)
    if (cost_in_first_hour < cost):
        cost -= cost_in_first_hour
        hour = time_start.hour + 1
        time_finish += timedelta(hours=1)
        time_finish += timedelta(minutes=60-time_finish.minute)
        time_finish += timedelta(minutes=60-time_finish.second)
        while cost > tariff[hour]:
            cost -= tariff[hour]
            time_finish += timedelta(hours=1)
            if hour < 23:
                hour += 1
            else:
                hour = 0
        else:
            minutes_in_last_hour = calculate_estimated_time_in_last_hour(cost, tariff[hour])
            time_finish += timedelta(minutes=minutes_in_last_hour)
    else:
        minutes_in_last_hour = calculate_estimated_time_in_last_hour(cost, tariff[time_start.hour])
        time_finish += timedelta(minutes=minutes_in_last_hour)
    return time_finish


def calculate_total_price(place_id, time_finish):
    """
    params:
        lot_id: id of parking lot (INT)
        time_finish: time expiration of parking (DATETIME)
    return:
        cost: total cost for given parking duration (INT)
    """
    tariff = get_current_tariff_matrix(place_id)
    tariff = parse_tariff_to_list(tariff)
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
            cost += tariff[hour]
            time_start += timedelta(hours=1)
            if hour < 23:
                hour += 1
            else:
                hour = 0
        else:
            cost += calculate_minutes_cost(tariff[hour], time_finish.minute - time_start.minute)
            return int(cost)


def get_parked_car_on_lot(lot_id):
    """
    params:
        place_id: id of parking place (INT)
    return:
        query: list of cars who allowed to be parked for now on given ParkingLor (LIST of objects)
    """
    parked_car = db_session.query(Payment.car_number, Payment.expiration_time, Payment.place_id).\
                                                filter(Payment.expiration_time > datetime.now(),
                                                Payment.place_id == ParkingPlace.id,
                                                ParkingPlace.parkinglot_id == lot_id).all()
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


def get_list_of_places_by_lot(lot_id):
    """
    params:
        lot_id: id of parking lot (INT)
    return:
        response: list of parkingplace_id which respond to given ParkingLor (LIST of INT)
    """
    query = db_session.query(ParkingPlace.id).filter(ParkingPlace.parkinglot_id == lot_id)
    response = []
    for item in query:
        response.append(item[0])
    return response


def get_list_of_lot():
    """
    return:
        response: list of all ParkingLot.name (LIST of STR)
    """
    query = db_session.query(ParkingLot.name).all()
    response = []
    for item in query:
        response.append(item[0])
    return response


def get_payment_by_date(lot_id, date_tmp):
    """
    params:
        lot_id: id of parking lot (INT)
        date: (DATE)
    return:
        query: list of Payment who parked in this date at ParkingLor (LIST of objects)
    """

    date_tmp = datetime.strptime(date_tmp, "%Y-%m-%d")
    query = db_session.query(Payment).filter(Payment.date >= date_tmp,
                                             Payment.date <= (date_tmp + timedelta(days=1)),
                                             Payment.place_id == ParkingPlace.id,
                                             ParkingPlace.parkinglot_id == lot_id).all()
    return query


def get_priced_parking_lot(price_min, price_max):
    """
    params:
        price_min: minimal searching price for current hour(INT)
        price_max: maximal searching price for current hour (INT)
    return:
        lots: list of ParkingLot with price for current hour in given range (LIST of objects)
    """
    current_hour = datetime.now().hour
    query = db_session.query(ParkingLot)
    lots = []
    for item in query:
        tariff = get_current_tariff_matrix(item.id)
        tariff = parse_tariff_to_list(tariff)
        if ((tariff[current_hour] >= int(price_min)) and (tariff[current_hour] <= int(price_max))):
            lots.append({'id': item.id, 'address': item.address, 'name': item.name})
    print lots
    return lots


def get_lotid_by_lotname(lot_name):
    """
    params:
        lot_name: ParkingLot.name of serching ParkingLot (STRING)
    return:
        lot_id: ParkingLot.id of given ParkingLot (INT)
    """
    query = db_session.query(ParkingLot.id).filter(ParkingLot.name == lot_name)
    for item in query:
        lot_id = item[0]
    if lot_id:
        return lot_id
    else:
        return lot_id


#some internal functions
def calculate_minutes_cost(price_of_hour, minutes):
    return minutes * price_of_hour / 60


def calculate_estimated_time_in_last_hour(estimated_money, price_of_hour):
    return 60 * estimated_money / price_of_hour


def parse_tariff_to_list(tariff):
    return tuple([int(x) for x in tariff.split(';')])
