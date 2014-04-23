# -*- coding: utf-8 -*-
import os
from services import * 
from datetime import datetime, timedelta
from models import ParkingPlace, PriceHistory, Payment
from database import db_session, init_db
from flask.ext.babel import *
from flask_babelex import *
from flask import *


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
        return render_template('payment.html', classactive_payment="class=active", places=get_list_of_places())

    else:
        username = request.json['name']
        cost = int(request.json['cost'])
        print request.json
        id_lot = get_placeid_by_placename(request.json['lot_id'])

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


@app.route('/<lang_code>/history', methods=['GET', 'POST'])
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


@app.route('/<lang_code>/can_stand', methods=['GET', 'POST'])
def can_stand():
    if request.method == 'GET':
        return render_template('get_cars.html', classactive_canstand="class=active", res_list=get_list_of_places())
    elif request.method == 'POST':
        lot_name = request.json['lot_name']
        lot_id = get_lotid_by_lotname(lot_name)
        response = get_parked_car_on_lot(lot_id)
        print response
        return render_template('auth_cars.html', response=response, lot_name=lot_name, classactive_canstand="class=active", res_list=get_list_of_lot())


@app.route('/<lang_code>/dynamic_select', methods=['POST', 'GET'])
def dynamic_select():
    place_name = request.json['place']
    place = db_session.query(ParkingPlace.name).filter(ParkingPlace.name == place_name)
    if place == []:
        return jsonify(response='None')
    else:
        return jsonify(response='OK')


@app.route('/<lang_code>/log', methods=['GET', 'POST'])
def log_in():
    data = ''    
    return render_template('log.html', classactive_log="class=active")


@app.route('/<lang_code>/welcome', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html', classactive_welcome="class=active")


@app.route('/<lang_code>/find', methods=['GET', 'POST'])
def find_place():   
    if request.method == 'POST':
        return render_template('response_aval_place.html', lots=get_priced_parking_lot(request.json['l_price'], request.json['h_price']), classactive_log ="class=active")
    elif request.method == 'GET': return render_template('find_place.html', classactive_log ="class=active")
    

if __name__ == '__main__':
    init_db()
    app.run(debug=True, use_reloader=False)
