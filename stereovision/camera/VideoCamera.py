import cv2 as cv
import threading

class VideoCamera(object):
    def __init__(self):
        self.video = cv.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        (self.grabbed, self.frame) = self.video.read()
        image = self.frame
        jpeg = cv.imencode('.jpg', image)
        return jpeg.tobytes()