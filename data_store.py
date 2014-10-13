__author__ = 'fkint'

class DataStore:
    def __init__(self, app):
		self.application = app
		self.data = []
    def add_record(self, record):
        if self.try_send_data(record):
			return
        self.data.append(record)
    def try_send_data(self, record):
        if not self.live_trip_active():
			return
        self.application.connection.send_data(record)
    def live_trip_active(self):
        return self.application.live_trip_active()
