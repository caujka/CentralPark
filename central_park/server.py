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


@app.route('/static/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('static', path))


@app.route('/payment', methods = ['POST'])
def payment():
    db = get_db()
    car_number = request.json.get('car_number', '')
    cost = float(request.json.get('cost', ''))
    leave_before = str(datetime.now() + timedelta(hours = calculate_hours(cost)))
    id_place = request.json.get('id_place', '')
    id_lot = request.json.get('id_lot', '')
    rate = get_hourly_rate(id_lot, id_place)
    query = "INSERT INTO 'Payments' ('car_number', 'leave_before', 'cost', 'id_place', 'rate') \
VALUES('{0}', '{1}', '{2}', '{3}', '{4}')".format(car_number, leave_before, str(cost), str(id_lot), str(id_place), str(rate))
    if (int(request.json.get('id_lot', '')) in [l[0] for l in db.execute('SELECT id_lot FROM Parking_Lots').fetchall()] and 
        int(request.json.get('id_place', '')) in [p[0] for p in db.execute('SELECT id_place FROM Parking_Places').fetchall()]):
        db.execute(query)
        print "OK!!!"
        return jsonify( { 'Success': 'Everything is OK!' } ), 201 
    else:             
        print "ERROR!!!"
        return jsonify( {'Error': 'Transaction is not successful! There is no such place in db. Try again.'}) 
   


if __name__ == '__main__':
    init_db()
    #parking_lot = ParkingLot("C1entxcv rewed", "bilidsafawf konia")
    #db_session.add(parking_lot)
    #db_session.commit()
    #print parking_lot
    app.run(debug=True)






'''
def calculate_hours(cost):
    rate = 10.0
    return cost / rate

def get_hourly_rate(id_lot, id_place):
    hourly_rate = 10.0
    return hourly_rate

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
current application context.
"""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
'''
