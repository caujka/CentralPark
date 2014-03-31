import os, sqlite3
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
    return render_template('home.html')

def get_hourly_rate(id_lot, id_place):
    return 10

def calculate_hours(cost):
    return 20

@app.route('/payment', methods = ['GET','POST'])
def payment():

    if request.method == 'GET':
        return render_template('payment.html')
     
    else:
        """
        car_number = request.values.get('car_number')
        cost = int(request.values.get('cost'))
        leave_before = str(datetime.now() + timedelta(hours = calculate_hours(cost)))
        id_place = request.values.get('id_place')
        id_lot = request.json.get('id_lot', '')
        print id_lot
        rate = get_hourly_rate(id_lot, id_place) 
        credentials = {'car_number' : car_number, 'cost': cost, 'leave_before':leave_before, 'id_place':id_place}
    
        """ 
        cost = int(request.values.get('cost'))
        id_lot = request.values.get('id_lot')
        id_place = request.values.get('id_place')
        credentials = { 'car_number' : request.values.get('car_number'),
                        'cost': cost,
                        'leave_before':str(datetime.now() + timedelta(hours = calculate_hours(cost))),
                        'id_place': id_place,
                        'id_lot': id_lot,
                        'rate': get_hourly_rate(id_lot, id_place) }
        #print credentials
       
        #p = Payment(car_number = credentials['car_number'], cost = cost, expiration_time = credentials['leave_before'], place_id = id_place, pricehistory_id = 1)    
        p = Payment(credentials['car_number'], cost, credentials['leave_before'], id_place, 1)    
       
        #query = "INSERT INTO 'Payment' ('car_number', 'cost', 'expiration_time','place_id', 'pricehistory') 
        #VALUES('{0}', '{1}', '{2}', '{3}', '{4}')".format(car_number,str(cost), leave_before, str(id_place), str(rate))
        
       
        if  (db_session.query(ParkingLot).filter(ParkingLot.id==id_lot).first().id):
            #(db_session.query(ParkingPlace).filter_by(id=id_place).first().id)):
            db_session.add(p)
            db_session.commit()
            #Payment.insert().execute(credentials['car_number'], cost, credentials['leave_before'], id_place, credentials['rate'])
            
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
    return render_template('response_price.html')

"""
@app.route('/find_place', methods=['GET', 'POST'])
def find_place():
    if request.method == 'GET':
         return render_template('get_place.html')
    else:
        db = get_db()
        low_pay = request.values.get('low_id')
        up_pay = request.values.get('up_id')

        query=('SELECT * FROM PriceHistory where hourly ')
"""
@app.route('/log', methods = ['GET','POST'])
def log_in():
    data = ''    
    return render_template('log.html')

@app.route('/welcome', methods = ['GET','POST'])
def welcome():
    return render_template('welcome.html')

@app.route('/find_place', methods = ['GET','POST'])
def find_place():
    return render_template('get_place.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, use_reloader=False)


