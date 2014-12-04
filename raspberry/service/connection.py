import json
import time
import logging
import threading
import datetime

from socketIO_client import SocketIO


logging.basicConfig()

__author__ = 'fkint'


class Connection:
    """
    This class manages the connection to the remote server using Websockets.
    It uses the modue socketIO_client.SocketIO.
    """
    def __init__(self, application, server, port):
        """
        Initializes the connection object.
        :param application: a reference to the current application object that manages the main thread.
        :param server: the address of the server
        :param port: the port of the server to which the program should connect
        :param sendtoarduino: the object that keeps track of the state and sends it to the Arduino (used to inform the user whether the socket is connected).
        """
        self.application = application
        self.server = server
        self.port = port
        self.connection_opened = False
        self.socket = None
        self.thread = None

    def start(self):
        """
        Starts the connection thread.
        """
        self.thread = threading.Thread(name="connection thread", target=self.action)
        self.thread.daemon = True
        self.thread.start()

    def send_data(self, data, trip_id):
        """
        Sends the given data to the remote server if a connection is available.
        :param data: the sensor data as a Python dict
        :param trip_id: the id of the trip to which this data should be added
        """
        # If no connection is available, just drop the data
        if not self.has_connection():
            print("no connection, dropping data")
            return
        # Prepare the dict to be sent to the server
        to_send = {'_id': trip_id, "sensorData": data}
        #print("sending data: "+str(data))
        print("sending data for trip ", trip_id)
        try:
            self.socket.emit('rt-sensordata', json.dumps(to_send))
        except:
            print("connection error while sending data!")

    def open_connection(self):
        """
        Initializes the connection.
        """
        self.socket = SocketIO(self.server, self.port)
        self.socket.on('server_message', self.on_response)
        self.connection_opened = True

    def close_connection(self):
        """
        Closes the connection.
        """
        self.socket.disconnect()

    def start_trip(self):
        """
        Asks the server to start a new trip.
        """
        data = {'purpose': 'realtime-sender', 'groupID': self.application.group_id, 'userID': self.application.user_id}
        print("starting bike trip")
        try:
            self.socket.emit('start', json.dumps(data))
        except:
            print("connection error while starting trip")

    def stop_trip(self):
        """
        Asks the server to stop the current trip.
        """
        data = {'_id': self.application.data_store.current_trip.get_id(), "meta": None}
        print("stopping bike trip!")
        try:
            self.socket.emit('endBikeTrip', json.dumps(data))
        except:
            print("connection error while ending bike trip")

    def on_response(self, *args):
        """
        Handles the responses received from the server.
        """
        parsed = args[0]
        if "Connection accepted. Ready to receive realtime data." in parsed:
            self.application.trip_started(parsed['_id'])
        elif 'Data succesfully received and saved' in parsed:
            pass
        elif "bikeTrip saved to Database" in parsed:
            print("trip saved to database!")
        elif "illegal JSON data received" in parsed:
            print("saving data to database failed")
        elif u'Welcome' in parsed:
            print("Welcome! ")
        else:
            print("error: ", str(parsed)[:100])
            f=open("error.log","a")
            f.write(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
            f.write(str(parsed))
            f.write("\n\n\n\n")
            f.close()

    def has_connection(self):
        """
        Returns whether a connection to the remote server is available.
        """
        return self.connection_opened and self.socket.connected

    def action(self):
        """
        This function is executed in the connection thread.
        """
        while True:
            # print("connected: "+str(self.connection_opened and self.socket.connected))
            if self.has_connection():
                self.socket.wait(.5)
                # Notify the Arduino that a network connection is available.
            else:
                try:
                    # No connection is available, try to initialize one
                    self.open_connection()
                    time.sleep(.1)
                except ValueError:
                    print("value error")
