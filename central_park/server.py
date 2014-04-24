# -*- coding: utf-8 -*-
import os
from services import * 
from datetime import datetime, timedelta
from models import ParkingPlace, PriceHistory, Payment
from database import db_session, init_db
from flask.ext.babel import *
from flask_babelex import *
from flask import *
from flask import Flask, request, render_template, jsonify, json
import re
# create our little application :)
app = Flask(__name__)
babel = Babel(app)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'central_park.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

@babel.localeselector
def get_locale():   
    return g.get('current_lang', 'en')


@app.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        if request.view_args['lang_code'] not in ('en','de','uk'):
            return abort(404)
        g.current_lang = request.view_args['lang_code']
        request.view_args.pop('lang_code')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
    
#Controling session closing
@app.teardown_appcontext
def teardown_session(expception=None):
    db_session.remove()

app.config.from_envvar('APP_SETTINGS', silent=True)


@app.route('/')
def home():
     return redirect(url_for('welcome', lang_code="en"))

@app.route('/<lang_code>')
def index():
    return render_template('welcome.html')

@app.route('/<lang_code>/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'GET':
        return render_template('payment.html', classactive_payment="class=active")

    else:
        min_possible_cost = 1
        place_id = get_placeid_by_placename(request.json['place'])
        print place_id, type(place_id)


        reg = r'\d{1,}'
        reg_str = r'[A-Z, a-z, 0-9]{4,6}'

        if (re.search(reg, request.json['cost']) and re.search(reg, request.json['place'])
                and re.search(reg_str, request.json['car_number'])):
            cost = int(request.json['cost'])
            transaction = "web%s" % str(datetime.now())
            time_left = calculate_estimated_time(datetime.now(), cost, place_id)
            credentials = {
                'car_number': request.json['car_number'],
                'cost': cost,
                'time_left': time_left,
                'transaction': transaction,
                'place_id': request.json['place'],
                'rate': get_current_tariff_matrix(place_id)
            }
            pricehistory_id = get_current_pricehistory_id(place_id)

            p = Payment(request.json['car_number'], cost, time_left, transaction, place_id, pricehistory_id)
            db_session.add(p)
            db_session.commit()
            return render_template("payment_response.html", credentials=credentials)
        else:
            error = "Your data is not valid"
            return render_template("payment_response.html", error=error)


@app.route('/<lang_code>/history', methods=['GET', 'POST'])
def show_history():
    
    if request.method == 'GET':
        list_of_place = get_list_of_places()
        return render_template('history.html', place_list = list_of_place)
    
    else:
        choosen_place = request.values.get('place')
        print (choosen_place)
      
        data_time = request.values.get('date')
      
        actual_history = get_payment_by_date(choosen_place, data_time)
        print (actual_history)
        return render_template('response_history.html', history_info = actual_history) 


@app.route('/<lang_code>/can_stand', methods=['GET', 'POST'])
def can_stand():
    if request.method == 'GET':
        return render_template('get_cars.html', classactive_canstand="class=active", res_list=get_list_of_places())
    elif request.method == 'POST':
        lot_name = request.values.get('lot_name')
        #lot_id = get_list_of_places()
        response = get_parked_car_on_lot(lot_name)
        return render_template('auth_cars.html', response=response, lot_name=lot_name, classactive_canstand="class=active")


@app.route('/<lang_code>/dynamic_select', methods=['POST', 'GET'])
def dynamic_select():
    place_name = request.json['place']
    place = db_session.query(ParkingPlace.name).filter(ParkingPlace.name == place_name).all()
    if place == []:
        return jsonify(response='None')
    else:
        return jsonify(response='OK')


@app.route('/<lang_code>/log', methods=['GET', 'POST'])
def log_in():
    data = ''    
    return render_template('log.html', classactive_log="class=active")


@app.route('/<lang_code>/maps', methods=['GET', 'POST'])
def maps():
    return render_template('maps.html', classactive_maps="class=active")


@app.route('/<lang_code>/welcome', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html', classactive_welcome="class=active")


@app.route('/maps_ajax_info', methods=['GET', 'POST'])
def maps_ajax():
    return 'aaaaaaa_info'


@app.route('/<lang_code>/find', methods=['GET', 'POST'])
def find_place():
    if request.method == 'POST':
        return render_template('response_aval_place.html', lots=get_priced_parking_lot(request.json['l_price'], request.json['h_price']), classactive_log ="class=active")
    elif request.method == 'GET': return render_template('find_place.html', classactive_log="class=active")


@app.route('/<lang_code>/time_left', methods=['GET', 'POST'])
def time_left():
    cost = request.json['cost']
    place_id = request.json['place']
    est_time = calculate_estimated_time(datetime.now(), int(cost), place_id)
    if est_time:
        return est_time.strftime("%H:%M:%S %Y-%m-%d")
    else:
        return ''


if __name__ == '__main__':
    init_db()
    app.run(debug=True, use_reloader=False)