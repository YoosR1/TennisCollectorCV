import cv2
import numpy as np
import math
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

# Use hough transform on canny image to find court lines and
# estimated distance away from camera 
# Returns estimated distance
def distEst(image, focalLength):
    # # Control distance from camera to object (in)
    # knownDist = 48

    # # Known width of object in control image (in)
    # knownWidth = 3

    # focalLength = (pxlWidth * knownDist) / knownWidth

    return distance

def findFocalLength(refImage, lineWidth, lineDist):
    grayImage = cv2.cvtColor(refImage, cv2.COLOR_RGB2GRAY)
    blurImage = cv2.GaussianBlur(grayImage, (7, 7), 0)
    edgeImage = cv2.Canny(blurImage, 250, 400)
    # TODO: test rho value (2nd value) with camera images
    lines = cv2.HoughLines(edgeImage, .8, np.pi/180, 150, np.array([]), 0, 0)

    # lines = cv2.HoughLinesP(
    #     edgeImage,
    #     lines=np.array([]),
    #     rho=6,
    #     theta=np.pi / 120,
    #     threshold=160,
    #     minLineLength=100,
    #     maxLineGap=25
    # )

    # TEST CODE
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(refImage, pt1, pt2, (255,0,0), 3, cv2.LINE_AA)

    # if lines is not None:
    #     for i in range(0, len(lines)):
    #         l = lines[i][0]
    #         cv2.line(refImage, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
    
    fig, ax = plt.subplots(2,1)
    ax[0].imshow(refImage)
    ax[1].imshow(edgeImage)
    print(lines)
    plt.show()

    # cropImage = 

    # focalLength = (pxlWidth * lineDist) / lineWidth
    # return focalLength

image = mpimg.imread('/home/yoosr/opencvtest/images/disttest.jpg')
# image = mpimg.imread('testimages/tennis-ball-on-court.jpg')
findFocalLength(image, 0, 0)