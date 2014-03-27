from sqlalchemy import Column, Integer, String, Binary, ForeignKey, DATETIME
from central_park.database import Base



class ParkingLot(Base):
    __tablename__ = 'Parking_Lot'

    id = Column(Integer, primary_key=True)
    name = Column(String(70), unique=True)
    address = Column(String(120), unique=True)

    def __repr__(self):
        return '<Parking_Lot: %r>' % (self.name)


class ParkingPlace(Base):
    __tablename__ = 'Parking_Place'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), unique=True)
    place_category = Column(Binary)
    parkinglot_id = Column(ForeignKey(ParkingLot.ParkingLot_id))
    


    def __repr__(self):
        return '<Parking_Place %r>' % (self.place_name)



class PriceHistory(Base):
    __tablename__ = 'PriceHistory'
    id = Column(Integer, primary_key=True)
    ParkingLot_id = Column(ForeignKey(ParkingLot.ParkingLot_id))
    acrivation_time = db.Column(db.DateTime)
    time_finish = db.Column(db.DateTime)

    def __repr__(self):
        return '<Rate_Statistics %r>' % (self.id)



class Payment(Base):
    __tablename__ = 'Payment'
    payment_id = Column(Integer, primary_key=True)
    car_number = Column(String(8))
    cost = Column(Integer)
    expiration_time = Column(DATETIME())
    hours_paid = db.Column(db.String(15))
    id_lot= db.Column(db.Integer)
    id_place = db.Column(db.Integer)
    id_rate = db.Column(db.String(10))
    hourly_rate = db.Column(db.Integer)

    def __repr__(self):
        return '<Payment %r>' % (self.id)
