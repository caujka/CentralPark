from database import db_session
from models import ParkingPlace, PriceHistory, Payment
from sqlalchemy import desc
from datetime import datetime, timedelta



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
    return:, "get_estimated_time_for_given_car return wrong value"
        time_finish: time expiration of parking (DATETIME)
    """
    tariff = parse_tariff_to_list(get_current_tariff_matrix(place_id))
    if tariff:
        time_finish = time_start
        try:
            cost_in_first_hour = calculate_minutes_cost(tariff[time_start.hour], 60 - time_start.minute)
            if (cost_in_first_hour < cost):
                cost -= cost_in_first_hour
                time_finish += timedelta(hours=1)
                time_finish = time_finish.replace(minute=0, second=0)
                hour = time_finish.hour
                while cost > tariff[hour % 24]:
                    cost -= tariff[hour % 24]
                    time_finish += timedelta(hours=1)
                    hour += 1
                else:
                    minutes_in_last_hour = calculate_estimated_time_in_last_hour(cost, tariff[hour % 24])
                    time_finish += timedelta(minutes=minutes_in_last_hour)
            else:
                minutes_in_last_hour = calculate_estimated_time_in_last_hour(cost, tariff[time_finish.hour])
                time_finish += timedelta(minutes=minutes_in_last_hour)
        except AttributeError:
            raise AttributeError("AttributeError")
        return time_finish
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
    if type(time_finish) == datetime:
        tariff = parse_tariff_to_list(get_current_tariff_matrix(place_id))
        time_start = datetime.now()
    
        if (time_finish.hour == time_start.hour and time_finish.day == time_start.day):
            return calculate_minutes_cost(time_finish.minute - time_start.minute, tariff[time_start.hour])
        else:
            cost = calculate_minutes_cost(tariff[time_start.hour], 60 - time_start.minute)
            time_start += timedelta(hours=1)
            time_start = time_start.replace(minute=0, second=0)
            hour = time_start.hour
            while time_start.hour < time_finish.hour:
                cost += tariff[hour % 24]
                time_start += timedelta(hours=1)
            else:
                cost += calculate_minutes_cost(tariff[hour], time_finish.minute - time_start.minute)
            return int(cost)
    else:
        return "Incorrect type of time_finish (datetime should be)"


# FIXED for NEW database
def get_parked_car_on_lot(place_id):
    """
    params:
        place_id: id of parking place (INT)
    return:
        query: list of cars who allowed to be parked for now on given ParkingLor (LIST of dictionaries)
    """
    parked_car = db_session.query(Payment.car_number, Payment.expiration_time, Payment.place_id).\
                                                filter(Payment.expiration_time > datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
def get_list_of_places_id():
    """
    return:
        response: list of all ParkingPlace.id (LIST of INT)
    """
    list_of_places_tuples = db_session.query(ParkingPlace.id).all()
    response = []
    for item in list_of_places_tuples:
        response.append(item[0])
    return response


def get_list_of_places_names():
    """
    return:
        response: list of all ParkingLot.name (LIST of STR)
    """
    list_of_places_tuples = db_session.query(ParkingPlace.name).all()
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
    res = []
    try:
        date_tmp = datetime.strptime(date_tmp, "%Y-%m-%d")
    except TypeError:
        raise TypeError("invalid data format given. Should be 'YYYY-MM-DD'")
    list_of_payments = db_session.query(Payment).filter(Payment.activation_time >= date_tmp,
                                             Payment.activation_time <= (date_tmp + timedelta(days=1)),
                                             Payment.place_id == place).all()
    for i in range(len(list_of_payments)):
        res.append({"car_number" : list_of_payments[i].car_number,
                  "cost" : list_of_payments[i].cost,
                  "expiration_time" : list_of_payments[i].expiration_time})
    return res


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
    try:
        for item in query:
            tariff = get_current_tariff_matrix(2)
            tariff = parse_tariff_to_list(tariff)
            if ((tariff[current_hour] >= int(price_min)) and (tariff[current_hour] <= int(price_max))):
                places.append({'id': item.id, 'address': item.address, 'name': item.name})
        return places
    except TypeError:
        raise TypeError


# FIXED for NEW database
def get_placeid_by_placename(place_name):
    """
    params:
        lot_name: ParkingLot.name of serching ParkingLot (STRING)
    return:
        lot_id: ParkingLot.id of given ParkingLot (INT)
    """
    parking_place = db_session.query(ParkingPlace.id).filter(ParkingPlace.name == place_name).all()
    if parking_place != [] and parking_place != None:
        return parking_place[0][0]
    return None


# FIXED for NEW database
def create_payment_record(car_number, place_id, cost, transaction):
    already_parked = is_car_already_parked_here(place_id, car_number)
    if already_parked is False or already_parked is None:
        try:
            insert_new_payment(car_number, cost, transaction,
                               place_id, get_current_pricehistory_id(place_id))
            return True
        except ValueError:
            raise ValueError
    else:
        try:
            continue_parking(already_parked, cost, transaction)
            return True
        except ValueError:
            raise ValueError


#some internal functions
#fixed for new database
def is_car_already_parked_here(place_id, car_number):
    already_parked_car = db_session.query(Payment).filter(Payment.car_number == car_number,
                                                          Payment.place_id == place_id,
                                                          Payment.expiration_time >= datetime.now()).all()
    if already_parked_car != [] and already_parked_car is not None:
        return already_parked_car[0]
    return False


def insert_new_payment(car_number, cost, transaction, place_id, pricehistory_id):
    try:
        estimated_time = calculate_estimated_time(datetime.now(), cost, place_id)
        pay = Payment(car_number, cost, estimated_time, transaction, place_id, pricehistory_id)
        db_session.add(pay)
        db_session.commit()
        return True
    except ValueError:
        raise ValueError('Database insertion error')


def continue_parking(parked_car_record, cost, transaction):
    try:
        parked_car_record.expiration_time = calculate_estimated_time(parked_car_record.expiration_time,
                                                                     cost,
                                                                     parked_car_record.place_id)
        parked_car_record.cost += cost
        parked_car_record.transaction += ', '+transaction
        db_session.add(parked_car_record)
        db_session.commit()
        return True
    except StandardError:
        raise StandardError("Database insertion error")


def get_estimated_time_for_given_car(car_number, place_id, cost):
    if place_id in get_list_of_places_id():
        already_parked_record = is_car_already_parked_here(place_id, car_number)
        if already_parked_record is False or already_parked_record is None:
            return calculate_estimated_time(datetime.now(), cost, place_id)
        else:
            return calculate_estimated_time(already_parked_record.expiration_time, cost, place_id)
    else:
        return None


def calculate_minutes_cost(price_of_hour, minutes):
    return minutes * price_of_hour / 60


def calculate_estimated_time_in_last_hour(estimated_money, price_of_hour):
    return 60 * estimated_money / price_of_hour


def parse_tariff_to_list(tariff):
    if type(tariff) == str or type(tariff) == unicode:
        return tuple([int(x) for x in tariff.split(';')])
    else:
        return None


def take_parking_coord():
    locations = db_session.query(ParkingPlace.location, ParkingPlace.id, ParkingPlace.name).all()
    ls = []
    tup = ()
    list_of_coord =[]
    for i in locations:
        ls.append(i[0]+','+str(i[2]) )
        tup = tuple(ls)
    
    k=0
    while k < len(tup):
        a=tuple([x for x in tup[k].split(',')])    
        list_of_coord.append(a)
        k+=1
    return list_of_coord


def get_payment_by_circle_coord(list_of_id):
    list_of_payment = []
    for i in list_of_id:
        element = db_session.query(ParkingPlace.name, Payment.car_number, Payment.expiration_time)
        element = element.filter(ParkingPlace.id == i, Payment.place_id == i,\
            Payment.expiration_time > datetime.now()).order_by(ParkingPlace.name).all()
        if element:
            list_of_payment.append(element)
    return list_of_payment

    
