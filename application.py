import data_store, connection


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
        if self.live_trip_active():
            for s in self.sensors:
                s.read()
        self.connection.wait()
    def start(self):
        #start realtime sender
        self.connection.open_connection()
        self.connection.start_trip()
        for s in self.sensors:
            s.start()
        #self.thread = threading.Thread(name="application", target=self.work)

    def stop(self):
        #stop realtime sender
        print("trying to stop!")
        self.connection.stop_trip()

    def attachSensorReader(self, sensor):
        self.sensors.append(sensor)
        sensor.setDataStore(self.data_store)
    def live_trip_active(self):
        if self.connection is None:
            print "no connection"
            return
        return self.connection.live_trip_active()
    def send_data(self):
        self.data_store.send_data()