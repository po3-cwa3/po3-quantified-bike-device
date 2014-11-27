import MySQLdb
import datetime
import time
import json
from socketIO_client import SocketIO
import config
import images

class BatchUpload:
    def __init__(self, disabled_trips, hostname=config.local_host, username=config.local_database_username, password=config.local_database_password, database_name=config.local_database_name, server=config.remote_hostname, port=config.remote_port, user_id=config.user_id):
        self.disabled_trips = disabled_trips
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
        self.done = False
        self.open_connection()
        self.succes = True

    def open_connection(self):
        try:
            self.socket = SocketIO(self.server, self.port)
            self.socket.on('server_message', self.on_response)
        except:
            print "error in open connection"
            self.ready=True
            self.success=False

    def start(self):
        data = {'purpose': 'batch-sender', 'groupID': 'cwa3', 'userID': self.user_id}
        f=open("error.batchupload.log","a")
        f.write("started: "+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
        f.write(str(json.dumps(data)))
        f.write("\n\n\n\n")
        f.close()
        self.socket.emit('start', json.dumps(data))


    def on_response(self, *args):
        parsed = args[0]
        print "got response: ", parsed

        f=open("error.batchupload.log","a")
        f.write("received: "+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
        f.write(str(json.dumps(data)))
        f.write("\n\n\n\n")
        f.close()
        if "Connection accepted. Ready to receive batch data." in parsed:
            #print("ready to receive batch data!")
            self.retrieve_data()
        elif "Added trip" in parsed:
            self.trips_left -= 1
            if self.trips_left == 0:
                self.ready = True
        else:
            print("error: ", parsed)

            f=open("error.batchupload.log","a")
            f.write("error: "+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
            f.write(str(parsed))
            f.write("\n\n\n\n")
            f.close()
                
    def retrieve_data(self):
        print "start batch upload"
        #con = connection.Connection('dali.cs.kuleuven.be',8080)
        #self.start_trip()
        query = "SELECT * FROM Trips"
        cursor = self.db.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        to_send = []
        for index in results:
            print "will try to batch-upload trip ", index[0]
            if int(index[0]) in self.disabled_trips:
                continue
            print "not disabled"
            self.trips_left+=1
            query = "SELECT * FROM Images WHERE Trip = "+str(int(index[0]))
            cursor.execute(query)
            data = cursor.fetchall()
            for d in data:
                print d
                images.send_to_server(d[1], str(int(index[0])), self.user_id)
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

        f=open("error.batchupload.log","a")
        f.write("sending: "+str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
        f.write(str(json.dumps(to_send)))
        f.write("\n\n\n\n")
        f.close()
        self.socket.emit('batch-tripdata', json.dumps(to_send))
        self.done=True
        time.sleep(5)
        self.done=False

if __name__ == "__main__":
    B = BatchUpload('localhost', 'QB_CWA3', 'CEeT9cPFSnPExMzQ', 'QuantifiedBike','dali.cs.kuleuven.be',8080)
    B.start()

    while not B.ready:
        B.socket.wait_for_callbacks(seconds=5)
