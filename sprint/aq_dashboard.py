from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq
import requests
# Create an instance of the OpenAQ API
api = openaq.OpenAQ()

# initialize the app
APP = Flask(__name__)

# configure the database
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

############### PART 2 - BREATHE EASY WITH OPENAQ ##########################

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

####################### PART 4 - DASHBOARD TO THE FINISH ################################

def parse_records(database_records):
    parsed_records = []
    for record in database_records:
        print(record)
        parsed_record = str(record) #.__dict__
        # del parsed_record["_sa_instance_state"]
        parsed_records.append(parsed_record)
    return parsed_records

# Call data from the database to the /dashboard page
@APP.route('/dashboard')
def dashboard():

    records = Record.query.filter(Record.value>=10).all()
    
    return str(parse_records(records))



###################### PART 3 - THE DATA BELONGS IN A MODEL #################################

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'Time: {self.datetime}-------Value: {self.value}'

# sends data from an API endpoint to a SQLite database
@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db

    test = tuple_list()
    counter = 0
    for x in test:

      new_record = Record(datetime=test[counter][0], value=test[counter][1])
      DB.session.add(new_record)
      print(new_record.datetime)
      print(new_record.value)
      print(new_record)
      counter = counter + 1
    
    DB.session.commit()
    return 'Data refreshed!'