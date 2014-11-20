import threading
import time
import random
import datetime
import XLoBorg
import serial_connection

XLoBorg.printFunction = XLoBorg.NoPrint
XLoBorg.Init()


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


#class GPSSensor(SensorReader):
#    def __init__(self):
#        pass


class AcceleroSensor(SensorReader):
    def __init__(self,app):
        SensorReader.__init__(self, app.data_store)
        self.application = app
        
        self.thread = threading.Thread(name="AccelleroSensor", target=self.action)
        self.thread.start()

    def action(self):
        while(True):
            self.read()
            time.sleep(1)

    def read(self):
        #init x,y,z,mx,my,mz
        x,y,z=XLoBorg.ReadAccelerometer()
        mx,my,mz=XLoBorg.ReadCompassRaw()
        data=[{
                "sensorID": 5,
                "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                "data": [
                    {"acceleration": [{
                        "x":x,
                        "y":y,
                        "z":z
                        }],
                     "orientation": [{
                         "mx":mx,
                         "my":my,
                         "mz":mz
                         }]
                    }]
            }]
        self.application.get_data_store().add_record(data)


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
        SerialSensor.__init__(self, serial, application)

    def data_received(self, data):
        line = data
        if len(line) < 10:
            return
        if line[:10] == "Error No :":
            print("thermo sensor error: ", line)
            return
        if line[:3] != "TH;":
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
        if line[:3] != "TH;":
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

class GPSSensor(SerialSensor):
    def __init__(self, serial, application):
        SerialSensor.__init__(self, serial, application)

    def data_received(self, data):
        line = data
        if len(line) < 9:
            return
        if line[:4] != "GPS;":
            return

        splitted = line.split(";")
        if splitted[1] == "nofix":
            return
        latitude = float(splitted[1])
        altitude = float(splitted[2])

        gps_data = [{
                             "sensorID": 1,
                             "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime(
                                 '%Y-%m-%d %H:%M:%S'),
                             "data": [{"type": "Point",
                                       "unit":"google",
                                       "coordinates":[latitude, altitude]}]
                         }]
        self.send_record(gps_data)
class BPMSensor(SerialSensor):
    def __init__(self, serial, application):
        SerialSensor.__init__(self, serial, application)

    def data_received(self, data):
        line = data
        if len(line) < 5:
            return
        if line[:4] != "BPM;":
            return

        splitted = line.split(";")

        bpm = float(splitted[1])
        gps_data = [{
                             "sensorID": 9,
                             "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime(
                                 '%Y-%m-%d %H:%M:%S'),
                             "data": [{"value": bpm}]
                         }]
        self.send_record(gps_data)



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
