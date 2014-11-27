import threading
import time
import serial
import serial_connection

class SendtoArduino:
    def __init__(self, serial):
        self.serial = serial
        self.string = '0000'
        self.status = True
        self.thread = None

    def start(self):
        self.thread = threading.Thread(name="SendtoArduino",target=self.send)
        self.thread.run()

    def stop(self):
        self.status = False

    def send(self):
        while self.status:
            self.serial(self.string)
            time.sleep(1)

    def online(self):
        self.replace(-1,'1')

    def offline(self):
        self.replace(-1,'0')

    def replace(self,place,char):
        lst = list(self.string)
        lst[place]=char
        self.string = ''.join(lst)

sc = serial_connection.SerialConnection("/dev/arduino1", 115200)
sc.start()
sendtoard = SendtoArduino(sc)
sendtoard.start()
