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
        'car': '',
        'leave_before': '',
        'hourly_rate': '',
    }
]


@app.route('/todo/api/v1.0/places', methods = ['GET'])
def get_places():
    return jsonify( { 'places': places } )

@app.route('/todo/api/v1.0/transact', methods = ['POST'])
def trasaction():
    for place in places:
        error_flag = False
        if request.json.get('place_id', '') == place['place_id']:
            transaction = {
                'transaction_id': transactions[-1]['transaction_id'] + 1,
                'place_id': request.json.get('place_id', ''),
                'car': request.json.get('car', ''),
                'cost': request.json.get('cost', ''),
                'hourly_rate': request.json.get('hourly_rate'), 
                'result': True
            }
            parking_place = {
                'place_id': request.json.get('place_id', ''),
                'come_after': request.json.get('come_after', ''),
                'leave_before': request.json.get('leave_before', ''),
                'car': request.json.get('car', ''),
                'hourly_rate': request.json.get('hourly_rate'), 
            }
            transactions.append(transactions)
            places.append(parking_place)
            error_flag = True
            break
    if(error_flag) :
        return jsonify( { 'transaction': transaction, 'parking_place': parking_place } ), 201 
    else:             
        return jsonify( {'Error': 'Transaction is not successful! There is no such place in db. Try again.'}) 

if __name__ == '__main__':
    app.run(debug = True)