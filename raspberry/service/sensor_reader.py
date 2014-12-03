import threading
import time
import random
import datetime

import XLoBorg
import serial_connection


# Some configuration for the Accelero sensor on the Raspberry Pi itself
xloborg_found = False
try:
    XLoBorg.printFunction = XLoBorg.NoPrint
    XLoBorg.Init()
    xloborg_found = True
except:
    print "XLoBorg not found"

__author__ = 'fkint'


class SensorReader:
    """
    Base class for Sensor classes.
    SensorReader provides an interface to send data to the data_store.
    """
    def __init__(self, data_store):
        """
        Initialize the SensorReader by storing a reference to the data_store.
        """
        self.active = False
        self.set_data_store(data_store)

    #@TODO: the active flag is not used. Will we use it or remote this code?
    def start(self):
        """
        Start the sensor. This means that from now on, as soon as data is received, the data will be processed.
        """
        self.active = True

    def stop(self):
        """
        Stop the sensor. This means that from now on, all received data will be ignored.
        """
        self.active = False

    def set_data_store(self, store):
        """
        Store a reference to the data_store.
        @param store: a reference to the data_store this sensor should send its processed data to.
        """
        self.data_store = store

    def send_record(self, record):
        """
        Send the record to the DataStore.
        @param record: the record (a Python dict) to be sent to the DataStore.
        """
        self.data_store.add_record(record)


# class GPSSensor(SensorReader):
#    def __init__(self):
#        pass


class AcceleroSensor(SensorReader):
    """
    Sensor class for the Accelerometer.
    """
    def __init__(self, app):
        """
        Initializes the Accelerometer sensor.
        """
        SensorReader.__init__(self, app.data_store)
        self.application = app
        if not xloborg_found:
            return
        #Initialize a thread that constantly reads the data from the XyBorg sensor
        self.thread = threading.Thread(name="AccelleroSensor", target=self.action)
        self.thread.start()

    def action(self):
        """
        This function is executed in the AcceleroSensor thread.
        """
        while (True):
            self.read()
            time.sleep(1)

    def read(self):
        """
        Read the data from the XyBorg and send it in a nice format to the data_store.
        """
        #init x,y,z,mx,my,mz
        #Orientation information is also sent.
        x, y, z = XLoBorg.ReadAccelerometer()
        mx, my, mz = XLoBorg.ReadCompassRaw()
        data = [{
                    "sensorID": 5,
                    "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                    "data": [
                        {"acceleration": [{
                                              "x": x,
                                              "y": y,
                                              "z": z
                                          }],
                         "orientation": [{
                                             "mx": mx,
                                             "my": my,
                                             "mz": mz
                                         }]
                        }]
                }]
        self.application.get_data_store().add_record(data)


class DummySensor(SensorReader):
    """
    A Dummy Sensor that generates random GPS coordinates to be sent to data_store.
    This class should only be used for development purposes!
    """
    def __init__(self, app):
        """
        Initialize the DummySensor by initializing the thread
        """
        self.application = app
        # Initialize the thread that constantly generates random GPS coordinates to be sent to the DataStore
        self.thread = threading.Thread(name="dummy sensor", target=self.action)
        self.thread.start()

    def action(self):
        """
        This method is executed in the DummySensor thread.
        It 'reads' data 10 times.
        """
        for i in range(10):
            self.read()
            time.sleep(1)

    def read(self):
        """
        Generates random GPS coordinates and sends them to the DataStore in a nice format.
        """
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
    """
    Base class for SensorReader classes that read data from the SerialConnection.
    """
    def __init__(self, serial, application):
        """
        Initializes the SerialSensor by registering itself as a Serialistener and storing a reference to the application
        @param serial: a reference to the SerialConnection used for communication with the Arduino
        @param application: a reference to the main application
        """
        serial_connection.SerialListener.__init__(self, serial)
        SensorReader.__init__(self, application.data_store)
        #@TODO: is self.application used somewhere?
        self.application = application


class HumiditySensor(SerialSensor):
    """
    Class to collect data from the humidity sensor.
    """
    def __init__(self, serial, application):
        """
        Initializes the HumiditySensor as a SerialSensor.
        @param serial: a reference to the SerialConnection used for communication with the Arduino.
        @param application: a reference to the main application
        """
        SerialSensor.__init__(self, serial, application)

    def data_received(self, data):
        """
        Processes the data that has been received from the Arduino.
        @param data: the string sent by the Arduino
        """
        line = data
        #format: th;TT.tt;HH.hh
        #data for the humidity sensor should be at least 10 characters long
        if len(line) < 10:
            return
        #This format is sent by the TH-sensor when an error occurred.
        #@TODO: refactor this error message so it fits in the TH-format.
        if line[:10] == "Error No :":
            print("thermo sensor error: ", line)
            return
        #Only consider lines sent with a matching identification pattern
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
    """
    Class for the Thermometer sensor.
    """
    def __init__(self, serial, application):
        """
        Initializes the ThermoSensor by registering it as a SerialSensor.
        @param serial: a reference to the SerialConnection used for communication with the Arduino.
        @param application: a reference to the main application
        """
        SerialSensor.__init__(self, serial, application)

    def data_received(self, data):
        """
        Processes the data received from the Arduino.
        @param data: the line received from the Arduino.
        """
        line = data
        # format TH;TT.tt;HH.hh
        # Only consider lines having at least length 10
        if len(line) < 10:
            return
        # Error message from the Temperature and Humidity Sensor
        #@TODO: refactor this error message so it fits in the TH-format
        if line[:10] == "Error No :":
            print("thermo sensor error: ", line)
            return
        # Only consider lines with a matching identification pattern
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
    """
    Class for the GPS sensor.
    """
    def __init__(self, serial, application):
        """
        Initializes the GPSSensor by registering itself as a SerialSensor.
        @param serial: a reference to the SerialConnection used for communication with the Arduino
        @param applicatoi: a reference to the main application
        """
        SerialSensor.__init__(self, serial, application)

    def data_received(self, data):
        """
        Processed the data received from the Arduino.
        @param data: the line received from the Arduino.
        """
        line = data
        # Format: GPS;nofix or GPS;Lat;Long
        # Only consider lines of length at least 9
        if len(line) < 9:
            return
        # Only consider lines with a matching identification pattern
        if line[:4] != "GPS;":
            return

        splitted = line.split(";")
        # If the GPS has no fix, the data is useless
        if splitted[1] == "nofix":
            return
        latitude = float(splitted[1])
        altitude = float(splitted[2])

        gps_data = [{
                        "sensorID": 1,
                        "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime(
                            '%Y-%m-%d %H:%M:%S'),
                        "data": [{"type": "Point",
                                  "unit": "google",
                                  "coordinates": [latitude, altitude]}]
                    }]
        self.send_record(gps_data)


class BPMSensor(SerialSensor):
    """
    Class for the heart beat sensor.
    """
    def __init__(self, serial, application):
        """
        Initialize the BPMSensor by registering it as a SerialSensor.
        @param serial: a reference to the SerialConnection used to communicate with the Arduino
        @aram application: a reference to the main application
        """
        SerialSensor.__init__(self, serial, application)

    def data_received(self, data):
        """
        Processes the data received from the Arduino.
        @param data: the line received from the Arduino.
        """
        line = data
        # Format: BPM;xx
        # Only consider lines of length at least 5
        if len(line) < 5:
            return
        # Only consider lines with a matching identification pattern
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


class HallSensor(SerialSensor):
    """
    Class for the Hall sensor.
    """
    def __init__(self, serial, application):
        """
        Initialize the HallSensor by registering it as a SeralSensor.
        @param serial: a reference to the SerialConnection used for communication with the Arduino.
        @param application: a reference to the main Application
        """
        SerialSensor.__init__(self, serial, application)

    def data_received(self, data):
        """
        Processes the data received from the Arduino.
        @param data: the line received from the Arduino.
        """
        # Format: v;xx.xx
        line = data
        #@TODO: remove all length as they make the code longer and not faster (also at other sensors)
        # Only consider lines of at least length 6
        if len(line) < 6:
            return
        # Only consider lines with a matching identification pattern
        if line[:2] != "v;":
            return

        splitted = line.split(";")
        #@TODO: multiply v by the radius (or diameter, needs check) of the wheel (store as value in config.py)
        v = float(splitted[1])

        hall_data = [{
                             "sensorID": 11,
                             "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime(
                                 '%Y-%m-%d %H:%M:%S'),
                             "data": [{"velocity": v}]
                         }]
        self.send_record(hall_data)


class SwitchButton(serial_connection.SerialListener):
    """
    Class for switch buttons.
    """
    def __init__(self, serial, action_on, action_off, identifier):
        """
        Initialize SwitchButton by registering it as a SerialSensor.
        @param serial: a reference to the SerialConnection used for communication with the Arduino.
        @param action_on: a function that should be called when the button is switched on
        @param action_off: a function that should be called when the button is switched off
        @param identifier: the identifier of this switch button
        """
        serial_connection.SerialListener.__init__(self, serial)
        self.action_on = action_on
        self.action_off = action_off
        self.previous_value = False
        self.identifier = identifier
        self.on_length = 0
        self.off_length = 0
        self.last_on_action = False
        # the amount of consecutive 'on' signals that are needed for the state to be considered reliable
        self.on_threshold = 10
        # the amount of consecutive 'off' signals that are needed for the state to be considered reliable
        self.off_threshold = 10

    def on_received(self):
        """
        Called when a signal is received that the button is switched on.
        """
        self.on_length += 1
        self.off_length = 0
        self.action()
    def off_received(self):
        """
        Called when a signal is received that the button is switched off.
        """
        self.on_length = 0
        self.off_length += 1
        self.action()
    def action(self):
        """
        Determines wether the button state is reliable and takes action if this is the case.
        The button state is reliable if at least self.on_threshold times the same signal has been received.
        """
        if self.on_length > self.on_threshold and not self.last_on_action:
            self.action_on()
            self.last_on_action = True
        if self.off_length > self.off_threshold and self.last_on_action:
            self.action_off()
            self.last_on_action = False

    def data_received(self, data):
        """
        Processes the data received from the Arduino.
        @param data: the line received from the Arduino.
        """
        line = data
        # Only consider lines with length strictly longer than the length of the identifier + 1 
        if len(line) < len(self.identifier) + 2:
            return
        # Only consider lines with a matching identification pattern
        if line[:len(self.identifier)+1] != self.identifier + ";":
            return
        splitted = line.split(";")

        if splitted[1].strip() == "1":
            # Current received state is 'on'
            self.on_received()

        else:
            # Current received state is 'off'
            self.off_received()


class PushButton(serial_connection.SerialListener):
    """
    Class for push buttons.
    """
    def __init__(self, serial, action, identifier):
        """
        Initializes PushButton by registering it as a SerialSensor.
        @param serial: a reference to the SerialConnection used for communication with the Arduino.
        @param action: a function that should be called when the button is pressed.
        @param identifier: the identifier of this button.
        """
        serial_connection.SerialListener.__init__(self, serial)
        self.action = action
        self.previous_value = False
        self.identifier = identifier

    def data_received(self, data):
        """
        Processes data received from the Arduino.
        @param data: the line received from the Arduino.
        """
        #print(data)
        line = data
        # Only consider lines with length longer than the length of the identifer +2
        if len(line) < len(self.identifier) + 2:
            return
        # Only consider lines with a matching identification pattern
        if line[:len(self.identifier) + 1] != self.identifier + ";":
            return
        splitted = line.split(";")
        #@TODO: add threshold?
        if splitted[1].strip() == "1":
            # Only trigger a button-pressed event when the button wasn't pressed previously
            if not self.previous_value:
                print(self.identifier+" pressed")
                self.action()
            self.previous_value = True
        else:
            self.previous_value = False
