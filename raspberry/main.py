import logging

import time
import serial_connection
import application
import sensor_reader


logging.basicConfig(level=logging.ERROR)

app = application.Application("cwa3", "r0463107")

started = False


def start():
    global started, app
    started = True
    app.start()

    #start live trip
    app.start_trip(False)


def stop():
    global app, started
    app.stop()
    started = False


def click():
    global started
    if started:
        stop()
    else:
        start()

# gps_reader = sensor_reader.GPSSensor()
# accellero_reader = sensor_reader.AccelleroSensor()
#sc = serial_connection.SerialConnection("/dev/arduino1", 9600)
#sc.start()
dummy_reader = sensor_reader.DummySensor(app)
#thermo_sensor = sensor_reader.ThermoSensor(sc, app)
#humidity_sensor = sensor_reader.HumiditySensor(sc, app)
#button = sensor_reader.PushButton(sc, click)
click()

time.sleep(10)
click()