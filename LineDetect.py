import cv2
import numpy as np
import math
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

# Use hough transform on canny image to find court lines and
# estimated distance away from camera 
# Returns estimated distance
def distEst(image, focalLength):
    distance = -1

    return distance

def findFocalLength(refImage, lineWidth, lineDist):
    # Ideally, refImage should have very few Hough lines
    lines = findLines(refImage)
    if lines is None or len(lines) < 2:
        return -1
    # TODO: figure out how to group lines by nearly equal theta
    # print(lines.shape)
    
    # lines.sort()# works for now, might need reworking
    # print(lines)

    longestDist = 0
    for line in lines:
        # print('new line')
        for otherLine in lines:
            if (line == otherLine).all():
                # print('continue')
                continue
            # Compare thetas, parallel if close
            if abs(line[0][1] - otherLine[0][1]) < .2:
                currDist = distBtwnLines(line[0][1], line[0][0], otherLine[0][0])
                if currDist > longestDist:
                    longestDist = currDist
                # print(abs(line[0][1] - otherLine[0][1]))
                # parallels.append([line[0].tolist(), otherLine[0].tolist()])
    
    # print(np.array(parallels).shape)
    # print(parallels)

    pxlWidth = longestDist

    focalLength = (pxlWidth * lineDist) / lineWidth
    return focalLength

def findLines(image):
    grayImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blurImage = cv2.GaussianBlur(grayImage, (5, 5), 0)
    edgeImage = cv2.Canny(blurImage, 250, 400)
    # TODO: test rho value (2nd value) with camera images
    lines = cv2.HoughLines(edgeImage, .7, np.pi/180, 150, np.array([]), 0, 0)

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
            cv2.line(image, pt1, pt2, (255,0,0), 3, cv2.LINE_AA)

    # if lines is not None:
    #     for i in range(0, len(lines)):
    #         l = lines[i][0]
    #         cv2.line(image, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
    
    fig, ax = plt.subplots(2,1)
    ax[0].imshow(image)
    ax[1].imshow(edgeImage)
    print(lines)
    plt.show()

    # linelist = []
    # for pair in lines:
    #     linelist.append([pair[0][1], pair[0][0]])
    # print(linelist)
    return lines

def distBtwnLines(theta, r1, r2):
    # y = (-cos(theta)/sin(theta))x + (r/sin(theta))
    # d = |b2 - b1|/sqrt(1 + m^2)
    m = -np.cos(theta)/np.sin(theta)
    b1 = r1/np.sin(theta)
    b2 = r2/np.sin(theta)
    d = abs(b2-b1)/np.sqrt(1+pow(m, 2))
    return d

# TEST CODE
# image = mpimg.imread('/home/yoosr/opencvtest/images/disttest.jpg')
image = mpimg.imread('testimages/tennis-ball-on-court.jpg')
# image = mpimg.imread('testimages/outside.jpg')
print(findFocalLength(image, 0, 0))