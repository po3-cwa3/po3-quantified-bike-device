import json
import threading
import time

from socketIO_client import SocketIO


__author__ = 'fkint'


class Connection:
    def __init__(self, application, server, port):
        self.application = application
        self.server = server
        self.port = port
        self.connection_opened = False
        self.socket = None

    def send_data(self, data, trip_id):
        to_send = {'_id': trip_id, "sensorData": data}
        self.socket.emit('rt-sensordata', json.dumps(to_send))

    def open_connection(self):
        self.socket = SocketIO(self.server, self.port)
        self.socket.on('server_message', self.on_response)
        self.connection_opened = True

    def close_connection(self):
        self.socket.disconnect()

    def start_trip(self):
        data = {'purpose': 'realtime-sender', 'groupID': self.application.group_id, 'userID': self.application.user_id}
        self.socket.emit('start', json.dumps(data))

    def stop_trip(self):
        data = {'_id': self.application.data_store.current_trip.get_id(), "meta": None}
        self.socket.emit('endBikeTrip', json.dumps(data))

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

    def action(self):
        if self.connection_opened and self.socket.connected:
            self.socket.wait(.5)
        else:
            time.sleep(.1)