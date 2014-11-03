__author__ = 'fkint'

import application
import serial_connection
import connection




app = application.Application("cwa3", "r0463107")
#initialize server connection thread (connects if a Internet connection is available)
conn = connection.Connection(app, "dali.cs.kuleuven.be", 8080)

#initialize local database connection thread (connects to local MySQL database)

#initialize Serial Thread (=Interface)
sc = serial_connection.SerialConnection("/dev/arduino1", 9600)
sc.start()