__author__ = 'fkint'

import application
import serial_connection
import sensor_reader
import interface




app = application.Application("cwa3", "r0463107")
#initialize server connection thread (connects if a Internet connection is available)
#conn = connection.Connection(app, "dali.cs.kuleuven.be", 8080)

#initialize Serial Thread (=Interface)
sc = serial_connection.SerialConnection("/dev/arduino1", 115200)
sc.start()
# #dummy_reader = sensor_reader.DummySensor(app)
thermo_sensor = sensor_reader.ThermoSensor(sc, app)
humidity_sensor = sensor_reader.HumiditySensor(sc, app)
gps_sensor = sensor_reader.GPSSensor(sc, app)
bpm_sensor = sensor_reader.BPMSensor(sc, app)
interface = interface.Interface(sc, app)

app.start()