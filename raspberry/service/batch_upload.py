import MySQLdb
import datetime
import time
import json
from socketIO_client import SocketIO
import config
import images

class BatchUpload:
    def __init__(self, hostname=config.local_host, username=config.local_database_username, password=config.local_database_password, database_name=config.local_database_name, server=config.remote_hostname, port=config.remote_port, user_id=config.user_id):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database_name = database_name
        self.server = server
        self.port = port
        self.user_id = user_id
        self.trip_started = False
        self.db = MySQLdb.connect(host=self.hostname, user=self.username, passwd=self.password, db=self.database_name)
        self.socket = None
        self.ready = False
        self.trips_left = 0
        self.open_connection()

    def open_connection(self):
        self.socket = SocketIO(self.server, self.port)
        self.socket.on('server_message', self.on_response)

    def start(self):
        data = {'purpose': 'batch-sender', 'groupID': 'cwa3', 'userID': self.user_id}
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
            query = "SELECT * FROM Images WHERE Trip = "+str(int(index[0]))
            cursor.execute(query)
            data = cursor.fetchall()
            for d in data:
                images.send_to_server(d.ImageName, str(int(index[0])), self.user_id)
            query = "DELETE FROM Images WHERE Trip = "+str(int(index[0]))
            cursor.execute(query)
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

if __name__ == "__main__":
    B = BatchUpload('localhost', 'QB_CWA3', 'CEeT9cPFSnPExMzQ', 'QuantifiedBike','dali.cs.kuleuven.be',8080)
    B.start()

    while not B.ready:
        B.socket.wait_for_callbacks(seconds=5)