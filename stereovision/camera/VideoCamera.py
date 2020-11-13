import cv2 as cv
from stereovision.camera import PixelCalculator as pc
from stereovision.camera import StereoCamera
import threading

class VideoCamera:
    def __init__(self):

        # self.video = cv.VideoCapture(1 + cv.CAP_DSHOW)
        # (self.grabbed, self.frame) = self.video.read()        
        # threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        #(self.grabbed, self.frame) = self.video.read()
        image = self.frame
        jpeg = cv.imencode('.jpg', image)
        return jpeg[1].tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()  