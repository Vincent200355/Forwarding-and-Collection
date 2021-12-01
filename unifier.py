import json
import connection as con
from datetime import datetime, timedelta
database = con.Connection()

def handle_unique(endpoint, obj, record):
  '''
  this Methode defines the action, that
  is being made after unifier returns
  FALSE for comparison if a data object
  is being found in the database
  '''
  database.writeRecord(endpoint, obj, record)

def handle_duplicate(endpoint, record, id):
  '''
  This method defines the action that
  is being made, after unifier returns
  a list of ids matching the data object
  that was searched in the database. The
  objects matching this id are getting
  updated with the record object.
  '''
  database.update(endpoint, record, id)

def create_ob_record(observedAt, endpoint):
    record = {
      "observedAt": observedAt,
      "validUntil": observedAt + endpoint.interval(),
      "outdated": 0,
      "reported": 0
      }
    return record
   
def unify(endpoint, observedAt, jsonObj):
  '''
  This method searches for an object
  of the given jsonObj list  inside 
  the database. In case it matches the
  object, it returns a list of matching
  ids. In this case 'handle_duplicate'
  is called. In case it doesnt find a 
  match it returns FALSE and 'handle_unique'
  is called
  '''
  for obj in jsonObj:
    res = database.read(endpoint.name(), obj)
    record = create_ob_record(observedAt, endpoint)
    if res == False:      
      handle_unique(endpoint.name(), obj, record)
    else:
      try:
        for id in res:
          handle_duplicate(endpoint.name(), record, id)
      except Exception as e:
        print(e)
        print(type(e))
