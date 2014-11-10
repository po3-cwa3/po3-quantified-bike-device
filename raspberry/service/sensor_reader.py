import threading
import time
import random
import datetime

import serial_connection


__author__ = 'fkint'


class SensorReader:
    def __init__(self, data_store):
        self.active = False
        self.set_data_store(data_store)

    def start(self):
        self.active = True

    def stop(self):
        self.active = False

    def set_data_store(self, store):
        self.data_store = store

    def send_record(self, record):
        self.data_store.add_record(record)


class GPSSensor(SensorReader):
    def __init__(self):
        pass


class AccelleroSensor(SensorReader):
    def __init__(self):
        pass


class DummySensor(SensorReader):
    def __init__(self, app):
        self.application = app
        self.thread = threading.Thread(name="dummy sensor", target=self.action)
        self.thread.start()

    def action(self):
        for i in range(10):
            self.read()
            time.sleep(1)

    def read(self):
        data = [{
                    "sensorID": 1,
                    "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                    "data": [
                        {"type": "Point",
                         "coordinates": [
                             [random.randint(0, 100), random.randint(0, 100)]
                         ]
                        }]
                }]
        self.application.get_data_store().add_record(data)


class SerialSensor(SensorReader, serial_connection.SerialListener):
    def __init__(self, serial, application):
        serial_connection.SerialListener.__init__(self, serial)
        SensorReader.__init__(self, application.data_store)
        self.application = application


class HumiditySensor(SerialSensor):
    def __init__(self, serial, application):
        #super(serial, application)
        SerialSensor.__init__(self, serial, application)

    def data_received(self, data):
        line = data
        if len(line) < 10:
            return
        if line[:10] == "Error No :":
            print("thermo sensor error: ", line)
            return
        if line[:3] != "th;":
            return

        splitted = line.split(";")
        h = float(splitted[2])

        humidity_data = [{
                             "sensorID": 4,
                             "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime(
                                 '%Y-%m-%d %H:%M:%S'),
                             "data": [{"value": h}]
                         }]
        self.send_record(humidity_data)


class ThermoSensor(SerialSensor):
    def __init__(self, serial, application):
        SerialSensor.__init__(self, serial, application)

    def data_received(self, data):
        line = data
        if len(line) < 10:
            return
        if line[:10] == "Error No :":
            print("thermo sensor error: ", line)
            return
        if line[:3] != "th;":
            return

        splitted = line.split(";")
        t = float(splitted[1])

        temperature_data = [{
                                "sensorID": 3,
                                "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime(
                                    '%Y-%m-%d %H:%M:%S'),
                                "data": [{"value": t}]
                            }]
        self.send_record(temperature_data)


class PushButton(serial_connection.SerialListener):
    def __init__(self, serial, action, identifier):
        serial_connection.SerialListener.__init__(self, serial)
        self.action = action
        self.previous_value = False
        self.identifier = identifier

    def data_received(self, data):
        #print(data)
        line = data
        if len(line) < len(self.identifier)+2:
            return
        if line[:len(self.identifier)+1] != self.identifier+";":
            return
        splitted = line.split(";")
        if splitted[1].strip() == "1":
            if not self.previous_value:
                self.action()
            self.previous_value = True
        else:
            self.previous_value = False
