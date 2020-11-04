import cv2 as cv
import numpy as np

class SelectBorder:
    def __init__(self, title):
        self.title = title      #콜백을 등록한 윈도우 타이틀
        self.draw_mode = False  #영역 지정 모드
        self.first_point = None #클릭한 좌표
        self.final_point = None #클릭을 뗀 좌표
        # self.target_image_list = []

    #마우스 콜백 - 물체 영역 지정
    def SelectObjectBorder(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:   #마우스 왼쪽 버튼 클릭
            self.draw_mode = True
            self.final_point = None
            self.first_point = (x, y)
        elif event == cv.EVENT_LBUTTONUP:   #마우스 왼쪽 버튼 클릭 해제
            param[0].fill(0)
            param[1].fill(0)
            self.draw_mode = False
            self.final_point = (x, y)
            if self.first_point != self.final_point:
                self.first_point, self.final_point = self.SortTopBottomPoint(self.first_point, self.final_point)
                cv.rectangle(param[0], self.first_point, self.final_point, (0,0,255), 2)
                cv.rectangle(param[1], self.first_point, self.final_point, (255,255,0), 2)
        elif self.draw_mode and event == cv.EVENT_MOUSEMOVE:    #영역 지정 중 마우스 이동
            param[0].fill(0)
            param[1].fill(0)
            cv.rectangle(param[0], self.first_point, (x, y), (255,0,0), 2)
            cv.rectangle(param[1], self.first_point, (x, y), (0,255,255), 2)

    #두 좌표를 받아서 좌상단 좌표와 우하단 좌표를 반환
    def SortTopBottomPoint(self, p1, p2):
        x1,x2,y1,y2 = 0,0,0,0
        x_sorted = (p1[0], p2[0]) if p1[0] < p2[0] else (p2[0], p1[0])
        y_sorted = (p1[1], p2[1]) if p1[1] < p2[1] else (p2[1], p1[1])
        return (x_sorted[0], y_sorted[0]),(x_sorted[1], y_sorted[1])

    #지정된 물체의 이미지와 그 이미지의 그레이스케일 이미지를 타겟 리스트에 추가
    def GetTarget(self, img):
        if self.first_point is not None and self.final_point is not None:
            target = img[self.first_point[1]:self.final_point[1],self.first_point[0]:self.final_point[0]]
            # target_gray = cv.cvtColor(target, cv.COLOR_BGR2GRAY)
            # self.target_image_list.append((target, target_gray))
            self.first_point, self.final_point = None, None
            return target

    # #타겟 리스트의 모든 이미지를 삭제
    # def AllDeleteTarget(self):
    #     self.target_image_list = []

    # #타겟 리스트의 index를 받아서 해당 이미지를 삭제
    # def DeleteTarget(self, index):
    #     del self.target_image_list[index]