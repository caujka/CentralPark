from database import db_session
from models import ParkingLot, ParkingPlace, PriceHistory, Payment
from sqlalchemy import desc
from datetime import datetime

# return current pricehistory_id for given parking_lot_id
def get_current_pricehistory_id(current_parkinglot_id):
    i = current_parkinglot_id
    tariff = db_session.query(PriceHistory).filter(PriceHistory.parkinglot_id == i).order_by(desc(PriceHistory.activation_time)).limit(1)
    if tariff[0]:
        return tariff[0].id
    else:
        return None


# return current hourly_rate for given parking lot
def get_current_tariff_matrix(current_parkinglot_id):
    i = current_parkinglot_id
    tariff = db_session.query(PriceHistory).filter(PriceHistory.parkinglot_id == i).order_by(desc(PriceHistory.activation_time)).limit(1)
    if tariff[0]:
        return tariff[0].hourly_rate
    else:
        return None


def calculate_estimated_time(cost, lot_id):
    tariff = get_current_tariff_matrix(lot_id)
    tariff = parse_tariff_to_list(tariff)
    time_finish = time_start = datetime.now()
    minutes = 60 - time_start.minute
    cost_in_first_hour = minutes * tariff[time_start.hour] / 60
    if (cost_in_first_hour < cost):
        cost -= cost_in_first_hour
        hour = time_start.hour + 1
        time_finish.hour += 1
        time_finish.minute = 00
        time_finish.second = 00
        while cost > tariff[hour]:
            cost -= tariff[hour]
            time_finish.hour += 1
            if hour < 23:
                hour += 1
            else:
                hour = 0
                time_finish.day += 1
        else:
            #minutes_in_last_hour = 60 * cost / tariff[hour]
            minutes_in_last_hour = calculate_estimated_time_in_last_hour(cost, tariff[hour])
            time_finish.minute = minutes_in_last_hour
    else:
        #minutes_in_last_hour = 60 * cost / tariff[time_start.hour]
        minutes_in_last_hour = calculate_estimated_time_in_last_hour(cost, tariff[time_start.hour])
        time_finish.minute += minutes_in_last_hour
    return time_finish


def calculate_estimated_time_in_last_hour(estimated_money, price_of_hour):
    return 60 * estimated_money / price_of_hour


def parse_tariff_to_list(tariff):
    return tuple([int(x) for x in tariff.split(';')])

