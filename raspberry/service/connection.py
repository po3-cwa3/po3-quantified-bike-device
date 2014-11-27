import json
import time
import logging
import threading

from socketIO_client import SocketIO


logging.basicConfig()

__author__ = 'fkint'


class Connection:
    def __init__(self, application, server, port):
        self.application = application
        self.server = server
        self.port = port
        self.connection_opened = False
        self.socket = None
        self.thread = None

    def start(self):
        self.thread = threading.Thread(name="connection thread", target=self.action)
        self.thread.daemon = True
        self.thread.start()

    def send_data(self, data, trip_id):
        if not self.has_connection():
            print("no connection, dropping data")
            return
        to_send = {'_id': trip_id, "sensorData": data}
        #print("sending data: "+str(data))
        print("sending data for trip ", trip_id)
        try:
            self.socket.emit('rt-sensordata', json.dumps(to_send))
        except SocketIO.ConnectionError:
            print("connection error while sending data!")

    def open_connection(self):
        self.socket = SocketIO(self.server, self.port)
        self.socket.on('server_message', self.on_response)
        self.connection_opened = True

    def close_connection(self):
        self.socket.disconnect()

    def start_trip(self):
        data = {'purpose': 'realtime-sender', 'groupID': self.application.group_id, 'userID': self.application.user_id}
        print("starting bike trip")
        try:
            self.socket.emit('start', json.dumps(data))
        except SocketIO.ConnectionError:
            print("connection error while starting trip")

    def stop_trip(self):
        data = {'_id': self.application.data_store.current_trip.get_id(), "meta": None}
        print("stopping bike trip!")
        try:
            self.socket.emit('endBikeTrip', json.dumps(data))
        except SocketIO.ConnectionError:
            print("connection error while ending bike trip")

    def on_response(self, *args):
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
            print("error: ", parsed)
            f=open("error.log","w")
            f.write(str(parsed))
            f.write("\n\n\n\n")
            f.close()

    def has_connection(self):
        return self.connection_opened and self.socket.connected

    def action(self):
        while True:
            # print("connected: "+str(self.connection_opened and self.socket.connected))
            if self.has_connection():
                self.socket.wait(.5)
            else:
                try:
                    self.open_connection()
                    time.sleep(.1)
                except ValueError:
                    print("value error")
