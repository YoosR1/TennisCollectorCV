import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from picamera2 import Picamera2
import RPi.GPIO as GPIO # Double check for installation of package on RasPi

from BallDetect import *
from LineDetect import *

# Command is value from 0 to 11, corresponding to the 6 commands of the
# motor controller, 0-5 being low priority, 6-11 being high priority
# For reference, motor controller commands are
# {fullLeft, slightLeft, straight, slightRight, fullRight, stop}
command = -1

inputGPIO = 18 # physical pin 12
outputGPIO = 17 # physical pin 11

GPIO.setmode(GPIO.BCM)
GPIO.setup(inputGPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(outputGPIO, GPIO.OUT, initial=GPIO.LOW)
# TODO: figure out how to transmit value
def commandRequest():
    # GPIO.output(outputGPIO, GPIO.HIGH)
    return command

GPIO.add_event_detect(inputGPIO, GPIO.RISING, callback=commandRequest, bouncetime=100)

# refimage should be of 2in court line 4ft away
# might use image from 2ft away
refImage = mpimg.imread('testimage/2in2ft.jpg')
focalLength = findFocalLength(refImage, 2, 24)

cam = Picamera2()
# TODO: test if lower resolution helps with capture/processing time
config = cam.create_still_configuration(main={'size': (1152, 648)})
cam.configure(config)

while True:
    cam.start()
    currImage = cam.capture_array()
    cam.stop()

    lineDist, lineDir = distEst(currImage, focalLength)
    # TODO: make distEst also return direction of line
    if lineDist < 36:
        command = 6 + lineDir
    else:
        ballList = BallDetect(currImage, True)
        ballDir = [0] * 5
        for ball in ballList:
            ballDir[ball] += 1
        command = max(ballDir)


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