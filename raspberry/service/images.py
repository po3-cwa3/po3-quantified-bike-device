import string
import random
import picamera
import os
import json
import config
from httplib import HTTPConnection

# The path of the directory containing the images that are temporarily stored on the RPi
images_path = "/home/pi/workspace/po3-quantified-bike-device/raspberry/service/images/"
#images_path = "/home/pi/images/"
# The url of the remote server to which the images should be sent
#upload_url = "http://dali.cs.kuleuven.be:8080/qbike/upload"
# The host of the remote server to which the images should be sent
#upload_host = "dali.cs.kuleuven.be"
upload_host = config.remote_hostname
# The port of the remote server to which the images should be sent
#upload_port = 8080
upload_port = config.remote_port
# The path on the remote server to which the images should be sent
upload_path = "/qbike/upload"

def id_generator(size=20, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    """
    Generates a new id for images (used to determine a filename)
    :param size: the length of the id
    :param chars: the collection of chars that can be used in the id
    """
    return ''.join(random.choice(chars) for _ in range(size))

def get_filename(photo_id):
    """
    Returns the filename based on the image id.
    """
    return photo_id + ".jpg"


def take_photo():
    """
    Takes a photo with the RPi Camera and stores in the folder specified on top of this file.
    Returns the id of the newly created picture.
    """
    photo_id=id_generator()
    with picamera.PiCamera() as camera:
        camera.capture(images_path + get_filename(photo_id))
    return photo_id


def send_to_server(photo_id, trip_id, user_id, timestamp=None):
    """
    Sends a picture to the remote server.
    :param photo_id: the id of the picture to be sent.
    :param trip_id: the id (received from the remote server) of the trip to which the picture belongs.
    :param user_id: the id of the user to which the picture (and the trip) belong.
    :param timestamp: the timestamp at which the picture was taken
    """
    try:
        location = images_path + get_filename(photo_id)
        f = open(location, "rb").read().encode("base64")
        # Prepare the Python dict to be sent to the server over HTTP POST
        data = {"imageName": get_filename(photo_id), "tripID": trip_id, "userID": user_id, "raw": f}
        if timestamp is not None:
            data['timestamp'] = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        test = json.dumps(data)
        # Prepare the headers used in the HTTP Request
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        conn = HTTPConnection(upload_host, upload_port)
        conn.request("POST", upload_path, test, headers)
        resp = conn.getresponse()
        print "sending image to server gave the following response: ", resp
        data = json.loads(resp.read().decode("utf-8"))
        print "data = ", data
        conn.close()
        # Delete the original image from the device (to make some free space on the RPi)
        os.remove(location)
    except Exception as e:
        print "error while trying to send image to server", e
    return get_filename(photo_id)


# test_trip_id "5436a08271b56f091b616920","r0463107"


# Debugging code
def debug():
    photo_id = "img"
    print(send_to_server("img", "5464d09f4e4238bc7756c319", "r0463107"))


if __name__ == "__main__":
    debug()
