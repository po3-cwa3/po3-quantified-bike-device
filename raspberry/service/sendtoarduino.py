import threading
import time
import serial
import serial_connection

class SendtoArduino:
    def __init__(self, serial):
        self.serial = serial
        self.string = '000000000'
        self.pattern = '1111100000'
        self.status = True
        self.thread = None
        self.tosend = None

    def start(self):
        self.thread = threading.Thread(name="SendtoArduino",target=self.send)
        self.thread.run()

    def stop(self):
        self.status = False

    def send(self):
        while self.status:
            tosend = self.pattern + self.string
            self.serial.write(tosend)
            time.sleep(1)

    def online(self):
        self.replace(0,'1')

    def offline(self):
        self.replace(0,'0')

    def replace(self,place,char):
        lst = list(self.string)
        lst[place]=char
        self.string = ''.join(lst)

if __name__ == "__main__":
    sc = serial_connection.SerialConnection("COM6", 115200)
    sc.start()
    sendtoard = SendtoArduino(sc)
    sendtoard.start()
