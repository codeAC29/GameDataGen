import cv2

# Color Palette
CP_R = '\033[31m'
CP_G = '\033[32m'
CP_B = '\033[34m'
CP_Y = '\033[33m'
CP_C = '\033[0m'


class VideoReader():
    def __init__(self, video_path):
        super(VideoReader, self).__init__()

        self.cap = cv2.VideoCapture(video_path)
        self.n_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frame_count = 0
        width = self.cap.get(3)
        height = self.cap.get(4)
        print('{}Frame Resolution: {}{} x {}{}'.
                format(CP_Y, CP_B, int(width), int(height), CP_C))

    def next_frame(self):
        if self.frame_count < self.n_frames:
            ret, self.frame = self.cap.read()
            self.frame_count += 1

            return ret
        else:
            return None
