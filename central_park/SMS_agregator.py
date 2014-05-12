# -*- coding: utf-8 -*-
from hashlib import md5
import requests
import re

credencials = {
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
credencials['sms_id'] = raw_input("Please, enter sms_id: ")
credencials['sms_body'] = raw_input("Please, enter sms_body in format 'XX#parking_place#car_number': ")
credencials['site_service_id'] = raw_input("Please, enter site_service_id: ")
credencials['user_num'] = raw_input("Please, enter user_num: ")
credencials['num'] = 1222
credencials['operator_id'] = 1
credencials['operator_name'] = "operator_name"
credencials['sms_price'] = raw_input("Please, enter sms_price: ")
credencials['sms_currency'] = "UAH"
credencials['partner_cost'] = credencials['sms_price']
credencials['partner_currency'] = "UAH"
'''

credencials['sms_id'] = 1
credencials['sms_body'] = "ed#name01#sad"
credencials['site_service_id'] = '32sd'
credencials['user_num'] = 2343245325
credencials['num'] = 1222
credencials['operator_id'] = 1
credencials['operator_name'] = "operator_name"
credencials['sms_price'] = 23
credencials['sms_currency'] = "UAH"
credencials['partner_cost'] = credencials['sms_price']
credencials['partner_currency'] = "UAH"


secret_key = md5()
secret_key.update(str(credencials['sms_id']) + credencials['sms_body'] +
                  str(credencials['site_service_id']) + str(credencials['operator_id']) +
                  str(credencials['num']) + str(credencials['sms_price']) + "SMSCentralPark")

credencials['secret_key'] = re.escape(secret_key.hexdigest())

r = requests.post("http://127.0.0.1:5000/en/sms_pay_request", credencials)
print r.text
