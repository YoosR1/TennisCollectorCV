import cv2

# Use hough transform on canny image to find court lines and
# estimated distance away from camera 
# Returns estimated distance
def distEst(cannyImg, focalLength):
    # # Control distance from camera to object (in)
    # knownDist = 48

    # # Known width of object in control image (in)
    # knownWidth = 3

    # focalLength = (pxlWidth * knownDist) / knownWidth

    return distance