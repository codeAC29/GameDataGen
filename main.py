"""
Gather information from frames of any game
Input: 1) Frame grabber to get each frame of any game
       2) key_info containing information about location
          from where values need to be extracted
Output: Detected numbers at locations of interest

Written by: Abhishek Chaurasia
Date      : 11th August, 2017
"""

import cv2

from argparse import ArgumentParser
from OCR import OCR
from video_reader import VideoReader

# Clear screen
print('\033[0;0f\033[0J')
# Color Palette
CP_R = '\033[31m'
CP_G = '\033[32m'
CP_B = '\033[34m'
CP_Y = '\033[33m'
CP_C = '\033[0m'

parser = ArgumentParser(description='Game Information Collector')
_ = parser.add_argument
_('--video_path', type=str,   default='./video.mp4', help='video location')
_('--key_info',   type=str,   default='./key_info.log', help='key information with coordinates')
_('--model',      type=str,   default='./Models/model.pyt', help='model weights')
_('--debug',      type=bool,  default=False, help='Display images at each step')
args = parser.parse_args()


def print_val(info, pad, n, N):
    print('{}{:>{width}}{}'.
            format(CP_R, info, CP_C, width=pad), end="")
    if n < N-1:
        print(' |', end="")
    else:
        print("", end="")


def main():
    print('{}{:=<50}{}'.format(CP_Y, '', CP_C))
    print('{}**{}{:^46}{}**{}'.
            format(CP_Y, CP_R, 'Game Informantion Collector', CP_Y, CP_C))
    print('{}**{}{:^46}{}**{}'.
            format(CP_Y, CP_R, 'By: Abhishek Chaurasia', CP_Y, CP_C))
    print('{}{:=<50}{}'.format(CP_Y, '', CP_C))
    # Grab frames from screen or video
    # Replace it with any other frame grabber
    frame_grabber = VideoReader(args.video_path)

    # Initialization
    ocr = OCR(args.model, args.debug)
    items = {}
    n_items = 0

    keyvalues = open(args.key_info, 'r')
    # Ignore first two lines
    keyvalues.readline()
    keyvalues.readline()

    for line in keyvalues:
        item = line.split()
        # parsed info:    keyword | tx     | ty     | bx     | by
        items[n_items] = (item[0], item[2], item[4], item[6], item[8])
        n_items += 1

    ########################################
    # Ignore this section:
    # Important only when you care about printed values
    print('{:=<50}'.format(''))
    pad = (50//n_items) - 2
    for n_item in items:
        print_val(items[n_item][0], pad, n_item, len(items))
    print('\n{:-<50}'.format(''))
    ########################################

    # Get next frame
    while frame_grabber.next_frame():
        current_frame = frame_grabber.frame
        # Crop section of the frame containing value you are interested in
        for n_item in items:
            tx = int(items[n_item][1])
            ty = int(items[n_item][2])
            bx = int(items[n_item][3])
            by = int(items[n_item][4])
            key_part = current_frame[ty:by, tx:bx, :]

            # send the cropped area and get its value
            value = ocr.forward(key_part)

            # Create box around idividual ROIs
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(current_frame, str(value),
                    (tx-10,ty-10), font, 1, (255,255,255), 1)
            # cv2.rectangle(current_frame, (tx, ty), (bx, by), (0, 255, 0), 1)
            print_val(value, pad, n_item, len(items))
        print("")

        if args.debug:
            pass
        else:
            cv2.startWindowThread()
            cv2.namedWindow("Video")
        cv2.imshow('Video', current_frame)
        if args.debug:
            cv2.waitKey(1)


if __name__ == '__main__':
    main()
