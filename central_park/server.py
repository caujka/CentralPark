import os, sqlite3
from services import * 
from datetime import datetime, timedelta
from models import ParkingLot, ParkingPlace, PriceHistory, Payment
from flask import Flask, request, g, redirect, url_for, abort, \
     render_template, flash, jsonify
from database import db_session, init_db


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'central_park.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))


#Controling session closing
@app.teardown_appcontext
def teardown_session(expception=None):
    db_session.remove()

app.config.from_envvar('APP_SETTINGS', silent=True)


@app.route('/')
def home():
    return render_template('home.html', classactive_home ="class=active")

def get_hourly_rate(id_lot, id_place):
    return 10

def calculate_hours(cost):
    return 20

@app.route('/payment', methods = ['GET','POST'])
def payment():

    if request.method == 'GET':
        return render_template('payment.html',classactive_payment ="class=active")
     
    else:
        username = request.values.get('username')
        cost = int(request.values.get('cost'))
        id_lot = request.values.get('id_lot')
        id_place = request.values.get('id_place')
        credentials = { 'username' : username,
                        'car_number' : request.values.get('car_number'),
                        'cost': cost,
                        'leave_before':datetime.now() + timedelta(hours = calculate_hours(cost)),
                        'id_place': id_place,
                        'id_lot': id_lot,
                        'rate': get_hourly_rate(id_lot, id_place) }
              
        print credentials['leave_before']
        p = Payment(credentials['car_number'], cost, credentials['leave_before'], id_place, 1)    
       
       
        if  (db_session.query(ParkingLot).filter(ParkingLot.id==id_lot).first().id):
            #(db_session.query(ParkingPlace).filter_by(id=id_place).first().id)):
            db_session.add(p)
            db_session.commit()
            
            
            return render_template('payment_response.html', credentials=credentials)
        else:
            return render_template('payment_response.html', error="ERROR!!!" )


@app.route('/price', methods = ['GET','POST'])
def show_price():
    """
    if request.method == 'GET':
         return render_template('get_cars.html')
    else:
        id_lot=request.values.get('lot_id')
        data = b.execute('SELECT * FROM PriceHistory where parkinglot_id={0}'.format(id_lot))
        data.fetchall()
    """
    return render_template('response_price.html', classactive_price ="class=active")

@app.route('/can_stand', methods=['GET', 'POST'])
def can_stand():
    if request.method == 'GET':
        return render_template('get_place.html', classactive_canstand="class=active")
    else:
        place = request.values.get('place')
        for obj in db_session.query(Payment).filter(Payment.place_id == place):
            car_number = obj.car_number
            cost = obj.cost
            expiration = obj.expiration_time

        response = {
        'id_lot': place,
        'car': car_number,
        'cost': cost,
        'time': expiration
        }
        if response:
            return render_template('response_aval_place.html', response=response, classactive_canstand="class=active")
        else:
            return render_template('response_aval_place.html', error="Something not correct", classactive_canstand="class=active")


@app.route('/log', methods = ['GET','POST'])
def log_in():
    data = ''    
    return render_template('log.html',classactive_log ="class=active")

@app.route('/welcome', methods = ['GET','POST'])
def welcome():
    return render_template('welcome.html', classactive_welcome ="class=active")


if __name__ == '__main__':
    init_db()
    app.run(debug=True, use_reloader=False)
