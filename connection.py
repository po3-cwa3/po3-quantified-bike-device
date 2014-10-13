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
        self.trip_started = False
        self.trip_id = None
        self.socket = None
        self.thread = None

    def send_data(self, data):
        to_send = {'_id': self.trip_id, "sensorData": data}
        self.socket.emit('rt-sensordata', json.dumps(to_send))

    def open_connection(self):
        self.socket = SocketIO(self.server, self.port)
        self.socket.on('server_message', self.on_response)
        self.connection_opened = True
        self.thread = threading.Thread(name='connection', target=self.action)
        self.thread.start()

    def close_connection(self):
        self.socket.disconnect()

    def start_trip(self):
        data = {'purpose': 'realtime-sender', 'groupID': self.application.group_id, 'userID': self.application.user_id}
        self.socket.emit('start', json.dumps(data))

    def stop_trip(self):
        data = {'_id': self.trip_id, "meta": None}
        self.socket.emit('endBikeTrip', json.dumps(data))
        self.trip_started = False

    def live_trip_active(self):
        return self.connection_opened and self.trip_started

    def on_response(self, *args):
        parsed = args[0]
        if "Connection accepted. Ready to receive realtime data." in parsed:
            self.trip_started = True
            self.trip_id = parsed['_id']
            print("trip started, id = ", self.trip_id)
        elif 'Data succesfully received and saved' in parsed:
            pass
        elif "bikeTrip saved to Database" in parsed:
            self.trip_started = False
            print("trip saved to database!")
        elif "illegal JSON data received" in parsed:
            print("saving data to database failed")
        elif u'Welcome' in parsed:
            print("Welcome! ", parsed)
        else:
            print("error: ", parsed)

    def action(self):
        while self.socket.connected:
            self.wait()

    def wait(self):
        self.application.send_data()
        time.sleep(.2)
        self.socket.wait(.5)

