import threading
import data_store
import connection


__author__ = 'fkint'


class Application:
    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id
        self.sensors = []
        self.data_store = data_store.DataStore(self)
        self.connection = connection.Connection(self, "dali.cs.kuleuven.be", 8080)
        self.active = False
        self.thread = None

    def action(self):
        self.connection.wait()

    def start(self):
        self.active = True
        self.connection.open_connection()
        self.thread = threading.Thread(name="main thread", target=self.action)
        self.thread.start()

    def start_trip(self, live):
        self.data_store.start_trip(live)

    def trip_started(self, id):
        self.data_store.trip_started(id)

    def stop(self):
        self.active = False
        self.connection.stop_trip()
        self.connection.close_connection()
        self.data_store.send_data()

    def get_connection(self):
        return self.connection

    def get_data_store(self):
        return self.data_store

    def action(self):
        while self.active:
            self.data_store.send_data()
            self.connection.action()
