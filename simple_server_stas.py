#!/usr/bin/python
from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {
        'id': 1,
        'login': u'root',
        'first_name' : u'',
        'last_name' :u'',
        'password': u'toor', 
        'isAdmin': True,
        'isInspector': False
    },
    {
         'id': 2,
        'login': u'varyag',
        'first_name' : u'Stas',
        'last_name' : u'Breslavskyi',
        'password': u'ololololo', 
        'isAdmin': False,
        'isInspector': False
    }
]

@app.route('/todo/api/v1.0/users', methods = ['GET'])
def get_tasks():
    return jsonify( { 'users': users } )

@app.route('/todo/api/v1.0/signin', methods = ['POST'])
def create_profile():
    user = {
        'id': users[-1]['id'] + 1,
        'login': request.json['login'],
        'first_name': request.json.get('first_name', ''),
        'last_name': request.json.get('last_name', ''),
        'password': request.json.get('password'), 
        'isAdmin': False,
        'isInspector': False
    }
    users.append(user)
    return jsonify( { 'user': user } ), 201

if __name__ == '__main__':
    app.run(debug = True)