import cv2 as cv
import numpy as np
from stereovision.module import Camera

class StereoCamera:
    def __init__(self):
        self.cam_list = []
        self.left_cam, self.right_cam = None, None
        self.distance_between_cameras = None
        self.camera_setting_values = {}

        self.InitCamList()

    #컴퓨터에 연결된 모든 웹캠리스트를 반환
    def InitCamList(self):
        index = 0
        while True:
            cam = cv.VideoCapture(index + cv.CAP_DSHOW)
            if cam.isOpened():
                self.cam_list.append(cam)
                index += 1
            elif index < 10:
                index += 1
            else:
                break

    #두 웹캠으로 촬영한 프레임을 반환
    def CamsRead(self):
        try:
            left = self.left_cam.Read()
            right = self.right_cam.Read()
        except:
            left = np.zeros((500,500,3), dtype= np.uint8)
            right = left.copy()
        return left, right

    #왼쪽과 오른쪽 웹캠 이외의 카메라를 종료
    def ReleaseOtherCamera(self, left_index, right_index):
        self.left_cam, self.right_cam = Camera.Camera(self.cam_list[left_index]), Camera.Camera(self.cam_list[right_index])
        cams = [self.cam_list[left_index], self.cam_list[right_index]]
        for cam in self.cam_list:
            if cam not in cams:
                cam.release()
                self.cam_list.remove(cam)

    #모든 웹캠들을 종료
    def ReleaseAll(self):
        for cam in self.cam_list:
            cam.release()

    #웹캠 설정 내용을 등록
    def AddSettingList(self, setting, value):
        self.camera_setting_values[setting] = value

    #설정 내용을 두 웹캠에 적용
    def ApplySetting(self):
        for key, value in self.camera_setting_values.items():
            self.left_cam.Setting(key, value)
            self.right_cam.Setting(key, value)