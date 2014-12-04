import threading
import serial

__author__ = 'fkint'


class SerialConnection:
    """
    Class to manage the communication between the Pi and the Arduino.
    """
    def __init__(self, address, baud):
        """
        Initializes the serial connection.
        :param address: the path to the serial device
        :param baud: the baud rate used by the serial device
        """
        self.ser = serial.Serial(address, baud)
        self.active = False
        self.listeners = set()
        self.thread = None

    def attach_listener(self, listener):
        """
        Add a SerialListener.
        :param listener: will be added to the listeners that are notified when new data is received from the Arduino.
        """
        self.listeners.add(listener)

    #@TODO: remote send_data or write
    def send_data(self, data):
        """
        Send data to the Arduino.
        :param data: data that will be sent to the Arduino.
        """
        self.ser.write(self, data)

    def action(self):
        """
        This method is executed in the Serial Thread.
        """
        while self.active:
            # Waits until a new line of data is available from the Arduino
            line = self.ser.readline().strip()
            # Inform all listeners about the data that has been received from the Arduino
            for listener in self.listeners:
                try:
                    listener.data_received(line)
                except Exception as e:
                    print("error in listener - data_received for line = " + line)
                    print e.message
        # Close the serial connection 
        self.ser.close()

    def stop(self):
        """
        Stop the serial connection thread
        """
        self.active = False;

    def write(self, data):
        """
        Send data to the Arduino
        :param data: data that will be sent to the Arduino
        """
        self.ser.write(data)

    def start(self):
        """
        Starts the Serial Thread.
        """
        self.active = True;
        self.thread = threading.Thread(name="serial", target=self.action)
        self.thread.daemon = True
        self.thread.start()


class SerialListener:
    """
    Base class for objects that receive data from the Serial Connection
    """
    def __init__(self, serial_connection):
        """
        Initialize the listener by attaching it to the serial_connection
        :param serial_connection: the connection to which this listener should be attached
        """
        serial_connection.attach_listener(self)

    def data_received(self, data):
        """
        Function that is called by serial_connection when new data is received.
        This function should be overridden for specific SerialListeners.
        """
        print("SerialListener.should be overridden")
