import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import math
from picamera2 import Picamera2

from BallDetect import *
from LineDetect import *

cam = Picamera2()
config = cam.create_still_configuration()
cam.configure(config)
try:
    while True:
        cam.start()
        image = cam.capture_array()
        cam.stop()
        print(BallDetect(image, 1))
except KeyboardInterrupt:
    cam.stop()
# image = mpimg.imread('testimages/tennis-ball-on-court.jpg')
