from socketIO_client import SocketIO
import time
import json

import data_store, application, sensor_reader

import logging
logging.basicConfig(level=logging.ERROR)

app = application.Application("cwa3", "r0463107")

#gps_reader = sensor_reader.GPSSensor()
#accellero_reader = sensor_reader.AccelleroSensor()
dummy_reader = sensor_reader.DummySensor()
thermo_sensor = sensor_reader.ThermoSensor()

#app.attachSensorReader(gps_reader)
#app.attachSensorReader(accellero_reader)
app.attachSensorReader(dummy_reader)
app.attachSensorReader(thermo_sensor)

app.start()
time.sleep(15)
app.stop()