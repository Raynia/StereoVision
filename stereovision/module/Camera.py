import cv2 as cv

class Camera:
    def __init__(self, cam):
        self.cam = cam
    #
    def Read(self):
        let, frame = self.cam.read()
        return frame

    #설정 내용을 웹캠에 적용
    def Setting(self, setting, value):
        if setting == 'Resolution':
            self.cam.set(cv.CAP_PROP_FRAME_WIDTH, value[0])
            self.cam.set(cv.CAP_PROP_FRAME_HEIGHT, value[1])
        elif setting == 'AutoFocus':
            self.cam.set(cv.CAP_PROP_AUTOFOCUS, value)
        elif setting == 'Format':
            self.cam.set(cv.CAP_PROP_FOURCC, value)
    
    def Release(self):
        self.cam.release()