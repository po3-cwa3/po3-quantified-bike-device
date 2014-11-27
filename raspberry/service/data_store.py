__author__ = 'fkint'

import MySQLdb
import json
import images


class DataStore:
    def __init__(self, app):
        self.application = app;
        self.current_trip = None
        self.database = DatabaseConnection('localhost', 'QB_CWA3', 'CEeT9cPFSnPExMzQ', 'QuantifiedBike')

    def start_trip(self, live):
        t = Trip(live)
        self.current_trip = t
        if live:
            self.get_connection().start_trip()
        else:
            self.get_database().start_trip(t)

    def stop_trip(self):
        if self.current_trip is None:
            print("stopping non-existent trip")
            return
        self.send_data()
        if self.current_trip.is_live():
            self.get_connection().stop_trip()
        self.current_trip = None

    def trip_started(self, id):
        self.current_trip.set_id(id)

    def send_data(self):
        if self.current_trip is None:
            return
        if not self.current_trip.has_id():
            return
        while self.current_trip.has_data():
            d = self.current_trip.next_data()
            if self.current_trip.is_live():
                self.get_connection().send_data(d, self.current_trip.get_id())
            else:
                self.get_database().send_data(d, self.current_trip.get_id())
        while self.current_trip.has_images():
            d = self.current_trip.next_image()
            if self.current_trip.is_live():
                print "image starts uploading"
                images.send_to_server(d, self.current_trip.get_id(), self.application.get_user_id())
                print "image finished uploading"
            else:
                self.get_database().send_image(d, self.current_trip.get_id())

    def get_connection(self):
        return self.application.get_connection()

    def get_database(self):
        return self.database

    def add_record(self, data):
        if self.current_trip is None:
            print "no trip to add data"
            return
        self.current_trip.store_data(data)

    def add_image(self, image_name):
        if self.current_trip is None:
            print "no trip to add image"
            return
        self.current_trip.store_image(image_name)


class DatabaseConnection:
    def __init__(self, hostname, username, password, database_name):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database_name = database_name
        self.db = MySQLdb.connect(host=self.hostname, user=self.username, passwd=self.password, db=self.database_name)

    def start_trip(self, trip):
        query = "INSERT INTO Trips VALUES()"
        cursor = self.db.cursor()
        cursor.execute(query)
        trip.set_id(cursor.lastrowid)
        self.db.commit()

    def send_data(self, data, trip_id):
        query = "INSERT INTO Data (Trip, DataString) VALUES (%s, %s)"
        cursor = self.db.cursor()
        cursor.execute(query, (trip_id, json.dumps(data)))
        self.db.commit()

    def send_image(self, image_name, trip_id):
        query = "INSERT INTO Images (Trip, ImageName) VALUES (%s, %s)"
        cursor = self.db.cursor()
        cursor.execute(query, (trip_id, image_name))
        self.db.commit()


class Trip:
    def __init__(self, live):
        self.data = []
        self.images = []
        self.live = live
        self.id = None

    def store_image(self, image_name):
        self.images.append(image_name)

    def store_data(self, data):
        self.data.append(data)

    def is_live(self):
        return self.live

    def has_id(self):
        return not self.id is None

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id
        print("self id = " + str(self.id))

    def has_data(self):
        return len(self.data) > 0

    def has_images(self):
        return len(self.images) > 0

    def next_data(self):
        return self.data.pop()
    def next_image(self):
        return self.images.pop()