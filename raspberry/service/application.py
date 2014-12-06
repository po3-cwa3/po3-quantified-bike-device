import threading
import time

import data_store
import connection


__author__ = 'fkint'


class Application:
    """
    The application class manages the main thread, the DataStore and the Connection to the remote server.
    It also provides a few basic functions returning information about the application state
    """
    def __init__(self, group_id, user_id):
        """
        Initializes the Application
        :param group_id: this id is used when sending trips to the remote database
        :param user_id: this id is used when sending trips to the remote database
        """
        self.group_id = group_id
        self.user_id = user_id
        self.sensors = []
        # self.data_store manages all data that's waiting to be sent to either the local or the remote database
        self.data_store = data_store.DataStore(self)
        # self.connection manages the connection to the remote server
        self.connection = connection.Connection(self, "dali.cs.kuleuven.be", 8080)
        self.active = False
        self.ui = None
        self.thread = None

    def has_active_trip(self):
        """
        returns whether a trip is going on
        """
        return self.data_store.current_trip is not None

    def start(self):
        """
        starts the main thread
        """
        self.active = True
        self.connection.start()
        self.thread = threading.Thread(name="main thread", target=self.action)
        self.thread.start()

    def start_trip(self, live):
        """
        starts a trip
        """
        self.data_store.start_trip(live)
        print("start trip")

    def stop_trip(self):
        """
        stops the current trip
        """
        self.data_store.stop_trip()
        print("stop trip")

    def trip_started(self, id):
        """
        This method is called when the application receives confirmation from the remote server that a new trip has been started.
        It notifies the data_store about this.
        """
        self.data_store.trip_started(id)

    def stop(self):
        """
        Stops the main thread and the connections.
        """
        self.connection.stop_trip()
        time.sleep(2)
        self.active = False
        self.connection.close_connection()
        self.data_store.send_data()

    def get_connection(self):
        """
        Returns the connection object to the remote server.
        """
        return self.connection

    def get_data_store(self):
        """
        Returns the DataStore
        """
        return self.data_store

    def action(self):
        """
        This method is executed in the main thread.
        It triggers the DataStore to send its data to either the local or the remote server.
        """
        while self.active:
            self.data_store.send_data()
            self.ui.update_state()
            time.sleep(.1)

    def get_trip_id(self):
        """
        Returns the id of the current trip.
        """
        return self.get_data_store().current_trip.get_id()

    def get_user_id(self):
        """
        Returns the user_id the application has been initialized with.
        """
        return self.user_id

    def set_interface(self, ui):
        """
        Sets the reference to the interface.
        :param ui: a reference to the interface instance.
        """
        self.ui = ui

    def has_connection(self):
        return self.connection.has_connection()
