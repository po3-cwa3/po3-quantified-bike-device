import threading
import time
import serial_connection


class SendtoArduino:
    """
    Class to ease sending the state of the appliction to the Arduino.
    """
    def __init__(self, serial):
        """
        Initializes the object.
        @param serial: the SerialConnection object used to communicate with the serial device.
        """
        self.serial = serial
        # The initial state (of length 9)
        self.string = '000000000'
        # The pattern preceding the state string (of length 9+1 = 10)
        # This pattern is used so there is no ambiguity for the Arduino about which part of the data contains the state string.
        self.pattern = '1111100000'
        self.status = True
        self.thread = None
        self.tosend = None

    def start(self):
        """
        Initializes the thread continuously sending the state information to the Arduino.
        """
        self.thread = threading.Thread(name="SendtoArduino",target=self.send)
        self.thread.start()
        
    def stop(self):
        """
        Stop the thread continuously sending the state information to the Arduino.
        """
        self.status = False

    def send(self):
        """
        This function is executed in the SendToArduino thread.
        """
        while self.status:
            #Always send the pattern concatenated with the state string to the Arduino
            tosend = self.pattern + self.string
            self.serial.write(tosend)
            time.sleep(1)

    def online(self):
        """
        Sets the online bit in the state string to 1.
        """
        self.replace(0,'1')

    def offline(self):
        """
        Sets the online bit in the state string to 0
        """
        self.replace(0,'0')

    def replace(self,place,char):
        """
        Sets the bit at place in the state string to char.
        """
        lst = list(self.string)
        lst[place]=char
        self.string = ''.join(lst)

# Debugging code
if __name__ == "__main__":
    sc = serial_connection.SerialConnection("COM5", 115200)
    sc.start()
    sendtoard = SendtoArduino(sc)
    sendtoard.start()
    time.sleep(5)
    sendtoard.online()
