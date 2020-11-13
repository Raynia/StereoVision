import cv2 as cv
import numpy as np
import threading
from stereovision.module import Camera

class StereoCamera:
    def __init__(self):
        self.flag, self.pre_flag = False, False
        self.cam_list = []
        self.pre_frame = []
        self.left_cam, self.right_cam = None, None
        self.left_frame, self.right_frame = None, None
        self.distance_between_cameras = None
        self.camera_setting_values = {}
        self.capture = threading.Thread(target=self.CamsRead, args=())
        #self.preCapture = threading.Thread(target=self.CamsPreview, args=())
        self.capture.setDaemon(True)
        #self.preCapture.setDaemon(True)
        self.InitCamList()

        print(self.cam_list)

    def __del__(self):
        self.flag = False
        self.pre_flag = False
        self.ReleaseAll()


    #컴퓨터에 연결된 모든 웹캠리스트를 반환
    def InitCamList(self):
        index = 0
        while True:
            cam = cv.VideoCapture(index + cv.CAP_DSHOW)
            if cam.isOpened():
                self.cam_list.append(Camera.Camera(cam))
                index += 1
            elif index < 10:
                index += 1
            else:
                break


    #두 웹캠으로 촬영한 프레임을 반환
    def CamsRead(self):
        while self.flag:
            try:
                self.left_frame = self.left_cam.Read()
                self.right_frame = self.right_cam.Read()
            except:
                self.left_frame = np.zeros((500,500,3), dtype= np.uint8)
                self.right_frame = self.left_frame.copy()

    # #
    # def CamsPreview(self):
    #     while self.pre_flag:
    #         self.pre_frame.clear()
    #         for cam in self.cam_list:
    #             self.pre_frame.append(cam.Read())

    #왼쪽과 오른쪽 웹캠 이외의 카메라를 종료
    def ReleaseOtherCamera(self, left_index, right_index):
        self.left_cam, self.right_cam = self.cam_list[left_index], self.cam_list[right_index]
        cams = [self.left_cam, self.right_cam]
        for cam in self.cam_list:
            if cam not in cams:
                cam.Release()
                self.cam_list.remove(cam)
        if not self.flag:
            self.flag = True
            self.capture.start()
        self.pre_flag = False

    #모든 웹캠들을 종료
    def ReleaseAll(self):
        for cam in self.cam_list:
            cam.Release()
            del cam

    #웹캠 설정 내용을 등록
    def AddSettingList(self, setting, value):
        self.camera_setting_values[setting] = value

    #설정 내용을 두 웹캠에 적용
    def ApplySetting(self):
        for key, value in self.camera_setting_values.items():
            self.left_cam.Setting(key, value)
            self.right_cam.Setting(key, value)

    def GetFrame(self, index):
        frame = self.cam_list[index].Read()
        image = cv.imencode('.jpg', frame)
        return image[1].tobytes()
    
    def GetLRFrame(self, lr):
        frame = self.left_frame if lr == 0 else self.right_frame
        image = cv.imencode('.jpg', frame)
        return image[1].tobytes()
