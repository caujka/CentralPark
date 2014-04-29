# -*- coding: utf-8 -*-

import os
import unittest
import tempfile
import server
from services import *
from flask import Flask, request, render_template, jsonify, redirect, url_for, abort, g
from flask.ext.babel import Babel
import database 
import flask_babel as babel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
import models
from mock import *
#from nose import with_setup


class TestQuery(unittest.TestCase):

    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    session = Session()

    def setUp(self):
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)


class TestFuncCoord(unittest.TestCase):

    def test_get_current_pakkinghistory_id(self):
        i = 1
        self.assertEqual(get_current_pricehistory_id(1), 4)

    def test_get_payment_by_circle_coord(self):
        list_id = [1, 2, 3]
        self.assertIsInstance(get_payment_by_circle_coord(list_id), list, "get_payment_by_circle_coord function returns incorrent value.")


    def test_take_parking_coord(self):
        mock_obj = Mock()
        mock_obj.locations = [(49.56263, 27.033), (55.02553, 24.2325), (50.20003, 24.03020)]
        value = type(mock_obj.locations)
        self.assertIsInstance(take_parking_coord(), value, "function returns incorect values")

class TestwithDB(unittest.TestCase):

    def test_get_placeid_by_placename(self):
        names = ['name01', 'name02', 'name03', 'name04', 'name05']
        self.assertEqual(get_placeid_by_placename(names[0]), 0)
        self.assertEqual(get_placeid_by_placename(names[1]), 1)
        self.assertEqual(get_placeid_by_placename(names[2]), 2)
        self.assertEqual(get_placeid_by_placename(names[3]), 3)
        self.assertEqual(get_placeid_by_placename(names[4]), 4)



class TestPayment(unittest.TestCase):

    def test_get_payment_by_date(self):
        num_place = 5
        date_tmp = date.today()
        self.assertIsInstance(get_payment_by_date(num_place, str(date_tmp)), list, "function get_payment_by_date returns wrong result") 

    def test_create_payment_record(self):
        obj = ('AA6645',5, 30)
        self.assertTrue(create_payment_record(obj))



if __name__ == '__main__':
    unittest.main()