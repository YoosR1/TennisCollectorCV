import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import serial
from time import sleep

from BallDetect import *
from LineDetect import *

# Command is value from 0 to 11, corresponding to the 6 commands of the
# motor controller, 0-5 being low priority, 6-11 being high priority
# For reference, motor controller commands are
# {fullLeft, slightLeft, straight, slightRight, fullRight, stop}
command = -1

inputGPIO = 18 # physical pin 12
# outputGPIO = 17 # physical pin 11

ser = serial.Serial("/dev/ttyAMA0", 9600)

GPIO.setmode(GPIO.BCM)
GPIO.setup(inputGPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(outputGPIO, GPIO.OUT, initial=GPIO.LOW)
def commandRequest(arg):
    ser.write((str(command)).encode('utf-8'))

GPIO.add_event_detect(inputGPIO, GPIO.RISING, callback=commandRequest, bouncetime=100)

# refimage should be of 2in court line 4ft away
# might use image from 2ft away
# refImage = mpimg.imread('testimages/2in2ft.jpg')
# focalLength = findFocalLength(refImage, 2, 24)
# if focalLength < 1:
#     print('something wrong with the input image')

cam = Picamera2()
config = cam.create_still_configuration(main={'size': (1152, 648)})
cam.configure(config)

mask = [
    (0, 366), # just under left arm
    (576, 324), # center of frame
    (1152, 342), # just under right arm
    (1152, 648), # bottom right
    (0, 648) # bottom left
]

while True:
    cam.start()
    currImage = cam.capture_array()
    cam.stop()

    # lineDist, lineDir = distEst(currImage, focalLength, mask)
    # # TODO: make distEst also return direction of line
    # if lineDist < 36:
    #     command = 6 + lineDir
    # else:
    ballList = BallDetect(currImage, True)
    ballDir = [0] * 5
    for ball in ballList:
        ballDir[ball] += 1
    command = ballDir.index(max(ballDir))
    # TEST CODE
    print(ballDir)
    print(command)

    sleep(1)

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
