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
        'car': 'car',
        'leave_before': 'time',
        'hourly_rate': 'rate'
    }
]


@app.route('/todo/api/v1.0/places', methods = ['GET'])
def get_tasks():
    return jsonify( { 'places': places } )

@app.route('/todo/api/v1.0/transact', methods = ['POST'])
def create_profile():
    try:
        transaction = {
            'transaction_id': transactions[-1]['transaction_id'] + 1,
            'place_id': request.json.get('place_id', ''),
            'cost': request.json.get('cost', ''),
            'leave_before': request.json.get('leave_before', ''),
            'hourly_rate': request.json.get('hourly_rate'), 
            'result': True
        }
        place = {
            'place_id': places[-1]['place_id'] + 1,
            'car': 'car',
            'leave_before': request.json.get('leave_before', ''),
            'hourly_rate': request.json.get('hourly_rate'), 
        }
        transactions.append(transactions)
        places.append(place)
        return jsonify( { 'transaction': transaction } ), 201
    except:
        return jsonify( {'Error': 'Transaction not successful! Try again.'}) 

if __name__ == '__main__':
    
    app.run(debug = True)