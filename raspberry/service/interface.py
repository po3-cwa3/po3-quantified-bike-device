__author__ = 'fkint'
import threading
import batch_upload
import sensor_reader
import images


# interface reads data from the serial monitor and from the camera installed on the RPi
#it can start batch-upload
#it sends all data to the data-store

class Interface:
    def __init__(self, serial, app, send_to_arduino):
        self.app = app
        self.app.set_interface(self)
        self.send_to_arduino = send_to_arduino
        self.taking_picture = False
        self.batch_uploading = False
        self.trip_button = sensor_reader.PushButton(serial, self.trip_button_pressed, "PB1")
        self.picture_button = sensor_reader.PushButton(serial, self.picture_button_pressed, "PB2")
        self.batch_button = sensor_reader.PushButton(serial, self.batch_button_pressed, "PB3")
        self.live_mode = True

    def trip_button_pressed(self):
        print("trip button pressed")
        if self.app.has_active_trip():
            self.app.stop_trip()
        else:
            self.app.start_trip(self.live_mode)

    def update_state(self):
        self.send_to_arduino.set_online_status(self.has_internet_connection())

    def has_internet_connection(self):
        return self.app.has_connection()

    def batch_upload(self):
        disabled_trips = set()
        if self.app.get_data_store().current_trip is not None:
            disabled_trips.add(self.app.get_trip_id())
        b = batch_upload.BatchUpload(disabled_trips)
        print "asking for batch upload"
        b.start()
        while not b.ready:
            print "waiting for batch to finish"
            b.socket.wait_for_callbacks(seconds=1)
        print "batch finished"
        self.batch_uploading = False

    def picture_button_pressed(self):
        print("picture button pressed")
        if self.taking_picture:
            print("still taking picture, try again later")
            return
        self.taking_picture = True
        t = threading.Thread(target=self.take_picture)
        t.start()

    def batch_button_pressed(self):
        print "batch button pressed"
        if self.batch_uploading:
            #show error with LEDs
            print "already uploading"
            return
        if not self.has_internet_connection():
            #show error with LEDs
            print "no internet connection"
            return
        self.batch_uploading = True
        t = threading.Thread(target=self.batch_upload)
        t.start()

    def take_picture(self):
        print("in take_picture")
        photo_id = images.take_photo()
        print("photo taken")
        self.app.get_data_store().add_image(photo_id)
        print("record added")
        self.taking_picture = False