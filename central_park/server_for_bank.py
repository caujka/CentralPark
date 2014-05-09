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
@app.route('/server_url', methods=['POST', 'GET'])
def banking_server():    
    #print "----------------------", json.loads(request.body.read())
    print "--------------------1", request.json.get('amt')
    return redirect('http://localhost:5000/return_url', code=302)
    #print "--------------------1", request.json
    #print "--------------------2", request.form.get('amt')
    #print "--------------------3", request.values.get('amt')
    #print "--------------------4", request.form["amt"]
    #print "--------------------5", request.json['amt']

if __name__ == '__main__':
    #init_db()
    app.run(debug=True, use_reloader=False, port=5002)