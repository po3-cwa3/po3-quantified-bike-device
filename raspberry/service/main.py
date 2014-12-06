#!/usr/bin/env python
__author__ = 'fkint'

import application
import serial_connection
import sensor_reader
import interface
import sendtoarduino
import config

# SerialConnection reads data sent by the Arduino 
# and warns the sensor listeners when new data has been received
sc = serial_connection.SerialConnection("/dev/arduino1", 115200)
sc.start()
# SentToArduino enables the application to send data to the Arduino
sendtoard = sendtoarduino.SendtoArduino(sc)
# The application initializes the main thread that manages the connection and data store
app = application.Application(config.group_id, config.user_id)
# initialize server connection thread (connects if a Internet connection is available)
#conn = connection.Connection(app, "dali.cs.kuleuven.be", 8080)

#initialize Serial Thread (=Interface)

# dummy_reader can be used to send sample data when no serial device
# is available
#dummy_reader = sensor_reader.DummySensor(app)

# SerialSensor for the thermometer
thermo_sensor = sensor_reader.ThermoSensor(sc, app)
# SerialSensor for the humidity sensor
humidity_sensor = sensor_reader.HumiditySensor(sc, app)
# SerialSensor for the GPS
gps_sensor = sensor_reader.GPSSensor(sc, app)
# Sensor reading data from the Accelerometer installed on the RPi
accelero_sensor = sensor_reader.AcceleroSensor(app)
# SerialSensor for the Pulse Sensor
bpm_sensor = sensor_reader.BPMSensor(sc, app)

# Enable SendToArduino
#sendtoard.start()
# Class managing user interaction
interface = interface.Interface(sc, app, sendtoard)

# Start the main thread
app.start()

