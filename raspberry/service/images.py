import string
import random
import picamera
#import base64
import os
import json
from httplib import HTTPConnection
import requests

images_path = "/home/pi/workspace/po3-quantified-bike-device/raspberry/service/images/"
#images_path = "/home/pi/images/"
upload_url = "http://dali.cs.kuleuven.be:8080/qbike/upload"
upload_host = "http://dali.cs.kuleuven.be"
upload_port = 8080
upload_path = "/qbike/upload"

def id_generator(size=20, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_filename(photo_id):
    return photo_id + ".jpg"


def take_photo():
    photo_id=id_generator()
    with picamera.PiCamera() as camera:
        camera.capture(images_path + get_filename(photo_id))
    return photo_id


def send_to_server(photo_id, trip_id, user_id):
    try:
        location = images_path + get_filename(photo_id)
        f = open(location, "rb").read().encode("base64")
        test = json.dumps({"imageName": get_filename(photo_id), "tripID": trip_id, "userID": user_id, "raw": f})
        url = upload_url
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        #requests.post(url, data=test, headers=headers)
        conn = HTTPConnection(upload_host, upload_port)
        conn.request("POST", upload_path, test, headers)
        resp = conn.getresponse()
        print "sending image to server gave the following response: ", resp
        data = json.loads(resp.read().decode("utf-8"))
        print "data = ", data
        conn.close()
        os.remove(location)
    except Exception as e:
        print "error while trying to send image to server", e.strerror
    return get_filename(photo_id)


# test_trip_id "5436a08271b56f091b616920","r0463107"

def debug():
    photo_id = "img"
    print(send_to_server("img", "5464d09f4e4238bc7756c319", "r0463107"))


if __name__ == "__main__":
    debug()
