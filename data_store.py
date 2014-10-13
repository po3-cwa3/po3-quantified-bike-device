__author__ = 'fkint'


class DataStore:
    def __init__(self, app):
        self.application = app
        self.data = []

    def add_record(self, record):
        self.data.append(record)

    def live_trip_active(self):
        return self.application.live_trip_active()

    def send_data(self):
        if not self.live_trip_active():
            return
        while len(self.data) > 0:
            self.application.connection.send_data(self.data.pop())

