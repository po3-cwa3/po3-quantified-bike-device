__author__ = 'fkint'

class Connection:
    def __init__(self, application, server, port):
        self.application = application
        self.server = server
        self.port = port
        self.connection_opened = False
        self.trip_started = False
        self.open_connection()
    def send_data(self, data):
        to_send = {'_id':self.trip_id, "sensorData":data}
        print("tries to send: ",to_send)
        self.socket.emit('rt-sensordata', json.dumps(to_send))
    def open_connection(self):
        self.socket = SocketIO(self.server, self.port)
        self.socket.on('server_message', self.on_response)
        self.connection_opened = True
    def start_trip(self):
        data = {'purpose':'realtime-sender', 'groupID':self.application.group_id, 'userID':self.application.user_id}
        self.socket.emit('start', json.dumps(data), self.on_trip_start_response)
    def stop_trip(self):
        data = {'_id':self.trip_id, "meta":None}
        self.socket.emit('endBikeTrip', json.dumps(data), self.on_trip_end_response)
    def live_trip_active(self):
        return self.connection_opened and self.trip_started
    def on_trip_start_response(self, *args):
        print('trip start response: ', args)
        self.trip_started = True
        self.trip_id = json.loads(args)['_id']
        print("trip id = ",str(self.trip_id))
    def on_response(self, *args):
        parsed = args[0]
        if 'message' in parsed:
            if parsed['message'] == "Connection accepted. Ready to receive realtime data.":
                self.trip_started = True
                self.trip_id = parsed['_id']
                print("trip started, id = ", self.trip_id)
            else:
                print("other message", parsed['message'])
        elif "bikeTrip saved to Database" in parsed:
            self.trip_started = False
            print("trip saved to database!")
        elif "illegal JSON data received" in parsed:
            print("saving data to database failed")
        elif isinstance(parsed, list) and u'Welcome' in parsed[0]:
            print("Welcome! ", parsed)
        else:
            print("error: ",parsed)

    def on_trip_end_response(self, *args):
        print('trip end response: ', args)
    def wait(self):
        #self.socket.wait(5)
        #self.socket.wait_for_callbacks()
        print("in wait")
        time.sleep(.2)
        self.socket.wait(.5)

