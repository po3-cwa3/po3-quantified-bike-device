__author__ = 'fkint'

class SensorReader:
    def __init__(self):
        self.active = False
    def start(self):
        self.active = True
    def stop(self):
        self.active = False
    def setDataStore(self, store):
        self.data_store = store
    def send_record(self, record):
        self.data_store.add_record(record)
    def read(self):
        print("read should be overridden")

class GPSSensor(SensorReader):
    def __init__(self):
        pass
class AccelleroSensor(SensorReader):
    def __init__(self):
        pass
class DummySensor(SensorReader):
    def __init__(self):
        pass
    def read(self):
        data = [{
                "sensorID":1,
                "timestamp":time.time(),
                "data":[
                    {"type":"Point",
                        "coordinates":[
                            [100,0]
                            ]
                        }]
                    }]
        self.send_record(data)