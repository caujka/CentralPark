from sqlalchemy import Column, Integer, String, Date
from server.Model import Model

class Parking_Lot(db.Model):
    __tablename__ = 'Parking_Lot'
    id = db.Column(db.Integer, primary_key = True)
    id_lot = db.Column(db.Integer, db.ForeignKey('Parking_Place.id_lot'))
    name = db.Column(db.String(64))
    adress = db.Column(db.String(120), unique = True)
    parking_places = db.relationship('Parking_Place', backref = 'has')

    def __repr__(self):
    	return '<Parking_Lot %r>' % (self.name)

class Parking_Place(db.Model):
	__tablename__ = 'Parking_Place'
	id_lot = db.Column(db.Integer, primary_key = True)
	id_place = db.Column(db.Integer)
	place_category = db.Column(db.Binary)
	place_name = db.Column(db.String(100))

	def __repr__(self):
		return '<Parking_Place %r>' % (self.place_name)

class Lot_Statistics(db.Model):
	__tablename__ = 'Lot_Statistics'
	id = db.Column(db.Integer, primary_key = True)
	id_lot = db.Column(db.Integer, db.ForeignKey('Parking_Lot.id_lot'))
	id_rate = db.Column(db.Integer, db.ForeignKey('Rate_Statistics.id'))

class Rate_Statistics(db.Model):
	__tablename__ = 'Rate_Statistics'
	id = db.Column(db.Integer, primary_key = True)
	id_rate = db.Column(db.String(10), db.ForeignKey('Rate.id_rate'))
	time_start = db.Column(db.DateTime)
	time_finish = db.Column(db.DateTime)
	
	def __repr__(self):
		return '<Rate_Statistics %r>' % (self.id)

class Rate(db.Model):
	__tablename__ = 'Rate'
	id_rate = db.Column(db.String(10), primary_key = True)
	hour_0 = db.Column(db.Integer)
	hour_1 = db.Column(db.Integer)
	hour_2 = db.Column(db.Integer)
	hour_3 = db.Column(db.Integer)
	hour_4 = db.Column(db.Integer)
	hour_5 = db.Column(db.Integer)
	hour_6 = db.Column(db.Integer)
	hour_7 = db.Column(db.Integer)
	hour_8 = db.Column(db.Integer)
	hour_9 = db.Column(db.Integer)
	hour_10 = db.Column(db.Integer)
	hour_11 = db.Column(db.Integer)
	hour_12 = db.Column(db.Integer)
	hour_13 = db.Column(db.Integer)
	hour_14 = db.Column(db.Integer)
	hour_15 = db.Column(db.Integer)
	hour_16 = db.Column(db.Integer)
	hour_17 = db.Column(db.Integer)
	hour_18 = db.Column(db.Integer)
	hour_19 = db.Column(db.Integer)
	hour_20 = db.Column(db.Integer)
	hour_21 = db.Column(db.Integer)
	hour_22 = db.Column(db.Integer)
	hour_23 = db.Column(db.Integer)

	def __repr__(self):
		return '<Rate %r>' % (self.id_rate)

class Payment(db.Model):
	__tablename__ = 'Payment'
	id = db.Column(db.Integer, primary_key = True)
	car_number = db.Column(db.String(10))
	cost = db.Column(db.Integer)
	time_start = db.Column(db.String(20))
	hours_paid = db.Column(db.String(15))
	id_lot= db.Column(db.Integer)
	id_place = db.Column(db.Integer)
	id_rate = db.Column(db.String(10))
	hourly_rate = db.Column(db.Integer)

	def __repr__(self):
		return '<Payment %r>' % (self.id)
