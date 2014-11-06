
##import time
##import picamera
##with picamera.PiCamera() as camera:
##    camera.start_preview()
##    time.sleep(5)
##    camera.capture('/home/pi/Desktop/image.jpg')
##    camera.stop_preview()


characters="abcd..."
stri=""
for i in range(10):
    stri+=characters[random.randint()%len(characters)]
