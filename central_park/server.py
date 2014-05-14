# -*- coding: utf-8 -*-
import os
from database import db_session, init_db
from services import *

from flask import *

from flask import Flask, request, render_template, jsonify, json, redirect, url_for
import re
from authentication import *
from flask.ext.babel import *
from flask_babelex import Babel
from datetime import datetime, timedelta
from models import *
from hashlib import md5
import re
import logging


logging.basicConfig(filename=u"server.log",
                    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')

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


@app.route('/<lang_code>/log', methods=['GET','POST'])
def log():
    if request.method == 'GET':
        return render_template('log.html')
    if request.method == 'POST':    
        name = request.json['log']
        pas = func_hash(request.json['pass'])
        check_user_info(name, pas)
        print session['role']
        return render_template('welcome.html')


@app.route('/<lang_code>/logout')
def loggout():
    session.pop('logged_in', None)
    session.pop('name', None)
    flash("You were logged out")
    return render_template('log.html')
        
@babel.localeselector
def get_locale():   
    return g.get('current_lang', 'en')


@app.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        if request.view_args['lang_code'] not in ('en', 'de', 'uk'):
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
    return render_template('start.html')


@app.route('/<lang_code>/payment', methods=['GET', 'POST'])
def payment():
    try:
        if request.method == 'GET':
            if request.args.get('parking_place') is None:
                return render_template('payment.html', place_from_map="")
            else:
                return render_template('payment.html', place_from_map=request.args.get('parking_place'))

        else:
            place_id = get_placeid_by_placename(request.json['place'])

            reg_cost = r'\d{1,}'
            reg_number = r'[A-Z, a-z, А-Я, а-я, 0-9]{3,10}'
            reg_place = r'[A-Z, a-z, 0-9]{1,}'

            if (re.search(reg_cost, request.json['cost']) and re.search(reg_place, request.json['place'])
                    and re.search(reg_number, request.json['car_number']) and int(request.json['cost']) > 0
                    and get_placeid_by_placename(request.json['place']) >= 0):

                cost = int(request.json['cost'])
                transaction = "waiting"

                create_payment_record(request.json['car_number'], place_id, cost, transaction)
                just_parked_car = is_car_already_parked_here(place_id, request.json['car_number'])

                if just_parked_car:
                    credentials = {
                        'car_number': just_parked_car.car_number,
                        'cost': cost,
                        'time_left': just_parked_car.expiration_time.strftime("%H:%M %d-%m-%Y"),
                        'transaction': just_parked_car.transaction,
                        'place': request.json['place'],
                        'rate': get_tariff_for_parked_car(just_parked_car)
                    }
                return render_template("payment_response.html", credentials=credentials)
                #return redirect("127.0.0.1:5001/banking")    - NOT IMPLEMENTED
            else:
                error = "Your data is not valid"
                return render_template("payment_response.html", error=error)
    except BaseException:
        return render_template("payment_response.html", error=BaseException)


@app.route('/<lang_code>/history', methods=['GET', 'POST'])
def show_history():
    
    if request.method == 'GET':
        list_of_place = get_list_of_places_names()
        return render_template('history.html', place_list=list_of_place)
    
    else:
        chosen_place = request.json['place']
        date_time = request.json['date']
        actual_history = get_payment_by_date(get_placeid_by_placename(chosen_place), date_time)
        return render_template('response_history.html', history_info=actual_history)

@app.route('/stats', methods=['GET', 'POST'])
def stat():
    statistics_payment_fill()

@app.route('/<lang_code>/can_stand', methods=['GET', 'POST'])
@login_required
def can_stand():
    if request.method == 'GET':
        return render_template('chek_parking.html')
    elif request.method == 'POST':
        lot_name = request.values.get('lot_name')
        response = get_parked_car_on_lot(lot_name)
        return render_template('auth_cars.html', response=response, lot_name=lot_name, classactive_canstand="class=active")


@app.route('/<lang_code>/dynamic_select', methods=['POST', 'GET'])
def dynamic_select():
    place_name = request.json['place']
    place = db_session.query(ParkingPlace.name).filter(ParkingPlace.name == place_name).all()
    if place is [] or place is None:
        return jsonify(response='None')
    else:
        try:
            place_id = get_placeid_by_placename(place_name)
            cur_tariff = parse_tariff_to_list(get_current_tariff_matrix(place_id))
            return jsonify(response='OK', first_hour_tariff=cur_tariff[datetime.now().hour],
                           second_hour_tariff=cur_tariff[(datetime.now() + timedelta(hours=1)).hour])
        except:
            return jsonify(response='None')


@app.route('/<lang_code>/log', methods=['GET', 'POST'])
def log_in():
    return render_template('log.html', classactive_log="class=active")


@app.route('/<lang_code>/maps', methods=['GET', 'POST'])
def maps():
    return render_template('maps.html', classactive_maps="class=active")


@app.route('/<lang_code>/welcome', methods=['GET', 'POST'])
def welcome():
    return render_template('start.html', classactive_welcome="class=active")


@app.route('/maps_ajax_info', methods=['GET', 'POST'])
def maps_ajax():
    s = request.args.get('parking_name')
    return jsonify({'statistics': get_statistics_by_place(s) ,'info':"Here goes info about parking place" + s})


@app.route('/maps_ajax_marker_add', methods=['GET', 'POST'])
def maps_ajax_maker():
    return jsonify({'status': 'ok', 'position': take_parking_coord()})


@app.route('/<lang_code>/find', methods=['GET', 'POST'])
def find_place():
    if request.method == 'POST':
        return render_template('response_aval_place.html',
                               lots=get_priced_parking_lot(request.json['l_price'],
                                                           request.json['h_price']),
                               classactive_log="class=active")
    elif request.method == 'GET':
        return render_template('find_place.html', classactive_log="class=active")


@app.route('/<lang_code>/time_left', methods=['GET', 'POST'])
def time_left():
    est_time = get_estimated_time_for_given_car(request.json['car_number'],
                                                get_placeid_by_placename(request.json['place']),
                                                int(request.json['cost']))
    if est_time:
        return jsonify(time_left=est_time.strftime("%H:%M:%S %Y-%m-%d"))
    return jsonify(time_left='error')


@app.route('/<lang_code>/take_coord', methods=['GET', 'POST'])
def take_coord():
    locations = take_parking_coord()
    return jsonify(list_ofcoord=locations)


@app.route('/<lang_code>/get_payment_by_coord', methods=['GET', 'POST'])
def get_payment_by_coord():
    ls = request.json['ls']
    final_list = get_payment_by_circle_coord(ls)
    info = {}
    for cars_in_parking in final_list:
        cars = []
        for car in cars_in_parking:
            car = {
                'car_number': car[1],
                'expception_time': car[2]
            }
            cars.append(car)
        info[cars_in_parking[0][0]] = cars
    return jsonify(res=info)


#SMS paying implementation
@app.route('/<lang_code>/sms_pay_request', methods=['POST'])
def authenticate_sms_paying_request():
    if request.form['sms_id'] not in get_list_of_sms_ids():
        create_SMSHistory_record(request.form['sms_id'], request.form['site_service_id'])
        secret_key = md5()
        secret_key.update(str(request.form['sms_id']) + str(request.form['sms_body']) +
                          str(request.form['site_service_id']) + str(request.form['operator_id']) +
                          str(request.form['num']) + str(request.form['sms_price']) + "SMSCentralPark")
        if secret_key.hexdigest() == request.form['secret_key']:
            sms_body = parse_sms_content(request.form['sms_body'])
            if (sms_body is not False) and (sms_body is not None) and (sms_body['place'] in get_list_of_places_names()):
                create_payment_record(sms_body['car_number'], get_placeid_by_placename(sms_body['place']),
                                      int(request.form['sms_price']), 'sms'+str(request.form['site_service_id'])+"waiting")
                logging.info("SMS Payment request was created. Transaction: %s" % 'sms'+request.form['site_service_id']+'waiting')

                sms_response = create_text_sms_response(sms_body['place'], sms_body['car_number'], request.form['sms_price'])
                return jsonify(sms_id=request.form['sms_id'], response=sms_response, error=0)
            logging.info("SMS Payment was requested. Error in sms_body: '%s' was found" % (request.form['sms_body']))
    else:
        #log creating
        user_num = "user number: %s" % str(request.form['user_num'])
        sms_id = "sms_id: %s" % str(request.form['sms_id'])
        site_service_id = "site_service_id: &s" % str(request.form['site_service_id'])
        sms_body = "sms text: &s" % str(request.form['sms_body'])
        logging.warning("Repeated sms-paying was detected! %s %s %s %s" % (user_num, sms_id, site_service_id, sms_body))
        #--------
    return jsonify(sms_id=request.form['sms_id'], response="Fail", error=1)


@app.route('/<lang_code>/sms_pay_submit', methods=['POST'])
def submit_sms_paying_request():
    print "in sms_pay_submit"
    print "print request.form['status']=", request.form['status']
    if int(request.form['status']) == 1:
        print "in request.form['status']==1"
        payment_id = finish_sms_payment_record("sms" + request.form['site_service_id'] + "waiting")
        logging.info("Finished sms payment with id: %s" % payment_id)
    else:
        print "request.form['status']=!1"
        delete_payment_by_transaction("sms" + request.form['site_service_id'] + "waiting")
        logging.info("Sms paying was not successful. Payment record was deleted")
    return jsonify(status='Done')


if __name__ == '__main__':
    init_db()
    app.run(debug=True, use_reloader=False)
