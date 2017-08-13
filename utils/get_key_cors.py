# Mostly adapted from:
# http://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/

# import the necessary packages
import argparse
import cv2
from tkinter import *
from popup import App

# Clear screen
print('\033[0;0f\033[0J')
# Color Palette
CP_R = '\033[31m'
CP_G = '\033[32m'
CP_B = '\033[34m'
CP_Y = '\033[33m'
CP_C = '\033[0m'

print('{}Press {}c {} to exit!!!{}'.format(CP_R, CP_G, CP_R, CP_C)
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
_ = parser.add_argument
_("-i", "--input", type=str, default='video.mp4', help="Path to video")
_("-s", "--save",  type=str, default='./', help="Path to save information")
args = vars(ap.parse_args())

# File saving bounding box information with label
logger = open(args['save']+'key_info.log', 'w')
logger.write('Keywords | TL-x | TL-y | BR-x | BR-y\n')
logger.write('{:-<36}'.format(''))
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False

def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False

        app = App()
        logger.write('\n{:9}|{:5} |{:5} |{:5} |{:5}'.
                format(str(app.text_value), refPt[0][0], refPt[0][1], refPt[1][0], refPt[1][1]))
        logger.flush()
        print(refPt)
        print(app.text_value)
        # draw a rectangle around the region of interest
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("Image", image)


# load the image, clone it, and setup the mouse callback function
cap = cv2.VideoCapture(args["input"])
ret, image = cap.read()
clone = image.copy()
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", click_and_crop)

# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    cv2.imshow("Image", image)
    key = cv2.waitKey(1) & 0xFF

    # if the 'r' key is pressed, reset the cropping region
    if key == ord("r"):
        image = clone.copy()

    # if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        break

logger.close()
# close all open windows
cv2.destroyAllWindows()
