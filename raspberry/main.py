import logging

from raspberry.service import application, serial_connection
import sensor_reader


logging.basicConfig(level=logging.ERROR)

app = application.Application("cwa3", "r0463107")

started = False


def start():
    global started, app
    started = True
    app.start()

    #start live trip
    app.start_trip(True)


def stop():
    global app, started, sc
    app.stop()
    sc.stop()
    started = False


def click():
    global started
    if started:
        stop()
    else:
        start()

# gps_reader = sensor_reader.GPSSensor()
# accellero_reader = sensor_reader.AccelleroSensor()
sc = serial_connection.SerialConnection("/dev/arduino1", 9600)
sc.start()
dummy_reader = sensor_reader.DummySensor(app)
thermo_sensor = sensor_reader.ThermoSensor(sc, app)
humidity_sensor = sensor_reader.HumiditySensor(sc, app)
button = sensor_reader.PushButton(sc, click)
#click()

#time.sleep(10)
#click()#
# class DataStore:
#     def __init__(self, app):
#         self.application = app
#         self.data = []
#
#     def add_record(self, record):
#         #self.data.append(record)
#         self.current_trip
#
#     def live_trip_active(self):
#         return self.application.live_trip_active()
#
#     def send_data(self):
#         if self.
#         if not self.live_trip_active():
#             return
#         while len(self.data) > 0:
#             tmp = self.data.pop()
#             if self.application.connection.send_data(tmp):

