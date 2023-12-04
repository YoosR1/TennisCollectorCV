import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Use color and hough transform to find tennis balls,
# prioritizes closer balls (lower in image)
# Returns directions of 5 closest balls as list
# (left, right, or center - empty list if none)

# TODO: adjust color range to outdoor lighting
def BallDetect(image, convert):
    imageWidth = image.shape[1]

    if convert:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    blurred = cv2.GaussianBlur(image, (15, 15), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_RGB2HSV)
    greens = cv2.inRange(hsv, (70, 90, 80), (90, 255, 255))

    balls = cv2.HoughCircles(greens, cv2.HOUGH_GRADIENT, 1, int(imageWidth*.05),
        param1=50, param2=10, minRadius=int(imageWidth*.01), maxRadius=int(imageWidth*.1))

    # TEST CODE FOR CHECKING DETECTION
    # print(balls)
    # print(len(balls[0]))
    # fig, ax = plt.subplots(3,1)
    # ax[0].imshow(image)
    # ax[1].imshow(blurred)
    # ax[1].imshow(hsv)
    # ax[1].imshow(greens)
    # cv2.imwrite('greens.jpg', greens)
    # print('greens saved')
    # if balls is not None:
    #     for i in balls[0,:]:
    #         # edge
    #         cv2.circle(image,(int(i[0]),int(i[1])),int(i[2]),(0,255,0),2)
    #         # center
    #         cv2.circle(image,(int(i[0]),int(i[1])),2,(255,0,0),3)
    # ax[2].imshow(image)
    # plt.show()

    if balls is None:
        return []
    else:
        # Sort based on y position, lower in picture is higher y
        ballsList = balls[0,:]
        ballsSort = ballsList[ballsList[:, 1].argsort()[::-1]]

        # Classify direction based on x position
        directions = []
        for ball in ballsSort[:10]:
            if ball[0] <= imageWidth * .4:
                # directions.append('left')
                directions.append(1)
            elif ball[0] < imageWidth - imageWidth * .4:
                # directions.append('center')
                directions.append(2)
            else:
                # directions.append('right')
                directions.append(3)

    # cv2.imwrite('output.jpg', image)
    # print("image saved")
    return directions

# Test function
#while(True):
#    video = cv2.VideoCapture(0)
#    
#    ret = True
#    while ret:
#        ret, image = video.read()
#        print(BallDetect(image, True))
#
#    if cv2.waitKey(1) & 0xFF == ord('q'): 
#        break

# image = mpimg.imread('testimages/balltest.jpg')
# print(BallDetect(image, True))
