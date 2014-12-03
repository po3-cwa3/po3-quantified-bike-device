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

    def update_state(self, picture_failed=False, picture_succeeded=False, batch_failed=False, batch_succeeded=False):
        self.send_to_arduino.set_online_status(self.has_internet_connection())
        self.send_to_arduino.set_batch_uploading_status(self.batch_uploading)
        self.send_to_arduino.set_batch_uploading_success_status(batch_succeeded)
        self.send_to_arduino.set_batch_uploading_failed_status(batch_failed)
        self.send_to_arduino.set_taking_picture_status(self.taking_picture)
        self.send_to_arduino.set_taking_picture_success_status(picture_succeeded)
        self.send_to_arduino.set_taking_picture_failed_status(picture_failed)
        self.send_to_arduino.set_trip_active_status(self.app.has_active_trip())
        self.send_to_arduino.send_status()

    def has_internet_connection(self):
        return self.app.has_connection()

    def batch_upload(self):
        self.update_state()
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
        if b.success:
            self.update_state(batch_succeeded=True)
        else:
            self.update_state(batch_succeeded=False)

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
        try:
            self.update_state()
            print("in take_picture")
            photo_id = images.take_photo()
            print("photo taken")
            self.app.get_data_store().add_image(photo_id)
            print("record added")
            self.taking_picture = False
            self.update_state(picture_failed=True)
        except:
            self.update_state(picture_failed=False)