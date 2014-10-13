import threading
import time, random
import datetime
import serial
__author__ = 'fkint'

class SensorReader:
    def __init__(self):
        self.active = False
    def start(self):
        self.active = True
        self.thread = threading.Thread(name="sensor", target=self.action)
        self.thread.start()
    def stop(self):
        self.active = False
    def setDataStore(self, store):
        self.data_store = store
    def send_record(self, record):
        self.data_store.add_record(record)
    def read(self):
        print("read should be overridden")
    def action(self):
        while self.active:
            self.read()
            time.sleep(1)

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
        data = [{
                "sensorID":1,
                "timestamp":datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                "data":[
                    {"type":"Point",
                        "coordinates":[
                            [random.randint(0,100),random.randint(0,100)]
                            ]
                        }]
                    }]
        self.send_record(data)
class ThermoSensor(SensorReader):
    def __init__(self):
        self.ser = serial.Serial('/dev/arduino1', 9600)
    def read(self):
        line = self.ser.readline()
        print("thermo sensor received: ", line)
        if len(line) < 10:
            print("no meaningful data")
        else:
            if line[:10] == "Error No :":
                print("thermo sensor error: ", line)
            elif line[:3] == "th;":
                splitted = line.split(";")
                t = float(splitted[1])
                h = float(splitted[2])

                temperature_data = [{
                    "sensorID":3,
                    "timestamp":datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                    "data":[{"value":t }]
                }]
                humidity_data =[{
                    "sensorID":4,
                    "timestamp":datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                    "data":[{"value":h}]
                }]
                self.send_record(temperature_data)
                self.send_record(humidity_data)
            else:
                print("received nonsense: ", line)