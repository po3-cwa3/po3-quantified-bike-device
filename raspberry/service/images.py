import string
import random

#import time
#import picamera
#import base64
import json
import requests

images_path = "/home/pi/workspace/po3-quantified-bike-device/raspberry/service/images/"
upload_url = "http://dali.cs.kuleuven.be:8080/qbike/upload"


def id_generator(size=20,chars=string.ascii_uppercase+string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_filename(photo_id):
    return photo_id+".jpg"


def take_photo():
    photo_id=id_generator()
    with picamera.PiCamera() as camera:
        camera.capture(images_path+get_filename(photo_id))
    return photo_id


def send_to_server(photo_id,trip_id,user_id):
    location=images_path+get_filename(photo_id)
    f=open(location,"rb").read().encode("base64")
    test=json.dumps({"imageName":get_filename(photo_id),"tripID":trip_id,"userID":user_id,"raw":f})
    url=upload_url
    headers={'Content-type':'application/json','Accept':'text/plain'}
    requests.post(url,data=test,headers=headers)
    return get_filename(photo_id)

# test_trip_id "5436a08271b56f091b616920","r0463107"
