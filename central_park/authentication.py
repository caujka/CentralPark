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
from create_file_users import *


app.secret_key='my key'

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwrags):
        if 'logged_in' in session:
            return test(*args, **kwrags)
        else:
            error = 'You need to login at first'
            return render_template('log.html', error=error)
    return wrap


def check_user_info(user_login, user_password):
    with open('users.csv', 'rb') as fp:
        reader = csv.reader(fp)
        for row in reader:
            if row[0]==user_login and row[1]==user_password:
                session['logged_in'] = True
                session['role'] = row[2]



