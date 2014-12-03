import threading
import time
import serial_connection


# State string:
# 0: 1 if a connection is available
# 1: 1 if batch-uploading
# 2: 1 if batch-uploading succeeded
# 3: 1 if batch-uploading failed
# 4: 1 if taking picture
# 5: 1 if taking picture failed
# 6: 1 if taking picture succeeded
# 7: 1 if trip active
# 8:

class SendtoArduino:
    ONLINE = 0
    BATCH_UPLOADING = 1
    BATCH_UPLOADING_SUCCESS = 2
    BATCH_UPLOADING_FAILED = 3
    TAKING_PICTURE = 4
    TAKING_PICTURE_FAILED = 5
    TAKING_PICTURE_SUCCESS = 6
    TRIP_ACTIVE = 7
    """
    Class to ease sending the state of the appliction to the Arduino.
    """
    def __init__(self, serial):
        """
        Initializes the object.
        :param serial: the SerialConnection object used to communicate with the serial device.
        """
        self.serial = serial
        # The initial state (of length 9)
        self.current_status = [False]*9
        # The pattern preceding the state string (of length 10)
        # This pattern is used so there is no ambiguity for the Arduino about which part of the data contains the state string.
        self.pattern = '1111100000'
        self.status = False
        self.thread = None
        self.tosend = None

    def get_string(self):
        return ''.join(['1' if x else '0' for x in self.current_status])

    # def start(self):
    #     """
    #     Initializes the thread continuously sending the state information to the Arduino.
    #     """
    #     self.status = True
    #     self.thread = threading.Thread(name="SendtoArduino",target=self.send)
    #     self.thread.start()
        
    def stop(self):
        """
        Stop the thread that continuously sends the state information to the Arduino.
        """
        self.status = False
    def send_status(self):
        tosend = self.pattern + self.get_string()
        self.serial.write(tosend)

    # def send(self):
    #     """
    #     This function is executed in the SendToArduino thread.
    #     """
    #     while self.status:
    #         #Always send the pattern concatenated with the state string to the Arduino
    #         tosend = self.pattern + self.get_string()
    #         self.serial.write(tosend)
    #         time.sleep(1)

    def set_online_status(self, value):
        """
        Sets the online status in the state string.
        :param value: True or False, depending on whether a connection is available
        """
        self.set_status(SendtoArduino.ONLINE, value)

    def set_batch_uploading_status(self, value):
        """
        Sets the batch uploading status in the state string.
        :param value: True or False, depending on whether batch uploading or not
        """
        self.set_status(SendtoArduino.BATCH_UPLOADING, value)

    def set_batch_uploading_success_status(self, value):
        """
        Sets the batch uploading success status in the state string.
        :param value: True or False, depending on whether batch uploading succeeded or not
        """
        self.set_status(SendtoArduino.BATCH_UPLOADING_SUCCESS, value)

    def set_batch_uploading_failed_status(self, value):
        """
        Sets the batch uploading failure status in the state string.
        :param value: True or False, depending on whether batch uploading failed or not
        """
        self.set_status(SendtoArduino.BATCH_UPLOADING_FAILED, value)

    def set_taking_picture_status(self, value):
        """
        Sets the taking picture status in the state string.
        :param value: True or False, depending on whether taking a picture or not
        """
        self.set_status(SendtoArduino.TAKING_PICTURE, value)

    def set_taking_picture_success_status(self, value):
        """
        Sets the taking picture success status in the state string.
        :param value: True or False, depending on whether taking a picture succeeded or not
        """
        self.set_status(SendtoArduino.TAKING_PICTURE_SUCCESS, value)

    def set_taking_picture_failed_status(self, value):
        """
        Sets the taking picture failure status in the state string.
        :param value: True or False, depending on whether taking a picture failed or not
        """
        self.set_status(SendtoArduino.TAKING_PICTURE_FAILED, value)

    def set_trip_active_status(self, value):
        """
        Sets the active trip status in the state string.
        :param value: True or False, depending on whether a trip is going on or not
        """
        self.set_status(SendtoArduino.TRIP_ACTIVE, value)

    def set_status(self, index, value):
        """
        Sets the status bit at index in the state string.
        :param index: the index of the bit that has to be set
        :param value: the value of the bit that has to be set (True or False)
        """
        self.current_status[index] = value


# Debugging code
if __name__ == "__main__":
    sc = serial_connection.SerialConnection("COM5", 115200)
    sc.start()
    sendtoard = SendtoArduino(sc)
    sendtoard.start()
    time.sleep(5)
    sendtoard.online()
