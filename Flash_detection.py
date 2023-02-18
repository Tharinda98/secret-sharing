import cv2
import numpy as np
webcam = cv2.VideoCapture(0)
pts = []
while (1):
    _, imageFrame = webcam.read()
    # Take each frame
    hsv = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    lower_flashlight = np.array([0, 0, 255])
    upper_flashlight = np.array([0, 0, 255])
    mask = cv2.inRange(hsv, lower_flashlight, upper_flashlight)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)

    cv2.circle(imageFrame, maxLoc, 50, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow('flash', imageFrame)

    

cv2.destroyAllWindows()