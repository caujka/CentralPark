from sqlalchemy import Column, Integer, String, Binary, ForeignKey, DATETIME
from central_park.database import Base


class ParkingLot(Base):
    __tablename__ = 'ParkingLot'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    address = Column(String, unique=True)

    def __repr__(self):
        return '<ParkingLot: %r>' % (self.name)


class ParkingPlace(Base):
    __tablename__ = 'ParkingPlace'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    place_category = Column(Binary)
    parkinglot_id = Column(ForeignKey(ParkingLot.id))
    


    def __repr__(self):
        return '<ParkingPlace %r>' % (self.id)



class PriceHistory(Base):
    __tablename__ = 'PriceHistory'

    id = Column(Integer, primary_key=True)
    parkingLot_id = Column(ForeignKey(ParkingLot.id))
    activation_time = Column(DATETIME)
    hourly_rate = Column(String)

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

    def __repr__(self):
        return '<Payment %r$ till %r>' % (self.cost, self.expiration_time)
