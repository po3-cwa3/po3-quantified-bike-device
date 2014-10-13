import threading
import time, random
__author__ = 'fkint'

class SensorReader:
    def __init__(self):
        self.active = False
    def start(self):
        self.active = True
        self.thread = threading.Thread(name="sensor", target=self.action)
        self.thread.start()
    def stop(self):
        self.active = False
    def setDataStore(self, store):
        self.data_store = store
    def send_record(self, record):
        self.data_store.add_record(record)
    def read(self):
        print("read should be overridden")
    def action(self):
        while self.active:
            self.read()
            time.sleep(1)

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
                            [random.randint(0,100),random.randint(0,100)]
                            ]
                        }]
                    }]
        self.send_record(data)