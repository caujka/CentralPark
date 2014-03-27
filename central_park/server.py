import os
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

def get_db():
    """Opens a new database connection if there is none yet for the
current application context.
"""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.route('/')
def home():
    # send_static_file will guess the correct MIME type
    return render_template('home.html')

@app.route('/payment', methods = ['GET','POST'])
def payment():

    if request.method == 'GET':
        return render_template('payment.html')

    else:

        db = get_db()
        data  = request.data
        car_number = request.values.get('car_number')
        cost = int(request.values.get('cost'))
        leave_before = str(datetime.now() + timedelta(hours = calculate_hours(cost)))
        id_place = request.values.get('id_place')
        id_lot = request.values.get('id_lot')
        #car_number = request.json.get('car_number', '')
        #cost = float(request.json.get('cost', ''))
        #leave_before = str(datetime.now() + timedelta(hours = calculate_hours(cost)))
        #id_place = request.json.get('id_place', '')
        #id_lot = request.json.get('id_lot', '')
        rate = get_hourly_rate(id_lot, id_place)
        query = "INSERT INTO 'Payments' ('car_number', 'leave_before', 'cost', 'id_place', 'rate') \
    VALUES('{0}', '{1}', '{2}', '{3}', '{4}')".format(car_number, leave_before, str(cost), str(id_lot), str(id_place), str(rate))
        '''
        if id_lot in [l[0] for l in db.execute('SELECT id_lot FROM Parking_Lots').fetchall()] and \
            id_place in [p[0] for p in db.execute('SELECT id_place FROM Parking_Places').fetchall()]:
            db.execute(query)
           # print "OK!!!"
            #return jsonify( { 'Success': 'Everything is OK!' } ), 201
            return render_template('payment_response.html', car_number=car_number)
        else:
            #print "ERROR!!!"
            #return jsonify( {'Error': 'Transaction is not successful! There is no such place in db. Try again.'})
            return render_template('payment_response.html', error="ERROR!!!" )
'''
        credentials = {'car_number' : '123fv'}
        return render_template('payment_response.html', credentials=credentials)


@app.route('/price', methods = ['GET','POST'])
def show_price():
    if request.method == 'GET':
         return render_template('get_cars.html')
    else:
        db = get_db()
        id_lot=request.values.get('id_lot')
        print db.execute('SELECT * FROM PriceHistory where id_lot={0}'.format(id_lot))
        return id_lot

if __name__ == '__main__':
    init_db()
    app.run(debug=True, use_reloader=False)


