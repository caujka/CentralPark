#!/usr/bin/python
from flask import Flask, jsonify, request

app = Flask(__name__)

transactions = [
    {
        'transaction_id': 1,
        'place_id': u'place_id',
        'car': 'car',
        'cost' : u'UAH',
        'leave_before' :u'date',
        'hourly_rate': u'rate', 
        'result': 'result'
    }
]
places = [
    {
        'place_id': 1,
        'car': [{'car_number': 'leave_before'}],
        'hourly_rate': '10',
    }
]


@app.route('/todo/api/v1.0/places', methods = ['GET'])
def get_places():
    for place in places:
        if request.json.get('place_id', '') == place['place_id']:
            return jsonify( { 'place': place })

@app.route('/todo/api/v1.0/transact', methods = ['POST'])
def trasaction():
    for place in places:
        error_flag = False
        if request.json.get('place_id', '') == place['place_id']:
            transaction = {
                'transaction_id': int(transactions[-1]['transaction_id']) + 1,
                'place_id': request.json.get('place_id', ''),
                'car_number': request.json.get('car', ''),
                'leave_before': request.json.get('leave_before', ''),
                'cost': request.json.get('cost', ''),
                'hourly_rate': request.json.get('hourly_rate'), 
                'result': True
            }
            place['car'].append({request.json.get('car_number', ''): request.json.get('leave_before', ''),})
            transactions.append(transaction)
            error_flag = True
            break
    if(error_flag) :
        return jsonify( { 'transaction': transaction } ), 201 
    else:             
        return jsonify( {'Error': 'Transaction is not successful! There is no such place in db. Try again.'}) 

if __name__ == '__main__':
    app.run(debug = True)