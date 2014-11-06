__author__ = 'fkint'

import application
import serial_connection
#import connection
import data_store
import sensor_reader
import interface




app = application.Application("cwa3", "r0463107")
#initialize server connection thread (connects if a Internet connection is available)
#conn = connection.Connection(app, "dali.cs.kuleuven.be", 8080)

#initialize local database connection thread (connects to local MySQL database)
db_connection = data_store.DatabaseConnection()

#initialize Serial Thread (=Interface)
sc = serial_connection.SerialConnection("/dev/arduino1", 9600)
sc.start()
dummy_reader = sensor_reader.DummySensor(app)
thermo_sensor = sensor_reader.ThermoSensor(sc, app)
humidity_sensor = sensor_reader.HumiditySensor(sc, app)
#button = sensor_reader.PushButton(sc, click)
interface = interface.Interface(sc, app)

app.start()