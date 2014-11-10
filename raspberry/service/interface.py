__author__ = 'fkint'
import sensor_reader
import images
import datetime
import time

#interface reads data from the serial monitor and from the camera installed on the RPi
#it can start batch-upload
#it sends all data to the data-store

class Interface:
    def __init__(self, serial, app):
        self.app = app
        self.trip_button = sensor_reader.PushButton(serial, self.trip_button_pressed, "PB1")
        self.picture_button = sensor_reader.PushButton(serial, self.picture_button_pressed, "PB2")
        self.live_mode = False

    def trip_button_pressed(self):
        print("trip button pressed")
        if self.app.has_active_trip():
            self.app.stop_trip()
        else:
            self.app.start_trip(self.live_mode)

    def picture_button_pressed(self):
        print("picture button pressed")
        photo_id = images.take_photo()
        filename = images.send_to_server(photo_id, self.app.get_trip_id(), self.app.get_user_id())
        record = [{
                                "sensorID": 8,
                                "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime(
                                    '%Y-%m-%d %H:%M:%S'),
                                "data": [{"value": filename}]
                            }]
        self.data_store.add_record(record)
