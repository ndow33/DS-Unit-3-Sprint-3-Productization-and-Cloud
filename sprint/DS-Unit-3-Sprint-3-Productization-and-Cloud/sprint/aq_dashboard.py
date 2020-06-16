from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq
import requests
# connects to the api
api = openaq.OpenAQ()

# initialize the app
APP = Flask(__name__)

# configure the database
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

# define a function that will return a list of date time and value tuples
def tuple_list():
  status, body = api.measurements(city='Los Angeles', parameter='pm25')
  body_result = body["results"]
  
  test_list = []
  
  counter = 0
  for x in body_result:
    utc_date = body_result[counter]['date']['utc']
    value = body_result[counter]['value']
    combo = [utc_date, value]
    test_list.append(combo)
    counter = counter + 1
    
  return test_list

# Base route
@APP.route('/')
def root():
  # uses the function defined above to return a list of tuples as a string
    test = tuple_list()    
    return str(test)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'TODO - write a nice representation of Records'

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    db_list = tuple_list()

    DB.session.commit()
    return 'Data refreshed!'