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
def get_current_tariff(current_parkinglot_id):
    i = current_parkinglot_id
    tariff = db_session.query(PriceHistory).filter(PriceHistory.parkinglot_id == i).order_by(desc(PriceHistory.activation_time)).limit(1)
    if tariff[0]:
        return tariff[0].hourly_rate
    else:
        return None


def calculate_estimated_time(cost, lot_id):
    tariff = get_current_tariff(lot_id)
    time_start = datetime.now()

def parse_tariff_to_list(tariff):
    return tuple([int(x) for x in tariff.split(';')])

