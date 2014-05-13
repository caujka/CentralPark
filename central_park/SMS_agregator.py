# -*- coding: utf-8 -*-
from hashlib import md5
import requests
import re
from flask import json
credentials = {
    "sms_id": "",
    "sms_body": "",
    "site_service_id": "",
    "user_num": "",
    "num": "",
    "cpref": "",
    "operator_id": "",
    "operator_name": "",
    "sms_price": "",
    "sms_currency": "",
    "partner_cost": "",
    "partner_currency": "",
    "secret_key": "",
}
'''
credentials['sms_id'] = raw_input("Please, enter sms_id: ")
credentials['sms_body'] = raw_input("Please, enter sms_body in format 'XX#parking_place#car_number': ")
credentials['site_service_id'] = raw_input("Please, enter site_service_id: ")
credentials['user_num'] = raw_input("Please, enter user_num: ")
credentials['num'] = 1222
credentials['operator_id'] = 1
credentials['operator_name'] = "operator_name"
credentials['sms_price'] = raw_input("Please, enter sms_price: ")
credentials['sms_currency'] = "UAH"
credentials['partner_cost'] = credentials['sms_price']
credentials['partner_currency'] = "UAH"

'''
credentials['sms_id'] = 1
credentials['sms_body'] = "ed#name01#aaaa111222dd"
credentials['site_service_id'] = 12
credentials['user_num'] = 2343245325
credentials['num'] = 1222
credentials['operator_id'] = 1
credentials['operator_name'] = "operator_name"
credentials['sms_price'] = 15
credentials['sms_currency'] = "UAH"
credentials['partner_cost'] = credentials['sms_price']
credentials['partner_currency'] = "UAH"


secret_key = md5()
secret_key.update(str(credentials['sms_id']) + credentials['sms_body'] +
                  str(credentials['site_service_id']) + str(credentials['operator_id']) +
                  str(credentials['num']) + str(credentials['sms_price']) + "SMSCentralPark")

credentials['secret_key'] = re.escape(secret_key.hexdigest())

r = requests.post("http://127.0.0.1:5000/en/sms_pay_request", credentials)
response = json.loads(r.content)

if response['error'] == 0:
    credentials_submit = {
        "sms_id": credentials['sms_id'],
        "status": 1,
        "user_num": credentials['user_num'],
        "site_service_id": credentials['site_service_id']
    }
    print "success"
    r = requests.post("http://127.0.0.1:5000/en/sms_pay_submit", credentials_submit)



