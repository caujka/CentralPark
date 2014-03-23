import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'app.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('APP_SETTINGS', silent=True)


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

@app.route('/static/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('static', path))

@app.route('/todo/api/v1.0/payment', methods = ['POST'])
def trasaction():
    db = get_db()
    if (request.json.get('id_lot', '') in [t[0] for t in db.execute('SELECT id_lot FROM Parking_Lots').fetchall()]): 
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
        db.session.close()
        return jsonify( { 'Success': 'Everything is OK!' } ), 201 
    else:             
        return jsonify( {'Error': 'Transaction is not successful! There is no such place in db. Try again.'}) 

if __name__ == '__main__':
    init_db()
    app.run(debug = True)