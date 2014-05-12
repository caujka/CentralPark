import requests

print requests.post("http://127.0.0.1:5000/en/sms_pay_request", {"sms_id": 1}).text
