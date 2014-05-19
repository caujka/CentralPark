from database import db_session
from models import *
from services import *
from sqlalchemy import desc
from datetime import timedelta
import random,datetime, time, string
import logging


def statistics_payment_fill():
    cars_count = 100
    year_b = 2014
    month_b = 4
    day_b = 6

    year_e = 2014
    month_e = 04
    day_e = 8
    parking_count = 1
    min_pay = 10
    max_pay = 90

    for x in range(0, cars_count):
        start_time = time.mktime(datetime.date(year_b, month_b, day_b).timetuple())
        end_time = time.mktime(datetime.date(year_e, month_e, day_e).timetuple())

        date = random.randrange(int(start_time), int(end_time))
        activation_time = datetime.datetime.fromtimestamp(date)

        car_number = (random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + " "+ str(random.randint(1000,9999))+ random.choice(string.ascii_letters) + random.choice(string.ascii_letters)).upper()
        cost = random.randint(min_pay,max_pay)
        place_id = random.randint(0,parking_count)
        transaction = 'string'

        pricehistory_id = get_current_pricehistory_id(place_id)
        estimated_time = calculate_estimated_time(activation_time, cost, place_id)
        pay = Payment(car_number, cost, estimated_time, transaction, place_id, pricehistory_id)
        pay.activation_time = activation_time
        db_session.add(pay)
    db_session.commit()
    return "all payments ok"

def get_statistics_by_place(place_name):
    stat = []
    statistics = db_session.query(ParkingPlace.name, Payment.car_number, Payment.cost).filter(ParkingPlace.name == place_name, ParkingPlace.id == Payment.place_id).all()
    for i in statistics:
        stat.append([i[1], i[2]])
    return stat

def get_statistics_by_place_year(place_name,year_):
    yr = datetime.datetime.strptime(year_,"%Y-%m-%d")
    year = datetime.date(yr.year, 01, 01)
    day = datetime.timedelta(days=1)
    stat = []
    for k in range(0,365):
        statistics = db_session.query(Payment.car_number, Payment.activation_time,Payment.expiration_time, ParkingPlace.name).filter(ParkingPlace.name == place_name, ParkingPlace.id == Payment.place_id).filter("Payment.activation_time<=:yearv and Payment.expiration_time>=:yearv").params(yearv=year).count()
        stat.append([year.isoformat(), statistics])
        year = year + day
    return stat

def get_statistics_by_place_day(place_name,year_):
    stat = []
    for i in range (0,24):
        stat.append([str(i),0,0])
    statistics = db_session.query(Payment.car_number, Payment.cost,Payment.activation_time, Payment.expiration_time, ParkingPlace.name).filter(ParkingPlace.name == place_name, ParkingPlace.id == Payment.place_id).filter("Payment.activation_time<=:yearv and Payment.expiration_time>=:yearv").params(yearv=year_).all()
    for j in statistics:
        if j[2].day == j[3].day:
            tilltime = j[3].hour
        else:
            tilltime = 24                      
        for k in range (j[2].hour,tilltime):
            stat[k][1]=stat[k][1]+1
    tm = db_session.query(PriceHistory.hourly_rate, ParkingPlace.name).filter(ParkingPlace.name == place_name, ParkingPlace.id == PriceHistory.parkingplace_id).filter("PriceHistory.activation_time<=:yearv").params(yearv=year_).order_by(desc(PriceHistory.activation_time)).first()
    t=tm[0].split(';')
    for i in range (0,24):
        stat[i][2]=int(t[i])   
    return stat
"""
    stat=[['0',  1000,400],['1',  1170, 460],['2',660,1120]]
    return stat
"""
