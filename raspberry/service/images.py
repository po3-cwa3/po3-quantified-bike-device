import string
import random
def id_generator(size=20,chars=string.ascii_uppercase+string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

import time
import picamera
def take_photo():
    photo_id=id_generator()
    destination='/home/pi/workspace/po3-quantified-bike-device/raspberry/service/images/'+photo_id+'.jpg'
    with picamera.PiCamera() as camera:
        camera.capture(destination)
    return photo_id

import base64
import json
import requests
def send_to_server(photo_id,trip_id,user_id):
    location='/home/pi/workspace/po3-quantified-bike-device/raspberry/service/images/'+photo_id+'.jpg'
    f=open(location,"rb").read().encode("base64")
    test=json.dumps({"imageName":photo_id+'.jpg',"tripID":trip_id,"userID":user_id,"raw":f})
    url="http://dali.cs.kuleuven.be:8080/qbike/upload"
    data=test
    headers={'Content-type':'application/json','Accept':'text/plain'}
    r=requests.post(url,data=test,headers=headers)
    return "Done!"
