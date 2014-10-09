from socketIO_client import SocketIO
import time
import json

import logging
logging.basicConfig(level=logging.ERROR)


class DataStore:
    def __init__(self, app):
        self.application = app
        def add_record(self, record):
            if self.try_send_data(record):
                return
            self.data.append(data)
        def try_send_data(self, record):
            if not self.live_trip_active():
                return
            self.application.connection.send_data(record)
        def live_trip_active():
            return self.application.live_trip_active()

class Application:
    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id
        self.sensors = []
        self.data_store = DataStore(self)
        self.connection = Connection(self, "dali.cs.kuleuven.be", 8080)
    def action(self):
        if self.live_trip_active():
            for s in self.sensors:
                s.read()
        self.connection.wait()
    def start(self):
        #start realtime sender
        self.connection.start_trip()
        for s in self.sensors:
            s.start()

    def stop(self):
        #stop realtime sender
        self.connection.stop_trip()

    def attachSensorReader(self, sensor):
        self.sensors.append(sensor)
        sensor.setDataStore(self.data_store)
    def live_trip_active(self):
        return self.connection.live_trip_active()
class Connection:
    def __init__(self, application, server, port):
        self.application = application
        self.server = server
        self.port = port
        self.connection_opened = False
        self.trip_started = False
        self.open_connection()
    def send_data(self, data):
        to_send = {'_id':self.trip_id, "sensorData":data}
        self.socket.emit('rt-sensordata', to_send)
    def open_connection(self):
        self.socket = SocketIO(self.server, self.port)
        self.socket.on('server_message', self.on_response)
        self.connection_opened = True
    def start_trip(self):
        data = {'purpose':'realtime-sender', 'groupID':self.application.group_id, 'userID':self.application.user_id}
        self.socket.emit('start', json.dumps(data), self.on_trip_start_response)
    def stop_trip(self):
        data = {'_id':self.trip_id, "meta":None}
        self.socket.emit('endBikeTrip', json.dumps(data), self.on_trip_end_response)
    def live_trip_active(self):
        return self.connection_opened and self.trip_started
    def on_trip_start_response(self, *args):
        print('trip start response: ', args)
        self.trip_started = True
        self.trip_id = json.loads(args)['_id']
        print("trip id = ",str(self.trip_id))
    def on_response(self, *args):
        parsed = args[0]
        if 'message' in parsed:
            if parsed['message'] == "Connection accepted. Ready to receive realtime data.":
                self.trip_started = True
                self.trip_id = parsed['_id']
                print("trip started, id = ", self.trip_id)
            else:
                print("other message", parse['message'])
        elif "bikeTrip saved to Database" in parsed:
            self.trip_started = False
            print("trip saved to database!")
        elif "illegal JSON data received" in parsed:
            print("saving data to database failed")
        elif isinstance(parsed, list) and u'Welcome' in parsed[0]:
            print("Welcome! ", parsed)
        else:
            print("error: ",parsed)

    def on_trip_end_response(self, *args):
        print('trip end response: ', args)
    def wait(self):
        #self.socket.wait(5)
        #self.socket.wait_for_callbacks()
        print("in wait")
        time.sleep(.2)
        self.socket.wait(.5)



class SensorReader:
    def __init__(self):
        self.active = False
    def start(self):
        self.active = True
    def stop(self):
        self.active = False
    def setDataStore(self, store):
        self.data_store = store
    def send_record(self, record):
        self.data_store.add_record(record)
    def read(self):
        print("read should be overridden")


class GPSSensor(SensorReader):
    def __init__(self):
        pass
class AccelleroSensor(SensorReader):
    def __init__(self):
        pass
class DummySensor(SensorReader):
    def __init__(self):
        pass
    def read(self):
        data = [
                "sensorID":1,
                "timestamp":time.time(),
                "data":[
                    {"type":"Point",
                        "coordinates":[
                            [100,0]
                            ]
                        }]
                    ]
        self.send_record(data)

app = Application("cwa3", "r0463107")

gps_reader = GPSReader()
accellero_reader = AccelleroReader()
dummy_reader = DummyReader()

app.attachSensorReader(gps_reader)
app.attachSensorReader(accellero_reader)
app.attachSensorReader(dummy_reader)

app.start()

for i in range(10):
    app.action()



app.stop()
for i in range(10):
    app.action()
