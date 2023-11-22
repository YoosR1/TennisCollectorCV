import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
from picamera2 import Picamera2

from BallDetect import *
from LineDetect import *

# refimage should be of 2in court line 4ft away
refImage = mpimg.imread('testimage/refimage.jpg')
focalLength = findFocalLength(refImage, 2, 48)

cam = Picamera2()
# TODO: test if lower resolution helps with capture/processing time
config = cam.create_still_configuration(main={'size': (1152, 648)})
cam.configure(config)

cam.start()
currImage = cam.capture_array()
cam.stop()

distance = distEst(currImage, focalLength)
# TODO: make distEst also return direction of line
# if distance < 48:
#     command = 

ballList = BallDetect(currImage, True)# Double check this needs conversion

# TEST CODE
# try:
#     while True:
#         cam.start()
#         image = cam.capture_array()
#         cam.stop()
#         ballList = BallDetect(image, True)
# except KeyboardInterrupt:
#     cam.stop()
# image = mpimg.imread('testimages/tennis-ball-on-court.jpg')