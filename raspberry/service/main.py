__author__ = 'fkint'

import application
import serial_connection
import sensor_reader
import interface
import sendtoarduino

sc = serial_connection.SerialConnection("/dev/arduino1", 115200)
sc.start()
sendtoard = sendtoarduino.SendtoArduino(sc)
app = application.Application("cwa3", "r0463107",sendtoard)
# initialize server connection thread (connects if a Internet connection is available)
#conn = connection.Connection(app, "dali.cs.kuleuven.be", 8080)

#initialize Serial Thread (=Interface)

# #dummy_reader = sensor_reader.DummySensor(app)
thermo_sensor = sensor_reader.ThermoSensor(sc, app)
humidity_sensor = sensor_reader.HumiditySensor(sc, app)
gps_sensor = sensor_reader.GPSSensor(sc, app)
accelero_sensor = sensor_reader.AcceleroSensor(app)
bpm_sensor = sensor_reader.BPMSensor(sc, app)
interface = interface.Interface(sc, app)

app.start()
sendtoard.start()

#
# import time, images, threading, datetime
#
# time.sleep(2);
# app.start_trip(True)
# time.sleep(2)
#
# def tmp_picture():
#     filename = images.send_to_server("img", app.get_trip_id(), app.get_user_id())
#     print("filename = "+filename)
#     record = [{
#         "sensorID": 8,
#         "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime(
#             '%Y-%m-%d %H:%M:%S'),
#         "data": [{"value": filename}]
#         }]
#     app.data_store.add_record(record)
#     print("record added")
#
# t = threading.Thread(target=tmp_picture)
# t.start()
#
# time.sleep(5)
# print("stopping app")
# app.stop()
