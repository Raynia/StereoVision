import cv2 as cv
from stereovision.camera import PixelCalculator as pc
from stereovision.module import StereoCamera
import threading

class VideoCamera:
    def __init__(self):
        f = open('log.txt', mode='wt', encoding='utf-8')
        self.video = cv.VideoCapture(0)
        if self.video.isOpened():            
            (self.grabbed, self.frame) = self.video.read()
            threading.Thread(target=self.update, args=()).start()
            f.write('success') 
        else:
            f = open('error.txt', mode='wt', encoding='utf-8')
            f.write('fail')   
        f.close()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        (self.grabbed, self.frame) = self.video.read()
        image = self.frame
        jpeg = cv.imencode('.jpg', image)
        return jpeg.tobytes()