import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
from picamera2 import Picamera2

from BallDetect import *
from LineDetect import *

cam = Picamera2()
# TODO: test if lower resolution helps with capture/processing time
config = cam.create_still_configuration(main={'size': (1152, 648)})
cam.configure(config)
try:
    while True:
        cam.start()
        image = cam.capture_array()
        cam.stop()
        ballList = BallDetect(image, True)
except KeyboardInterrupt:
    cam.stop()
# image = mpimg.imread('testimages/tennis-ball-on-court.jpg')
