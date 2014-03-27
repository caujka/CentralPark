from sqlalchemy import Column, Integer, String, Binary, ForeignKey, DATETIME
from database import Base
from datetime import datetime

class ParkingLot(Base):
    __tablename__ = 'ParkingLot'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False)
    address = Column(String, unique=False)

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __repr__(self):
        return '<ParkingLot: %r>' % (self.name)


class ParkingPlace(Base):
    __tablename__ = 'ParkingPlace'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    place_category = Column(Binary)
    parkinglot_id = Column(ForeignKey(ParkingLot.id))

    def __init__(self, name, place_category, parkinglot_id):
        self.name = name
        self.place_category = place_category
        self.parkinglot_id = parkinglot_id

    def __repr__(self):
        return '<ParkingPlace %r>' % (self.id)



class PriceHistory(Base):
    __tablename__ = 'PriceHistory'

    id = Column(Integer, primary_key=True)
    parkinglot_id = Column(ForeignKey(ParkingLot.id))
    activation_time = Column(DATETIME)
    hourly_rate = Column(String)

    def __init__(self, parkinglot_id, activation_time, hourly_rate):
        self.parkingLot_id = parkinglot_id
        self.activation_time = activation_time
        self.hourly_rate = hourly_rate

    def __repr__(self):
        return '<PriceHistory for %r lot from %r>' % (self.parkingLot_id, self.activation_time)




class Payment(Base):
    __tablename__ = 'Payment'
    id = Column(Integer, primary_key=True)
    car_number = Column(String)
    cost = Column(Integer)
    date = Column(DATETIME)
    expiration_time = Column(DATETIME())
    place_id = Column(ForeignKey(ParkingPlace.id))
    pricehistory_id = Column(ForeignKey(PriceHistory.id))

    def __init__(self, car_number, cost, expiration_time, place_id, pricehistory_id):
        self.car_number = car_number
        self.cost = cost
        self.date = datetime.now()
        self.expiration_time = expiration_time
        self.place_id = place_id
        self.pricehistory_id = pricehistory_id

    def __repr__(self):
        return '<Payment %r$ till %r>' % (self.cost, self.expiration_time)