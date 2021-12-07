import mysql.connector
import credentials as creds
# import endpoints as endp

'''
    Connect to database and execute custom requests
'''
class Connection:

    ''' Constructor
        Creates a connection to the database specified in credentials.py

        Keyword arguments: none
    ''' 
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(user=creds.MYSQL_USER, password=creds.MYSQL_PASSWORD, host=creds.MYSQL_HOST, database=creds.MYSQL_DATABASE, port=creds.MYSQL_PORT)
            print("Successfully connected to " + creds.MYSQL_DATABASE)
        except Exception as err:
            print ("Oops! An exception has occured:", err)
            print ("Exception TYPE:", type(err))
        
    '''
        Close the database connection.
        
        Keyword arguments: none
    '''
    def close(self):
        self.connection.close()

    '''
        Execute a query with custom arguments.
        
        Keyword arguments:
            - query: String -- mysql query using %s or %(name) as placeholder for arguments
            - arguments: Dictionary || List -- arguments as list (if query uses %s) or as dicitionary (if query uses %(name))
    '''
    def execute(self, query, arguments):
        try:
            cursor = self.connection.cursor(buffered=True)
            cursor.execute( query, arguments )
            result = cursor
            return result
        except Exception as err:
            print ("Oops! An exception has occured:", err)
            print ("Exception TYPE:", type(err))
            return False

    '''
        Get table name corresponding to observer-keyword
        
        Keyword arguments:
            - observer: String -- flightplan || radar || terminal || it || observer || error
    '''
    def table(_, observer):
        if(observer.lower() == 'flightplans'):
            return 'FlightplanEntry'
        elif(observer.lower() == 'radar'):
            return 'RadarEntry'
        elif(observer.lower() == 'terminal'):
            return 'TerminalEntry'
        elif(observer.lower() == 'it'):
            return 'ITEntry'
        elif(observer.lower() == 'observer'):
            return 'ObservedEntry'
        elif(observer.lower() == 'error'):
            return 'ObservationError'
        else:
            print("Endpoint is not implemented.")
            return False

    '''
        Execute a SELECT query for observer with custom arguments.
        
        Keyword arguments:
            - observer: Endpoint
            - arguments: Dictionary -- dictionary with arguments for WHERE-Clause. {key1: value1, key2: value2} => WHERE key1 = value1 AND key2 = value2
        Return value:
            - Boolean || List -- True -> Found matching record || List -> list of id's with matching data
    '''
    def read(self, observer, arguments):
        if(self.table(observer.name())):
            query = 'SELECT * FROM ' + self.table(observer.name()) + " WHERE " + ' AND '.join([k + "=" + "%(" + k + ")s" for k in arguments.keys()]) + ";"
            result = self.execute(query, arguments)
            if(result==False or result == []):
                return False
            else: 
                id = []
                for item in result.fetchall():
                    id.append(item[0])
                return id
                

    '''
        Execute a INSERT query for observer with custom arguments.
        
        Keyword arguments:
            - observer: Endpoint
            - arguments: Dictionary -- dictionary with arguments for INSERT {key1: value1, key2: value2} => INSERT INTO OBSERVER (key1, key2) VALUES(value1, value2)
    '''
    def write(self, observer, arguments):
        observerDatabase = observer if isinstance(observer, str) else observer.name()
        if(self.table(observerDatabase)):
            query = 'INSERT INTO ' + self.table(observerDatabase) + "(" + ', '.join(map(str, arguments.keys())) + ") " + 'VALUES (%(' + ')s, %('.join(map(str, arguments.keys())) + ")s );"
            result = self.execute(query, arguments)
            self.connection.commit()
            return result
    
    '''
        Execute a UPDATE query in ObservationEntry.
        
        Keyword arguments:
            - observer: Endpoint
            - arguments: Dictionary -- dictionary with arguments for UPDATE {key1: value1, key2: value2} => SET key1 = value1, key2 = value2
            - id: Integer -- id of record that should be updated
    '''
    def update(self, observer, arguments, id):
        if(self.table(observer.name())):
            query = 'UPDATE ' + self.table("observer") + ' SET ' + ', '.join([k + "=" + "%(" + k + ")s" for k in arguments.keys()]) + " WHERE id = " + str(id) + " AND observer = '" + observer.databaseName() + "';"
            self.execute(query, arguments)
            self.connection.commit()

    '''
        Execute two INSERT queries: Create a ObservationEntry and add observer-record.
        
        Keyword arguments:
            - observer: Endpoint
            - arguments: Dictionary -- dictionary with arguments for INSERT INTO flightplan/radar/terminal/it
            - observationEntry: Dictionary -- dictionary with arguments for INSERT INTO OBSERVER
    '''
    def writeRecord(self, observer, arguments, observationEntry):
        cursor = self.write("observer", {**observationEntry, **{"observer": observer.databaseName()}})
        self.write(observer, {**arguments, **{"id": cursor.lastrowid}})




###
###    TEST
###

# # Create database connection
# database = Connection()

# # data for Flightplan record
# record = {
#     "callsign":"EWG8XZ",
#     "ssr":"A1411",
#     "rules":"IS",
#     "wvc":"M",
#     "equipment":"S/S",
#     "origin":"LFPG",
#     "aircraft": "A320",
#     "eobt":1638144000000,
#     "route":"N0431F370 DH632",
#     "destination":"EDDH",
#     "eet":7200000,
#     "eta":1638371266444,
#     "status":"closed",
#     "registration":"DAAA",
#     "icao4444":"FPL-EWG8XZ/A1411-IS-A320/M-S/S-LFPG0000-N0431F370 DH632-EDDH0200-REG/DAAAA"
# }

# # data for observer record
# obRecord = {
#     "observedAt": 1638371266444,
#     "validUntil": 1638371266444,
#     "outdated": 0,
#     "reported": 0
# }

# # data for observer record
# obRecordUpdate = {
#     "observedAt": 1638371266444,
#     "validUntil": 1638371266444,
#     "outdated": 1,
#     "reported": 0
# }
# obs = endp.ENDPOINTS["flightplans"]

# # INSERT a record for observer FLIGHTPLAN
# database.writeRecord(obs, record, obRecord)

# # UPDATE ObservationEntry with observer = FLIGHTPLAN AND id = 13
# database.update(obs, obRecordUpdate, 13)

# # Search for record in FLIGHTPLAN table
# print(database.read(obs, record))

# # Close database connection
# database.close()