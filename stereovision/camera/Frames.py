import cv2 as cv
import numpy as np
from stereovision.camera import ImageProcess
from stereovision.camera import PixelCalculator as pc

class Frames:
    def __init__(self):
        self.left_frame, self.right_frame = None, None
        self.left_gray, self.right_gray = None, None
        self.main_frame = np.zeros((10,10,3), dtype=np.uint8)

        self.pixel_calculator = pc.PixelCalculator((1280, 960), 200, 80)

        self.target_image_list = []
        self.target_feature_points_list = []
        self.target_border_points_list = []
        self.target_distance_list = []

        self.left_back, self.right_back = None, None

    #
    def StoreFrame(self, left, right):
        self.left_frame = left
        self.right_frame = right
        self.left_gray = cv.cvtColor(self.left_frame, cv.COLOR_BGR2GRAY)
        self.right_gray = cv.cvtColor(self.right_frame, cv.COLOR_BGR2GRAY)

    #
    def SelectMainFrame(self, index):
        if self.target_image_list:
            self.target_border_points_list.clear()
            self.target_feature_points_list.clear()
            self.target_distance_list.clear()
            self.left_back = np.zeros(self.left_frame.shape, dtype=np.uint8)
            self.right_back = self.left_back.copy()
            for ele in self.target_image_list:
                self.target_border_points_list.append(ele.DetectingFeaturePoint(self.left_gray, self.right_gray))
                self.target_feature_points_list.append(ele.MatchingFeaturePoint())
        self.DrawBoder(index)
        self.DrawFeaturePoints(index)
        self.CalculateDistance()

        if index == 0:
            self.main_frame = self.left_frame.copy()
        else:
            self.main_frame = self.right_frame.copy()

        self.PrintDistance(index)
    # #
    # def ConnectTargetList(self, target_list):
    #     self.target_image_list = target_list    

    #
    def AddTarget(self, image):
        self.target_image_list.append(ImageProcess.ImageProcess(image))

    #타겟 리스트의 모든 이미지를 삭제
    def AllDeleteTarget(self):
        self.target_image_list.clear()
        self.target_feature_points_list.clear()
        self.target_border_points_list.clear()
        self.target_distance_list.clear()

    #타겟 리스트의 index를 받아서 해당 이미지를 삭제
    def DeleteTarget(self, index):
        del self.target_image_list[index]
        del self.target_feature_points_list[index]
        del self.target_border_points_list[index]
        del self.target_distance_list[index]

    #
    def ProcessingImage(self):
        pass

    #
    def DrawFeaturePoints(self, index):
        if self.target_feature_points_list:
            for ele in self.target_feature_points_list:
                if index == 0:
                    cv.drawKeypoints(self.left_frame, ele[0], self.left_frame)
                else:
                    cv.drawKeypoints(self.right_frame, ele[1], self.right_frame)

    #
    def DrawBoder(self, index):
        for ele in self.target_border_points_list:
            if index == 0:
                cv.rectangle(self.left_frame, ele[0][0], ele[0][1], (0, 0, 255), 2)
            else:
                cv.rectangle(self.right_frame, ele[1][0], ele[1][1], (0, 0, 255), 2)

    #
    def DetectAndMatch(self):
        self.target_border_points_list.clear()
        for ele in self.target_image_list:
            self.target_border_points_list.append(ele.DetectingFeaturePoint(self.left_gray, self.right_gray))
            self.target_feature_points_list.append(ele.MatchingFeaturePoint())

    #
    def CalculateDistance(self):
        if self.target_feature_points_list:
            for ele in self.target_feature_points_list:
                temp_list = []
                for index, point in enumerate(ele[0]):
                    temp_list.append(self.pixel_calculator.DistanceCalc(point.pt, ele[1][index].pt))
                    # print(self.pixel_calculator.DistanceCalc(point.pt, ele[1][index].pt))
            try:
                self.target_distance_list.append(sum(temp_list) // len(temp_list))
            except:
                print("err")
                self.target_distance_list.append(0)
        return self.target_distance_list

    #
    def SettingPixelCalculator(self, resolution, distance, fov):
        self.pixel_calculator.SettingCamera(resolution, distance, fov)

    #
    def PrintDistance(self, index):
        for idx, distance in enumerate(self.target_distance_list):
            try:
                cv.putText(self.main_frame, str(distance), self.target_border_points_list[idx][index][0], cv.FONT_HERSHEY_SIMPLEX,2,(0,0,255),1)
            except:
                pass
    #
    def GetTargetDistanceList(self):
        return self.target_distance_list
    #
    def GetBorderPointsList(self):
        return self.target_border_points_list