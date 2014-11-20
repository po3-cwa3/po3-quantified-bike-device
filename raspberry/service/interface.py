__author__ = 'fkint'
import sensor_reader
import images
import datetime
import time
import threading

#interface reads data from the serial monitor and from the camera installed on the RPi
#it can start batch-upload
#it sends all data to the data-store

class Interface:
	def __init__(self, serial, app):
		self.app = app
		self.trip_button = sensor_reader.PushButton(serial, self.trip_button_pressed, "PB1")
		self.picture_button = sensor_reader.PushButton(serial, self.picture_button_pressed, "PB2")
		self.live_mode = True

	def trip_button_pressed(self):
		print("trip button pressed")
		if self.app.has_active_trip():
			self.app.stop_trip()
		else:
			self.app.start_trip(self.live_mode)

	def picture_button_pressed(self):
		print("picture button pressed")
		t = threading.Thread(target=self.take_picture)
		t.start()

	def take_picture(self):
		print("in take_picture")
		photo_id = images.take_photo()
		print("photo taken")
		filename = images.send_to_server(photo_id, self.app.get_trip_id(), self.app.get_user_id())
		print("filename = "+filename)
		# record = [{
		# 	"sensorID": 8,
		# 	"timestamp": datetime.datetime.fromtimestamp(time.time()).strftime(
		# 		'%Y-%m-%d %H:%M:%S'),
		# 	"data": [{"value": filename}]
		# 	}]
		#self.app.data_store.add_record(record)
		print("record added")


