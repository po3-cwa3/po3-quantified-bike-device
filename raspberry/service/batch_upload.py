import MySQLdb
import datetime
import time
import json
import threading

from socketIO_client import SocketIO

import config
import images


class BatchUpload:
    """
    This class manages the uploading of data temporarily stored in the local MySQL database to the remote database.
    """
    def __init__(self, disabled_trips, hostname=config.local_host, username=config.local_database_username,
                 password=config.local_database_password, database_name=config.local_database_name,
                 server=config.remote_hostname, port=config.remote_port, user_id=config.user_id):
        """
        Initialize the BatchUpload.
        :param disabled_trips: a set of ids of the trips that shouldn't be uploaded (e.g. the current trip)
        :param hostname: the hostname of the server hosting the local MySQL Database
        :param username: the username that should be used to connect to the local MySQL Database
        :param password: the password that should be used to connect to the local MySQL Database
        :param database: the name of the database in which all data is stored in the local MySQL Database
        :param server: the hostname of the remote server
        :param port: the port of the remote server
        :param user_id: the id of the user that should be used to send data to the server
        """
        self.disabled_trips = disabled_trips
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database_name = database_name
        self.server = server
        self.port = port
        self.user_id = user_id
        self.trip_started = False
        # The object managing the MySQL connection to the local database
        self.db = MySQLdb.connect(host=self.hostname, user=self.username, passwd=self.password, db=self.database_name)
        # The object managing the connection to the remote server
        self.socket = None
        self.ready = False
        self.trips_left = 0
        self.done = False
        self.open_connection()
        self.success = True
        self.current_trip = -1
        self.current_trip_images = []

    def open_connection(self):
        """
        Initializes the connection to the remote server.
        """
        try:
            self.socket = SocketIO(self.server, self.port)
            self.socket.on('server_message', self.on_response)
        except:
            print "error in open connection"
            self.ready=True
            self.success=False

    def start(self):
        """
        Starts the uploading of the data.
        The first step, executed in this function, is sending a batch-send request to the server.
        """
        data = {'purpose': 'batch-sender', 'groupID': 'cwa3', 'userID': self.user_id}
        self.socket.emit('start', json.dumps(data))

    def send_images_of_trip(self, own_id, remote_id):
        """
        Sends all images belonging to a certain trip to the server.
        """
        # Take a copy of all images stored in current_trip_images (that way a new trip can already load its images while waiting for this function to finish).
        data = self.current_trip_images[:]
        for d in data:
            print d
            images.send_to_server(d[0], remote_id, self.user_id, d[1])


    def on_response(self, *args):
        """
        Handles response sent by the server.
        :param: an array containing the arguments passed by the socket.
        """
        parsed = args[0]
        print "got response: ", parsed
        if "Connection accepted. Ready to receive batch data." in parsed:
            self.send_next_trip()
        elif "Added trip" in parsed:
            # A trip has been added
            print "trip added", parsed
            self.send_images_of_trip(self.current_trip, parsed['_id'])
            # First start sending all images of the current trip to the server
            #Try to send the next trip
            self.send_next_trip()
        else:
            print("error: ", str(parsed)[:100])

    def send_next_trip(self):
        """
        Checks if there's a trip left to be sent to the server.
        If one is available, it loads all sensor data stored in the local database.
        """
        query = "SELECT * FROM Trips"
        cursor = self.db.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        to_send = []
        for index in results:
            print "will try to batch-upload trip ", index[0]
            # Only send trips to the server that haven't been disabled at the initialization of this BatchUpload object
            if int(index[0]) in self.disabled_trips:
                continue
            self.current_trip = str(int(index[0]))
            print "this trip can be uploaded"
            query = "SELECT * FROM Data WHERE Trip = " + str(int(index[0]))
            cursor.execute(query)
            data = cursor.fetchall()
            # The global trip data
            startTime = index[1]
            endTime = index[2]
            print(startTime.strftime("%Y-%m-%d %H:%M:%S"))
            trip_data = {'startTime': startTime.strftime("%Y-%m-%d %H:%M:%S"),# datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S"),
                         'endTime': endTime.strftime("%Y-%m-%d %H:%M:%S"), #datetime.datetime.fromtimestamp(time.time() + 1).strftime("%Y-%m-%d %H:%M:%S"),
                         'groupID': 'cwa3', 'userID': 'r0451433', 'sensorData': [], 'meta': {}}
            for d in data:
                trip_data['sensorData'].append(json.loads(d[2]))
                #print "will be uploaded:", d[2]
            # Clean the local database by removing all data that is to be sent to the remote server.
            query = "DELETE FROM Data WHERE Trip = " + str(int(index[0]))
            cursor.execute(query)
            query = "SELECT ImageName, Timestamp FROM Images WHERE Trip = " + str(int(index[0]))
            cursor.execute(query)
            data = cursor.fetchall()
            self.current_trip_images = []
            # Add all image ids to current_trip_images
            for d in data:
                self.current_trip_images.append((d[0], d[1]))
            to_send.append(trip_data)
            # Clean images from database that will be set to the remote server
            query = "DELETE FROM Images WHERE Trip = " + str(int(index[0]))
            cursor.execute(query)
            # Clean this trip from the database
            query = "DELETE FROM Trips Where Id = " + str(int(index[0]))
            cursor.execute(query)
            #Commit the DELETE queries
            self.db.commit()
            break;
        cursor.close()
        if len(to_send) == 0:
            # This happens when no new trip has been found
            # It is still possible that images are being uploaded, but the trip data should've been stored on the remote server.
            # Sets the ready flag to True, so external watchers we're done uploading 
            self.ready = True
            return
        print("json to send: " + str(json.dumps(to_send))[:100])
        self.socket.emit('batch-tripdata', json.dumps(to_send))
    #
    # def image_batch(self, imagelist):
    #     """
    #     Sends the all images in imagelist to the remote server.
    #     :param imagelist: a list of tupples (photo_id, trip_id, user_id)
    #     """
    #     print "start imagebatch"
    #     for t in imagelist:
    #         print "sending 1 image"
    #         try:
    #             images.send_to_server(t[0],t[1],t[2])
    #         except:
    #             print "failed to send image ",t


#stand-alone test script
if __name__ == "__main__":
    B = BatchUpload('localhost', 'QB_CWA3', 'CEeT9cPFSnPExMzQ', 'QuantifiedBike', 'dali.cs.kuleuven.be', 8080)
    B.start()

    while not B.ready:
        B.socket.wait_for_callbacks(seconds=5)
