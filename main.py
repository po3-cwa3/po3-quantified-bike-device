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

#app.attachSensorReader(gps_reader)
#app.attachSensorReader(accellero_reader)
app.attachSensorReader(dummy_reader)

app.start()
time.sleep(5)
app.stop()