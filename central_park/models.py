from sqlalchemy import Column, Integer, String, Binary, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class ParkingPlace(Base):
    __tablename__ = 'ParkingPlace'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(Binary)
    location = Column(String)
    address = Column(String, unique=False)
    min_capacity = Column(Integer)

    payment = relationship("Payment")
    price_history = relationship("PriceHistory")


    def __init__(self, name, place_category, location, min_capacity):
        self.name = name
        self.place_category = place_category
        self.location = location
        self.min_capacity = min_capacity

    def __repr__(self):
        return '<ParkingPlace %r address %r capacity %r>' % (self.name, self.address, self.min_capacity)



class PriceHistory(Base):
    __tablename__ = 'PriceHistory'

    id = Column(Integer, primary_key=True)
    activation_time = Column(DATETIME)
    hourly_rate = Column(String)

    parkingplace_id = Column(ForeignKey(ParkingPlace.id))
    payment = relationship("Payment")

    def __init__(self, parkingplace_id, activation_time, hourly_rate):
        self.parkingplace_id = parkingplace_id
        self.activation_time = activation_time
        self.hourly_rate = hourly_rate

    def __repr__(self):
        return '<PriceHistory for parkingplace# %r since %r>' % (self.parkingplace_id, self.activation_time)


class Payment(Base):
    __tablename__ = 'Payment'
    id = Column(Integer, primary_key=True)
    car_number = Column(String)
    cost = Column(Integer)
    activation_time = Column(DATETIME)
    expiration_time = Column(DATETIME)
    transaction = Column(String)

    place_id = Column(ForeignKey(ParkingPlace.id))
    pricehistory_id = Column(ForeignKey(PriceHistory.id))

    def __init__(self, car_number, cost, expiration_time, transaction, place_id, pricehistory_id):
        self.car_number = car_number
        self.cost = cost
        self.date = datetime.now()
        self.expiration_time = expiration_time
        self.transaction = transaction
        self.place_id = place_id
        self.pricehistory_id = pricehistory_id

