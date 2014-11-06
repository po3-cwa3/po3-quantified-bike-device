__author__ = 'fkint'
import sensor_reader

#interface reads data from the serial monitor and from the camera installed on the RPi
#it can start batch-upload
#it sends all data to the data-store

class Interface:
    def __init__(self, serial, app):
        self.app = app
        self.trip_button = sensor_reader.PushButton(serial, self.trip_button_pressed, "pb")
        self.picture_button = sensor_reader.PushButton(serial, self.picture_button_pressed, "pb2")
        self.live_mode = False

    def trip_button_pressed(self):
        if self.app.has_active_trip():
            self.app.stop_trip()
        else:
            self.app.start_trip(self.live_mode)

    def picture_button_pressed(self):
        #TODO: take picture!
        pass