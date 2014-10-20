import MySQLdb
import datetime
import time
import json
from socketIO_client import SocketIO


class BatchUpload:
    def __init__(self, hostname, username, password, database_name, server, port):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database_name = database_name
        self.server = server
        self.port = port
        self.trip_started = False
        self.db = MySQLdb.connect(host=self.hostname, user=self.username, passwd=self.password, db=self.database_name)
        self.socket = None
        self.ready = False
        self.trips_left = 0
        self.open_connection()

    def open_connection(self):
        self.socket = SocketIO(self.server, self.port)
        self.socket.on('server_message', self.on_response)

    def start_trip(self):
        data = {'purpose': 'batch-sender', 'groupID': 'cwa3', 'userID': 'r0451433'}
        self.socket.emit('start', json.dumps(data))

    def on_response(self, *args):
        parsed = args[0]
        print "got response: ", parsed
        if "Connection accepted. Ready to receive batch data." in parsed:
            #print("ready to receive batch data!")
            self.retrieve_data()
        elif "Added trip" in parsed:
            self.trips_left -= 1
            if self.trips_left == 0:
                self.ready = True
        else:
            print("error: ", parsed)
                
    def retrieve_data(self):
        #con = connection.Connection('dali.cs.kuleuven.be',8080)
        #self.start_trip()
        query = "SELECT * FROM Trips"
        cursor = self.db.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        to_send = []
        for index in results:
            self.trips_left+=1
            query = "SELECT * FROM Data WHERE Trip = " + str(int(index[0]))
            cursor.execute(query)
            data = cursor.fetchall()
            trip_data = {'startTime':datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S"),'endTime':datetime.datetime.fromtimestamp(time.time()+1).strftime("%Y-%m-%d %H:%M:%S"),'groupID':'cwa3','userID':'r0451433','sensorData':[],'meta':{}}
            for d in data:
                trip_data['sensorData'].append(json.loads(d[2]))
            to_send.append(trip_data)
            query = "DELETE FROM Data WHERE Trip = "+str(int(index[0]))
            cursor.execute(query)
            query = "DELETE FROM Trips Where Id = "+str(int(index[0]))
            cursor.execute(query)
            self.db.commit()
        print("json to send: "+json.dumps(to_send))
        self.socket.emit('batch-tripdata', json.dumps(to_send))

B = BatchUpload('localhost', 'QB_CWA3', 'CEeT9cPFSnPExMzQ', 'QuantifiedBike','dali.cs.kuleuven.be',8080)
B.start_trip()

while not B.ready:
    B.socket.wait_for_callbacks(seconds=5)