from database import db_session
from models import *
from sqlalchemy import desc
from datetime import datetime, timedelta
import logging

logging.basicConfig(filename=u"server.log",
                    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


def get_current_pricehistory_id(place_id):
    """
    params:
        place_id: id of parking place from ParkingPlce (INT)
    return:
        tariff[0].id: id of actual PriceHistory for given ParkingPlace (INT)
        None: if there is no available PriceHistory record for given ParkingPlace
    """
    i = place_id
    tariff = db_session.query(PriceHistory).filter(PriceHistory.parkingplace_id == i).order_by(desc(PriceHistory.activation_time)).all()

    if len(tariff) > 0:
        return tariff[0].id
    else:
        return None


def get_current_tariff_matrix(place_id):
    """
    params:
        place_id: id of ParkingPlace (INT)
    return:
        tariff[0].hourly_rate: actual tariff matrix for given ParkingPlace(STRING)
        None: if there is tariff matrix for given ParkingPlace
    """
    i = place_id
    tariff = db_session.query(PriceHistory).filter(PriceHistory.parkingplace_id == i).order_by(desc(PriceHistory.activation_time)).all()
    if len(tariff) > 0:
        return tariff[0].hourly_rate
    else:
        return None


def calculate_estimated_time(time_start, cost, place_id):
    """
    params:
        time_start: time, from what calculate parking (DATETIME)
        cost: payed amount of money (INT)
        place_id: id of parking place (INT)
    return:, "get_estimated_time_for_given_car return wrong value"
        time_finish: time expiration of parking (DATETIME)
        None: if there is no such place_id or tariff matrix
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
            logging.WARNING("Error in time calculating: %s" % AttributeError)
            raise AttributeError("AttributeError")
        return time_finish
    return None


def calculate_total_price(place_id, time_finish):
    """
    params:
        place_id: id of parking place (INT)
        time_finish: time expiration of parking (DATETIME)
    return:
        cost: total cost for given parking duration (INT)
        None: if there is no such place_id or tariff matrix
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
    return None


def get_parked_car_on_lot(place_id):
    """
    params:
        place_id: id of parking place (INT)
    return:
        place_list: list of cars who allowed to be parked for now on given ParkingLor (LIST of dictionaries)
    """
    parked_car = db_session.query(Payment.car_number, Payment.expiration_time, Payment.place_id).\
                                                filter(Payment.expiration_time > datetime.now().strftime("%H:%M:%S %d-%m-%Y"),
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


def get_payment_by_date(place, date_tmp):
    """
    params:
        place: id of parking lot (INT)
        date_tmp: searching date in format 'YYYY-MM-DD' (str)
    return:
        res: list of Payment who parked in this date at ParkingLor (LIST of Payments)
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


def get_priced_parking_lot(price_min, price_max):
    """
    params:
        price_min: minimal searching price for current hour(INT)
        price_max: maximal searching price for current hour(INT)
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


def get_placeid_by_placename(place_name):
    """
    params:
        place_name: ParkingPlace.name of searching ParkingPlace (STRING)
    return:
        parking_place[0][0]: ParkingPlace.id of given ParkingPlace (INT)
        None: if there is no such record with given place_name
    """
    parking_place = db_session.query(ParkingPlace.id).filter(ParkingPlace.name == place_name).all()
    if parking_place != [] and parking_place != None:
        return parking_place[0][0]
    return None


def create_payment_record(car_number, place_id, cost, transaction):
    """
    params:
        car_number: car_number of parking car (STRING)
        place_id: id of place, where car should be parked (INT)
        cost: amount of money to pay for parking (INT)
        transaction: state or number of transaction (STR)
    return:
        True: if everything was done with success (Bool)
        ValueError: if something went wrong (exception)
    """
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


def is_car_already_parked_here(place_id, car_number):
    """
    params:
        place_id: id of parking place (INT)
        car_number: car number (STR)
    return:
        already_parked_car[0]: record of car, parked on given place (Payment)
        False: if there is no such car, parked on this place now
    """
    already_parked_car = db_session.query(Payment).filter(Payment.car_number == car_number,
                                                          Payment.place_id == place_id,
                                                          Payment.expiration_time >= datetime.now()).all()
    if already_parked_car != [] and already_parked_car is not None:
        return already_parked_car[0]
    return False


def insert_new_payment(car_number, cost, transaction, place_id, pricehistory_id):
    """
    params:
        car_number: car number (STR)
        cost: amount of money to pay (INT)
        transaction: state or number of transaction (STR)
        place_id: id of place (INT)
        pricehistory_id: id of PriceHistory record (INT)
    return:
        True: if insertion in DB was successful (Bool)
        ValueError: if something went wrong (exception)
    """
    try:
        estimated_time = calculate_estimated_time(datetime.now(), cost, place_id)
        pay = Payment(car_number, cost, estimated_time, transaction, place_id, pricehistory_id)
        db_session.add(pay)
        db_session.commit()
        return True
    except ValueError:
        raise ValueError('Database insertion error')


def continue_parking(parked_car_record, cost, transaction):
    """
    params:
        parked_car_record: Payment record, which should be modified (Payment)
        cost: amount of money to pay (INT)
        transaction: state or number of transaction (STR)
    return:
        True: if modification in DB was successful (Bool)
        StandardError: if something went wrong (exception)
    """
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
    """
    params:
        car_number: car number (STR)
        place_id: id of ParkingPlace record (INT)
        cost: amount money to pay (INT)
    return:
        est_time: estimated time consider to given params (DATETIME)
        None: if place_id do not exist in DB (None)
    """
    if place_id in get_list_of_places_id():
        already_parked_record = is_car_already_parked_here(place_id, car_number)
        if already_parked_record is False or already_parked_record is None:
            return calculate_estimated_time(datetime.now(), cost, place_id)
        else:
            return calculate_estimated_time(already_parked_record.expiration_time, cost, place_id)
    return None


def parse_sms_content(sms_content):
    """
    params:
        sms_content: all sms's content (STR)
    return:
        respond: dict with value of car number and parking place to pay for (dict)
        False: if sms content has wrong format (doesn't have two separators '#') (None)
    """
    sms_content_list = sms_content.split('#')
    if len(sms_content_list) >= 3:
        respond = {['car_number']: sms_content_list[2], ['place']: sms_content_list[1]}
        return respond
    return False


def calculate_minutes_cost(price_of_hour, minutes):
    return minutes * price_of_hour / 60


def calculate_estimated_time_in_last_hour(estimated_money, price_of_hour):
    return 60 * estimated_money / price_of_hour


def parse_tariff_to_list(tariff):
    if type(tariff) == str or type(tariff) == unicode:
        return tuple([int(x) for x in tariff.split(';')])
    else:
        return None


def get_list_of_sms_ids():
    """
    return:
        ls: list of all sms_id in SMSHistory (LIST of STR)
    """
    sms_history = db_session.query(SMSHistory).all()
    ls = []
    for sms in sms_history:
        ls.append(sms.sms_id)
    return ls


def take_parking_coord():
    """
    return:
        list_of_coord: list of all coord of all Parking Places (LIST of STR)
        None: if place_id do not exist in DB (None)
    """
    locations = db_session.query(ParkingPlace.location, ParkingPlace.id, ParkingPlace.name).all()
    ls = []
    tup = ()
    list_of_coord =[]
    for i in locations:
        ls.append(i[0]+','+str(i[2]) )
        tup = tuple(ls)
    
    k=0
    while k < len(tup):
        a = tuple([x for x in tup[k].split(',')])
        list_of_coord.append(a)
        k += 1
    return list_of_coord


def finish_sms_payment_record(transaction):
    record = db_session.query(Payment).filter(Payment.transaction == transaction).one()
    if record is not None:
        record.transaction.replace("waiting", "")
        payment_id = record.id

        db_session.add(record)
        db_session.commit()
        return payment_id
    return None


def delete_payment_by_transaction(transaction):
    try:
        record = db_session.query(Payment).filter(Payment.transaction == transaction).one()
        db_session.delete(record)
        db_session.commit()
    except:
        raise ValueError


def get_payment_by_circle_coord(list_of_id):
    """
    params:
        list_of_id: list of searching ParkingPlace's ids (LIST of INT)
    return:
        list_of_payment: list of payment information (list of obj)
    """
    list_of_payment = []
    for i in list_of_id:
        element = db_session.query(ParkingPlace.name, Payment.car_number, Payment.expiration_time)
        element = element.filter(ParkingPlace.id == i, Payment.place_id == i,\
            Payment.expiration_time > datetime.now()).order_by(ParkingPlace.name).all()
        if element:
            list_of_payment.append(element)
    return list_of_payment

