import data_store
import connection


__author__ = 'fkint'


class Application:
    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id
        self.sensors = []
        self.thread = None
        self.data_store = data_store.DataStore(self)
        self.connection = connection.Connection(self, "dali.cs.kuleuven.be", 8080)

    def action(self):
        self.connection.wait()

    def start(self):
        self.connection.open_connection()
        self.connection.start_trip()

    def stop(self):
        print("trying to stop!")
        self.connection.stop_trip()
        self.connection.close_connection()

    def live_trip_active(self):
        if self.connection is None:
            print "no connection"
            return
        return self.connection.live_trip_active()

    def send_data(self):
        self.data_store.send_data()