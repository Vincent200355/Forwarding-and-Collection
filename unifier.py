import json
import connection as con
from datetime import datetime, timedelta
database = con.Connection()

record = {
  "observedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
  "validUntil": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
  "outdated": 0,
  "reported": 0
  }
with open('test.json') as f:
  lines = f.read()
data = json.loads(lines)


def handle_unique(tablename, obj, obRec):
  '''
  this Methode defines the action, that
  is being made after unifier returns
  FALSE for comparison if a data object
  is being found in the database
  '''
  database.writeRecord(tablename, obj, obRec)

def handle_duplicate(tablename, obRec, id):
  '''
  This method defines the action that
  is being made, after unifier returns
  a list of ids matching the data object
  that was searched in the database. The
  objects matching this id are getting
  updated with the record object.
  '''
  database.update(tablename, obRec, id)

def unify(tablename, jsonObj, obRec):
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
    res = database.read(tablename, obj)
    if res == False:
      handle_unique(tablename, obj, obRec)
    else:
      try:
        for id in res:
          handle_duplicate(tablename, obRec, id)
      except Exception as e:
        print(e)
        print(type(e))


#Test
unify("FLIGHTPLAN", data, record)
