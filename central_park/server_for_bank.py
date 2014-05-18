# -*- coding: utf-8 -*-
import os, requests, time
from services import * 
from datetime import datetime, timedelta
from models import *
from database import db_session, init_db
from flask.ext.babel import *
from flask import *
from flask import Flask, request, render_template, jsonify, json
import re

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


@app.route('/server_url', methods=['POST'])
def payment():
    print "--------------", request.json.get('ext_details')
    place_id = get_placeid_by_placename(request.json.get('ext_details'))
    print "---------------", place_id
    reg_cost = r'\d{1,}'
    reg_number = r'[A-Z, a-z, А-Я, а-я, 0-9]{3,10}'
    reg_place = r'[A-Z, a-z, 0-9]{1,}'

    if (re.search(reg_cost, request.json.get('amt')) and re.search(reg_place, request.json.get('ext_details'))
        and re.search(reg_number, request.json.get('details')) and int(request.json.get('amt')) > 0
        and get_placeid_by_placename(request.json.get('ext_details')) >= 0):
        cost = int(request.json.get('amt'))
        transaction = "waiting"
        create_payment_record(request.json.get('details'), place_id, cost, transaction)

        just_parked_car = is_car_already_parked_here(place_id, request.json.get('details'))
        tariff_matrix = parse_tariff_to_list(get_current_tariff_matrix(place_id))
        tariff = ""
        time_tmp = just_parked_car.activation_time
        while time_tmp.hour <= just_parked_car.expiration_time.hour:
            tariff += str(time_tmp.hour) + " hour: " + str(tariff_matrix[time_tmp.hour]) + "hrn/h; "
            time_tmp += timedelta(hours=1)

        if just_parked_car:
            credentials = {
                'car_number': just_parked_car.car_number,
                'cost': cost,
                'time_left': just_parked_car.expiration_time.strftime("%H:%M %d-%m-%Y"),
                'transaction': just_parked_car.transaction,
                'place': request.json.get('ext_details'),
                'rate': tariff
                }

            return render_template("payment_response.html", credentials=credentials)
            #return redirect("127.0.0.1:5001/banking")    - NOT IMPLEMENTED
    else:
        error = "Your data is not valid"
        return render_template("payment_response.html", error=error)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, use_reloader=False, port=5002)