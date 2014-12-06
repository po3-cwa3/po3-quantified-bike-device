__author__ = 'fkint'

import time
import datetime
import MySQLdb
import json
import images
import config
from contextlib import closing

class DataStore:
    """
    Class managing the storage and sending of data.
    """
    def __init__(self, app):
        """
        Initializes the DataStore
        :param app: a reference to the Application object this DataStore belongs to.
        """
        self.application = app;
        self.current_trip = None
        # Initialize the connection to the local Database
        self.database = DatabaseConnection(config.local_host, config.local_database_username, config.local_database_password, config.local_database_name)

    def start_trip(self, live):
        """
        Starts a new trip
        :param live: if True, all data received for that trip will be sent to the remote server immediately. If false, all data be stored in the local database.
        """
        t = Trip(live)
        self.current_trip = t
        if live:
            # Send a request for a new trip to the remote server
            self.get_connection().start_trip()
        else:
            # Add a new trip to the local database
            self.get_database().start_trip(t)

    def stop_trip(self):
        """
        Stops the current trip.
        """
        if self.current_trip is None:
            print("stopping non-existent trip")
            return
        # Send all data that is still available about this trip
        self.send_data()
        if self.current_trip.is_live():
            # If the trip is live, warn the remote server that we want to stop the trip.
            self.get_connection().stop_trip()
        else:
            self.get_database().stop_trip(self.current_trip.get_id())
        self.current_trip = None

    def trip_started(self, id):
        """
        This function is called when the creation of a new trip has been confirmed.
        :param id: the id of the new trip (either an id for the remote server or an id for the local database.
        """
        self.current_trip.set_id(id)

    def send_data(self):
        """
        Tries to send all data that is available in memory to either the local database or the remote server.
        """
        if self.current_trip is None:
            return
        if not self.current_trip.has_id():
            return
        try:
            if self.current_trip.is_live():
                while self.current_trip.has_data():
                    d = self.current_trip.next_data()
                    self.get_connection().send_data(d, self.current_trip.get_id())
            else:
                data_array = []
                amount = 30
                while self.current_trip.has_data() and amount > 0:
                    amount -= 1
                    data_array.append(self.current_trip.next_data())
                self.get_database().send_multiple_data(data_array, self.current_trip.get_id())
            # while self.current_trip.has_data():
            #     #First send all sensor data that is available for the current trip
            #     d = self.current_trip.next_data()
            #     if self.current_trip.is_live():
            #         self.get_connection().send_data(d, self.current_trip.get_id())
            #     else:
            #         self.get_database().send_data(d, self.current_trip.get_id())
            while self.current_trip.has_images():
                #Next send all images that are available for the current trip
                d = self.current_trip.next_image()
                if self.current_trip.is_live():
                    print "image starts uploading"
                    images.send_to_server(d, self.current_trip.get_id(), self.application.get_user_id())
                    print "image finished uploading"
                else:
                    self.get_database().send_image(d, self.current_trip.get_id())
        except Exception as ex:
            print "There was an error in send data", str(ex)

    def get_connection(self):
        """
        Returns a reference to the connection that is used to communicate with the remote server.
        """
        return self.application.get_connection()

    def get_database(self):
        """
        Returns a reference to the object that is used to communicate with the local database.
        """
        return self.database

    def add_record(self, data):
        """
        Temporarily store a record that will be sent to either the remote server or the local database when send_data is called.
        :param data: the record data that should be stored.
        """
        if self.current_trip is None:
            print "no trip to add data"
            return
        self.current_trip.store_data(data)

    def add_image(self, image_name):
        """
        Temporarily store information about an image that will be sent to either the remote server or the local database when send_data is called.
        :param image_name: the id of the image that should be sent.
        """
        if self.current_trip is None:
            print "no trip to add image"
            return
        self.current_trip.store_image(image_name)


class DatabaseConnection:
    """
    Class that manages the connection to the local database.
    """
    def __init__(self, hostname, username, password, database_name):
        """
        Initializes the connection to the local database.
        :param hostname: the hostname of the local database
        :param username: the username that should be used to connect to the local database
        :param password: the password that should be used to connect to the local database
        :param database_name: the name of the database in which all data is stored
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database_name = database_name
        
        self.db = MySQLdb.connect(host=self.hostname, user=self.username, passwd=self.password, db=self.database_name)

    def start_trip(self, trip):
        """
        Adds a new trip to the local database.
        :param trip: a reference to the Trip object. This object will be notified about the id it receives in the database.
        """
        with closing(self.db.cursor()) as cursor:
            t = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
            query = "INSERT INTO Trips (StartTime, EndTime) VALUES('"+t+"', '"+t+"')"
            #cursor = self.db.cursor()
            cursor.execute(query)
            trip.set_id(cursor.lastrowid)
            self.db.commit()

    def stop_trip(self, trip_id):
        """
        Sets the end time of the trip.
        :param trip_id: the id of the trip of which the end time should be set.
        """
        print "stopping trip in data_store"
        with closing(self.db.cursor()) as cursor:
            t = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
            query = "UPDATE Trips SET EndTime='"+t+"' WHERE Id = '"+str(trip_id)+"'"
            cursor.execute(query)
            self.db.commit()


    def send_multiple_data(self, data_array, trip_id):
        """
        Sends multiple records to the database.
        :param data_array: the list of records (Python dicts) that should be stored in the database.
        :param trip_id: the id of the trip to which this data belongs
        """
        print data_array
        l = []
        for d in data_array:
            l.append((trip_id, json.dumps(d[0])))
        print l
        with closing(self.db.cursor()) as cursor:
            query = "INSERT INTO Data (Trip, DataString) VALUES (%s, %s)"
            cursor.executemany(query, l)
            self.db.commit()


    def send_data(self, data, trip_id):
        """
        Sends data to the database.
        :param data: the record data (a Python dict) that should be stored in the database.
        :param trip_id: the id of the trip to which this data belongs.
        """
        with closing(self.db.cursor()) as cursor:
            query = "INSERT INTO Data (Trip, DataString) VALUES (%s, %s)"
            #cursor = self.db.cursor()
            cursor.execute(query, (trip_id, json.dumps(data[0])))
            self.db.commit()

    def send_image(self, image_name, trip_id):
        """
        Stores the image_name in the database.
        :param image_name: the id of the image that should be stored in the database.
        :param trip_id: the id of the trip to which this image belongs.
        """
        with closing(self.db.cursor()) as cursor:
            query = "INSERT INTO Images (Trip, ImageName) VALUES (%s, %s)"
            cursor = self.db.cursor()
            cursor.execute(query, (trip_id, image_name))
            self.db.commit()


class Trip:
    """
    A class representing a trip in memory.
    """
    def __init__(self, live):
        """
        Initializes the trip.
        :param live: stores whether all data should be sent immediately to the remote server or first to the local database.
        """
        self.data = []
        self.images = []
        self.live = live
        self.id = None

    def store_image(self, image_name):
        """
        Save image_name so it can be sent to the appropriate place later.
        :param image_name: the id of the image that belongs to this trip
        """
        self.images.append(image_name)

    def store_data(self, data):
        """
        Save record so it can be sent to the appropriate place later.
        :param data: the Python dict containing the record.
        """
        self.data.append(data)

    def is_live(self):
        """
        Returns whether all data about this trip should be stored in the local database or on the remote server.
        """
        return self.live

    def has_id(self):
        """
        Returns whether this trip received an id from the storage yet.
        """
        return not self.id is None

    def get_id(self):
        """
        Returns the id received from the storage.
        """
        return self.id

    def set_id(self, id):
        """
        Sets the id received from the storage.
        """
        self.id = id
        print("self id = " + str(self.id))

    def has_data(self):
        """
        Returns whether there's data to be sent.
        """
        return len(self.data) > 0

    def has_images(self):
        """
        Returns whether there are images to be sent.
        """
        return len(self.images) > 0

    def next_data(self):
        """
        Returns the next record.
        """
        return self.data.pop()
    def next_image(self):
        """
        Returns the next image.
        """
        return self.images.pop()
