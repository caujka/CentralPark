#!/usr/bin/python
from flask import Flask, jsonify, request, render_template
from app import db, models
import datetime
app = Flask(__name__)

def calculate_hours(cost):
    rate = 10.0
    return cost / rate 

def get_hourly_rate(id_lot, id_place):
    hourly_rate = 10.0
    return hourly_rate

#@app.route('/todo/api/v1.0/places', methods = ['GET'])
#def get_places():
#    place = db.execute('SELECT FROM Parking_Places')

@app.route('/')
def index():
    return render_template("static/index1.2.html", title = 'Home')

@app.route('/todo/api/v1.0/payment', methods = ['POST'])
def trasaction():
    if (request.json.get('id_lot', '') in [l.id_lot for l in models.Parking_Lot.query.all()]): 
##             request.json.get('id_place', '') in [p.id_lot for p in models.Parking_Place.query.all()]):
        receipe = models.Payment(
            id = models.Payment.query.all()[-1].id + 1,
            id_lot =  request.json.get('id_lot', ''),
            id_place = request.json.get('id_place', ''),
            car_number = request.json.get('car_number', ''),
            time_start = str(datetime.datetime.now().time()),
            hours_paid = str(calculate_hours(request.json.get('cost', ''))) + ' hours',
            cost = request.json.get('cost', ''),
            hourly_rate = get_hourly_rate(request.json.get('id_lot', ''), request.json.get('id_place', '')), 
            #result = True
        )
        db.session.add(receipe)
        db.session.commit()
        return jsonify( { 'Success': 'Everything is OK!' } ), 201 
    else:             
        return jsonify( {'Error': 'Transaction is not successful! There is no such place in db. Try again.'}) 

if __name__ == '__main__':
    app.run(debug = True)