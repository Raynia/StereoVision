import cv2 as cv
import numpy as np
from stereovision.camera import PixelCalculator as pc
from stereovision.module import SelectBorder
from stereovision.module import StereoCamera
from stereovision.module import Frames
from sys import maxsize

class MainProgram:
    Resolution = [(1280, 960), (1920, 1080), (2592, 1944)]
    def __init__(self, title):
        self.title = title
        self.frames = None
        self.select_border = None
        self.target_image_list = []

        self.pixel_calculator = pc.PixelCalculator((1280, 960), 200, 80)

    #메인 프로그램 실행
    def MainWindow(self):
        title = 'Mode Select'
        cv.namedWindow(title)
        cv.createTrackbar('Image/Cam', title, 1, 1, self._onChange)
        image = np.zeros((10,500), dtype=np.uint8)

        cv.imshow(title, image)

        key = cv.waitKey(0)

        if key == ord('s') or key == ord('S'):
            mode = cv.getTrackbarPos('Image/Cam', title)
            self.frames = Frames.Frames()
            self.select_border = SelectBorder.SelectBorder(title)
            self.target_border = []

            cv.destroyWindow(title)

            self._Reticle()

            if mode == 1:
                self.stereo_camera = StereoCamera.StereoCamera()
                self._CamSettingWindow()

            self._CalculatorWindow(mode)
                
        cv.destroyAllWindows()

    #거리 계산 화면
    def _CalculatorWindow(self, mode):
        cv.namedWindow(self.title)
        cv.createTrackbar('Left/Right', self.title, 0, 1, self._onChange)

        if mode == 1:
            left_image, right_image = self.stereo_camera.CamsRead()
        else:
            # _left_image = cv.imread('left_frame.jpg')
            # _right_image = cv.imread('right_frame.jpg')
            _left_image = cv.imread('Left.bmp')
            _right_image = cv.imread('Right.bmp')
            _left_image = cv.resize(_left_image, (1280, 960))
            _right_image = cv.resize(_right_image, (1280, 960))
            left_image = _left_image.copy()
            right_image = _right_image.copy()
        
        self.frames.StoreFrame(left_image, right_image)
        self.InitTargets()
        #마우스 왼쪽 버튼으로 물체 영역 지정
        cv.setMouseCallback(self.title, self.select_border.SelectObjectBorder, param=self.target_border)
        while True:
            if mode == 1:
                left_image, right_image = self.stereo_camera.CamsRead()
            else:
                left_image = _left_image.copy()
                right_image = _right_image.copy()

            self.frames.StoreFrame(left_image, right_image)

            LR = cv.getTrackbarPos('Left/Right', self.title)
            self.frames.SelectMainFrame(LR)
            cv.imshow(self.title, cv.subtract(cv.add(self.frames.main_frame, self.target_border[0]), self.target_border[1]))

            key = cv.waitKey(1)

            if key == 27 or cv.getWindowProperty(self.title, cv.WND_PROP_VISIBLE) < 1:   #프로그램 종료
                break
            elif key == ord('s') or key == ord('S'):    #타겟 리스트에 현재 선택한 물체 추가
                target = self.select_border.GetTarget(self.frames.main_frame)
                self.AddTargetImage(target)
            elif key == ord('r') or key == ord('R'):    #현재 영역 지정 취소
                self.ResetBorder()
            elif key == ord('t') or key == ord('T'):    #타겟 리스트 윈도우
                self.TargetWindow()
            elif key == ord('d') or key == ord('D'):    #타겟 리스트 삭제
                self.ResetTargets()
            elif key == ord('q') or key == ord('Q'):    #웹캠 세팅 화면
                self._CamSettingWindow()
                self.frames.StoreFrame(*self.stereo_camera.CamsRead())
                self.InitTargets()
            elif key == ord('w') or key == ord('W'):    #캡쳐 후 저장
                cv.imwrite('left_frame.jpg', self.frames.left_frame)
                cv.imwrite('right_frame.jpg', self.frames.right_frame)
            elif key == 9:                              #웹캠 좌우 전환
                cv.setTrackbarPos('Left/Right', self.title, LR^1)
                
        if mode == 1:
            self.stereo_camera.ReleaseAll()

        cv.destroyWindow(self.title)

    #웹캠 세팅 화면
    def _CamSettingWindow(self):
        title = 'Camera Setting'

        #윈도우 세팅
        cv.namedWindow(title)
        frame, temp = None, None

        print(self.stereo_camera.cam_list)

        #웹캠이 두개 이상일 때만 작동
        if len(self.stereo_camera.cam_list) >= 2:
            cv.createTrackbar('Left', title, 0, len(self.stereo_camera.cam_list)-1, self._onChange)
            cv.createTrackbar('Right', title, 1, len(self.stereo_camera.cam_list)-1, self._onChange)
            cv.createTrackbar('Resolution', title, 0, 1, self._onChange)
            cv.createTrackbar('Distance between Cameras', title, 1, 1, self._onChange)
            #Loop
            while True:
                left_index, right_index = cv.getTrackbarPos('Left', title), cv.getTrackbarPos('Right', title)
                let, frame = self.stereo_camera.cam_list[left_index].read()
                let, temp = self.stereo_camera.cam_list[right_index].read()

                frame = cv.resize(frame,dsize=(640,480), interpolation=cv.INTER_AREA)
                temp = cv.resize(temp,dsize=(640,480), interpolation=cv.INTER_AREA)

                frame = cv.add(frame, self.reticle[0])
                frame = cv.subtract(frame, self.reticle[1])
                temp = cv.add(temp, self.reticle[0])
                temp = cv.subtract(temp, self.reticle[1])

                frame = np.concatenate((frame,temp), axis=1)

                cv.imshow(title, frame)

                key = cv.waitKey(1)

                if key == ord('s') or key == ord('S'):
                    self.stereo_camera.ReleaseOtherCamera(left_index, right_index)
                    self._CamSetting(left_index, right_index, self.Resolution[cv.getTrackbarPos('Resolution', title)], (cv.getTrackbarPos('Distance between Cameras', title)+1)*100)
                    self.stereo_camera.ApplySetting()
                    break
                elif key == 27 or cv.getWindowProperty(title, cv.WND_PROP_VISIBLE) < 1:
                    break
        else:
            print("두 대 이상의 카메라가 필요합니다.")
            cv.imshow(title, np.zeros((480,640,3),dtype=np.uint8))
            cv.waitKey(0)
            self.stereo_camera.ReleaseAll()

        cv.destroyWindow(title)

    #타겟 리스트의 이미지를 보여줌
    def TargetWindow(self):
        if len(self.target_image_list) > 0:
            title = 'Tagets'
            cv.namedWindow(title)
            cv.createTrackbar('index', title, 0, len(self.target_image_list)-1, self._onChange)
            while True:
                index = cv.getTrackbarPos('index',title)
                cv.imshow(title, self.target_image_list[index])

                key = cv.waitKey(1)

                if key == 27 or cv.getWindowProperty(title, cv.WND_PROP_VISIBLE) < 1:
                    break
                elif key == ord('d') or key == ord('D'):
                    self.DeleteTarget(index)
                    if len(self.target_image_list) > 0:
                        cv.setTrackbarMax('index', title, len(self.target_image_list)-1)
                        cv.setTrackbarPos('index', title, 0)
                    else:
                        break
                elif key == 9:
                        index = cv.getTrackbarPos('index', title)
                        if index < (len(self.target_image_list)-1):
                            cv.setTrackbarPos('index', title, index+1)
                        else:
                            cv.setTrackbarPos('index', title, 0)
            cv.destroyWindow(title)

    #설정 화면에서 설정값을 받아서 적용
    def _CamSetting(self, left_index, right_index, resolution, distance):
        self.frames.SettingPixelCalculator(resolution, distance, 80)
        self.stereo_camera.AddSettingList('Resolution', resolution)
        self.stereo_camera.distance_between_cameras = distance
        self.stereo_camera.AddSettingList('AutoFocus', 0)
        self.stereo_camera.AddSettingList('Format', cv.VideoWriter_fourcc('M','J','P','G'))

    #
    def AddTargetImage(self, image):
        self.target_image_list.append(image)
        self.frames.AddTarget(image)
        self.ResetBorder()
    
    #
    def InitTargets(self):
        self.InitBorder()
        self.ResetTargets()

    #
    def ResetTargets(self):
        self.frames.AllDeleteTarget()
        self.target_image_list.clear()

    #
    def InitBorder(self):
        for ele in self.target_border:
            del ele
        self.target_border.append(np.zeros(self.frames.left_frame.shape, dtype=np.uint8))
        self.target_border.append(np.zeros(self.frames.left_frame.shape, dtype=np.uint8))

    #
    def ResetBorder(self):
        self.target_border[0].fill(0)
        self.target_border[1].fill(0)

    #
    def DeleteTarget(self, index):
        del self.target_image_list[index]
        self.frames.DeleteTarget(index)

    #
    def _Reticle(self):
        self.reticle = []
        temp = np.zeros((480,640,3), dtype=np.uint8)
        self.reticle.append(temp.copy())
        self.reticle.append(temp)

        cv.line(self.reticle[0],(0,239),(639,239),(0,255,0),2)
        cv.line(self.reticle[0],(319,0),(319,479),(0,255,0),2)

        cv.line(self.reticle[1],(0,239),(639,239),(255,0,255),2)
        cv.line(self.reticle[1],(319,0),(319,479),(255,0,255),2)

    def _onChange(self, pos):
        pass
