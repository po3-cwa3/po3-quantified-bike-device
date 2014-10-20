import threading
import serial

__author__ = 'fkint'


class SerialConnection:
    def __init__(self, address, baud):
        self.ser = serial.Serial(address, baud)
        self.active = False
        self.listeners = set()
        self.thread = None

    def attach_listener(self, listener):
        self.listeners.add(listener)

    def send_data(self, data):
        self.ser.write(self, data)

    def action(self):
        while self.active:
            line = self.ser.readline()
            for listener in self.listeners:
                listener.data_received(line)
        self.ser.close()

    def stop(self):
        self.active = False;

    def start(self):
        self.active = True;
        self.thread = threading.Thread(name="serial", target=self.action)
        self.thread.start()


class SerialListener:
    def __init__(self, serial_connection):
        serial_connection.attach_listener(self)

    def data_received(self, data):
        print("SerialListener.should be overridden")