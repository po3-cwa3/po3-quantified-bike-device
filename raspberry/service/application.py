import threading
import time

import data_store
import connection


__author__ = 'fkint'


class Application:
    def __init__(self, group_id, user_id, sendtoarduino):
        self.group_id = group_id
        self.user_id = user_id
        self.sendtoarduino = sendtoarduino
        self.sensors = []
        self.data_store = data_store.DataStore(self)
        self.connection = connection.Connection(self, "dali.cs.kuleuven.be", 8080, self.sendtoarduino)
        self.active = False
        self.thread = None

    # def action(self):
    #     self.connection.wait()

    def has_active_trip(self):
        return self.data_store.current_trip is not None

    def start(self):
        self.active = True
        self.connection.start()
        #self.connection.open_connection()
        self.thread = threading.Thread(name="main thread", target=self.action)
        self.thread.start()

    def start_trip(self, live):
        self.data_store.start_trip(live)
        print("start trip")

    def stop_trip(self):
        self.data_store.stop_trip()
        print("stop trip")

    def trip_started(self, id):
        self.data_store.trip_started(id)

    def stop(self):
        self.connection.stop_trip()
        time.sleep(2);
        self.active = False
        self.connection.close_connection()
        self.data_store.send_data()

    def get_connection(self):
        return self.connection

    def get_data_store(self):
        return self.data_store

    def action(self):
        while self.active:
            self.data_store.send_data()
            time.sleep(.1)

    def get_trip_id(self):
        return self.get_data_store().current_trip.get_id()

    def get_user_id(self):
        return self.user_id
