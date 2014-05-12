# -*- coding: utf-8 -*-
import os
from services import * 
from datetime import datetime, timedelta
from models import *
from database import db_session, init_db
from flask.ext.babel import *
from flask import *
from flask import Flask, request, render_template, jsonify, json, redirect, url_for
import re
from functools import wraps


app.secret_key='my key'


def func_hash(parameter):
    hash_object = hashlib.sha384(parameter)
    table_hash = hash_object.hexdigest()
    return table_hash

import csv as csv
import hashlib
with open('users.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
       print func_hash(row[1])

with open('users.csv', 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    data = [['Userneme', 'hash_password', 'role'],
            ['Olya', func_hash('Olya'), 'admin'],
            ['Stas', func_hash('Stas'), 'admin'],
            ['Dima', func_hash('Dima'), 'admin'],
            ['Kyrylo', func_hash('Kyrylo'), 'admin'],
            ['Lubchyk', func_hash('Lubchyk'), 'inspector'],
            ['Sashko', func_hash('Sashko'), 'inspector'],
            ]
    a.writerows(data)

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwrags):
        if 'logged_in' in session:
            return test(*args, **kwrags)
        else:
            #flash('You need to login at first')
            error = 'You need to login at first'
            #return redirect(url_for('log'))
            return render_template('log.html', error=error)
    return wrap


def check_user_info(user_login, user_password):
    with open('users.csv', 'rb') as fp:
        reader = csv.reader(fp)
        for row in reader:
            if row[0]==user_login and row[1]==user_password:
                session['logged_in'] = True
                session['name'] = row[2]


