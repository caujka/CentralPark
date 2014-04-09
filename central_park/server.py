# -*- coding: utf-8 -*-
import os
from services import * 
from datetime import datetime, timedelta
from models import ParkingLot, ParkingPlace, PriceHistory, Payment
from flask import Flask, request, render_template, jsonify
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
    return render_template('welcome.html')


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'GET':
        lot = request.values.get('lot')
        k = db_session.query(ParkingLot.id).filter(ParkingLot.name == lot)
        return render_template('payment.html', classactive_payment="class=active", lots=get_list_of_lot(), place_list = get_list_of_places_by_lot(0) )

    else:
        min_cost = 10;

        username = request.json['name']
        cost = int(request.json['cost'])
        print request.json
        id_lot = get_lotid_by_lotname(request.json['lot_id'])
        list_id_lot = get_lots()
        list_id_plaace = get_list_of_places_by_lot(id_lot)

        reg = r'\d{1,}'
        reg_str = r'[A-Z, a-z, 0-9]{4,6}'

        if ( (re.search(reg, request.json['cost'])) and re.search(reg, request.json['lot_id']) and re.search(reg, request.json['place_id']) and (cost >= min_cost) and re.search(reg_str,request.json['car_number']) ):
            credentials = { 'username' : username,
                        'car_number' : request.json['car_number'],
                        'cost': cost,
                        'leave_before':calculate_estimated_time(int(cost),id_lot),
                        'id_place': request.json['place_id'],
                        'id_lot': request.json['lot_id'],
                        'rate': get_current_tariff_matrix(id_lot)}       
            p = Payment(credentials['car_number'], credentials['cost'], credentials['leave_before'], credentials['id_lot'], credentials['id_place'])    
            
            if (db_session.query(ParkingLot).filter(ParkingLot.id == id_lot).first().id) and p:
                db_session.add(p)
                db_session.commit()
                
                return render_template("payment_response.html", credentials=credentials)
            
        else:
            eror = "Your data is not valid"
            return render_template("payment_response.html", error=eror )


@app.route('/history', methods=['GET', 'POST'])
def show_history():
    hist = None
    if request.method == 'GET':
        return render_template('history.html', years = (2010, 2011, 2012, 2013, 2014), months = (u'Січень',u'Лютий',u'Березень',u'Квітень',u'Травень',u'Червень',u'Липень',u'Серпень',u'Вересень',u'Жовтень',u'Листопад',u'Грудень' ))
    else:
        Lot = request.values.get('Lot')
        data_time = request.values.get('date')
        actual_history = get_payment_by_date(Lot, data_time)
        
        if actual_history:
            return render_template('response_history.html', history_info = actual_history) 


@app.route('/can_stand', methods=['GET', 'POST'])
def can_stand():
    if request.method == 'GET':
        return render_template('get_cars.html', classactive_canstand="class=active", res_list=get_list_of_lot())
    elif request.method == 'POST':
        lot_name = request.json['lot_name']
        lot_id = get_lotid_by_lotname(lot_name)
        response = get_parked_car_on_lot(lot_id)
        print response
        return render_template('auth_cars.html', response=response, lot_name=lot_name, classactive_canstand="class=active", res_list=get_list_of_lot())


@app.route('/dynamic_select', methods=['POST', 'GET'])
def dynamic_select():
    lot_name = request.json['lot_id']
    lot_id = get_lotid_by_lotname(lot_name)
    list = get_list_of_places_by_lot(lot_id)
    return jsonify(response=list)


@app.route('/log', methods=['GET', 'POST'])
def log_in():
    data = ''    
    return render_template('log.html', classactive_log="class=active")


@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html', classactive_welcome="class=active")


@app.route('/find', methods=['GET', 'POST'])
def find_place():   
    if request.method == 'POST':
        return render_template('response_aval_place.html', lots=get_priced_parking_lot(request.json['l_price'], request.json['h_price']), classactive_log ="class=active")
    elif request.method == 'GET': return render_template('find_place.html', classactive_log ="class=active")
    

if __name__ == '__main__':
    init_db()
    app.run(debug=True, use_reloader=False)
