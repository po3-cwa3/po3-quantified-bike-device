__author__ = 'fkint'


class Application:
    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id
        self.sensors = []
        self.data_store = DataStore(self)
        self.connection = Connection(self, "dali.cs.kuleuven.be", 8080)
    def action(self):
        if self.live_trip_active():
            for s in self.sensors:
                s.read()
        self.connection.wait()
    def start(self):
        #start realtime sender
        self.connection.start_trip()
        for s in self.sensors:
            s.start()

    def stop(self):
        #stop realtime sender
        self.connection.stop_trip()

    def attachSensorReader(self, sensor):
        self.sensors.append(sensor)
        sensor.setDataStore(self.data_store)
    def live_trip_active(self):
        return self.connection.live_trip_active()