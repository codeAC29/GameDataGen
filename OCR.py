# Extracting numbers taken from:
# http://www.pyimagesearch.com/2017/02/13/recognizing-digits-with-opencv-and-python/

import cv2
import torch
import torch.nn as nn
from torch.autograd import Variable

import imutils
from imutils import contours
from imutils.perspective import four_point_transform
from torchvision import transforms
from PIL import Image

from Model.model import Net


class OCR():
    def __init__(self, model_path, debug):
        super(OCR, self).__init__()
        # Load the model definition
        self.model = Net()
        # Load state dictionation of model
        self.model_weights = torch.load(model_path)
        # Update the weights of model
        self.model.load_state_dict(self.model_weights)
        self.model.eval()

        # Transforms to be performed on the thresholded image
        # before sending it as input to the network
        tune_val = 15
        self.transform = transforms.Compose([
            transforms.Scale(tune_val),           # FIXME: Tune this value according to your data if required
            transforms.Pad(28 - tune_val),             # Pad + Scale = 28
            transforms.CenterCrop(28),
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))])    # Network was trained using this value

        self.debug = debug


    def display_detail(self, title, frame):
        if self.debug:
            cv2.imshow(title, frame)
            cv2.waitKey(0)


    def forward(self, frame):
        value = 0
        # pre-process the frame by resizing it, converting it to
        # graycale, blurring it, and computing an edge map
        frame = imutils.resize(frame, height=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # threshold the warped frame, then apply a series of morphological
        # operations to cleanup the thresholded frame
        # FIXME: THRESH_BINARY_INV for light background and dark foreground
        thresh = cv2.threshold(gray, 0, 255,
                cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        self.display_detail('Crop', frame)
        self.display_detail('Threshold Numbers', thresh)

        digitCnts = digit_cor(thresh)
        # sort the contours from left-to-right, then initialize the
        # actual digits themselves
        digitCnts = contours.sort_contours(digitCnts,
                method="left-to-right")[0]
        digits = []


        # loop over each of the digits
        for c in digitCnts:
            # extract the digit ROI
            (x, y, w, h) = cv2.boundingRect(c)

            # Extract ROI
            roi = gray[y:y + h, x:x + w]
            self.display_detail('Extracted Number', roi)

            # Convert ROI from numpy to PIL in order to use torch transform
            PIL_roi = Image.fromarray(roi)
            rescaled_roi = self.transform(PIL_roi)

            net_out = self.model(Variable(rescaled_roi.unsqueeze(0)))

            # find argMax to get detected number
            pred = net_out.data.max(1, keepdim=True)[1]
            value = 10*value + pred[0][0]       # 2 -> 20+9 -> 29

        return value


# Accepts an input thresholded binary frame and returns all points occupied by each number
def digit_cor(thresh):
    # find contours in the thresholded frame, then initialize the
    # digit contours lists
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    digitCnts = []

    # loop over the digit area candidates
    for c in cnts:
        # compute the bounding box of the contour
        (x, y, w, h) = cv2.boundingRect(c)

        # if the contour is sufficiently large, it must be a digit
        #if w >= 15 and (h >= 30 and h <= 40):
        digitCnts.append(c)

    return digitCnts

