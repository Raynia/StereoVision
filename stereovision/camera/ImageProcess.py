import cv2 as cv
from stereovision.camera.AdditionalFunction import TupleAdd 

class ImageProcess:
    descriptor = {'ORB':cv.ORB_create(), }
    matcher = {'BF_NORM_HAMMING':cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True), }
    def __init__(self, target):
        self.target_gray = cv.cvtColor(target, cv.COLOR_BGR2GRAY)
        self.target_width, self.target_height = self.target_gray.shape[::-1]
        self.left_feature_points = []
        self.right_feature_points = []
        self.left_descriptor = []
        self.right_descriptor = []
        
    #
    def _TemplateTarget(self, image):
        res = cv.matchTemplate(image, self.target_gray, cv.TM_SQDIFF)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        top_left = min_loc
        bottom_right = (top_left[0] + self.target_width, top_left[1] + self.target_height)
        return top_left, bottom_right

    #
    def DetectingFeaturePoint(self, left_frame, right_frame):
        left_point = self._TemplateTarget(left_frame)
        sector_points = self._SearchSector(left_frame.shape, left_point)
        right_point = self._TemplateTarget(right_frame[sector_points[0][1]:sector_points[1][1],sector_points[0][0]:sector_points[1][0]])
        right_point = (TupleAdd(sector_points[0], right_point[0]), TupleAdd(sector_points[0], right_point[1]))

        self.left_feature_points, self.left_descriptor = self._DetectingFeaturePoint(left_frame, left_point)
        self.right_feature_points, self.right_descriptor = self._DetectingFeaturePoint(right_frame, right_point)

        return (left_point, right_point)

    #
    def MatchingFeaturePoint(self):
        matched_index = []
        matched_points_left = []
        matched_points_right = []
        try:
            temp = self.matcher['BF_NORM_HAMMING'].match(self.left_descriptor, self.right_descriptor)
            temp = sorted(temp, key = lambda x:x.distance)

            for ele in temp:
                matched_index.append((ele.queryIdx, ele.trainIdx))

            for ele in matched_index:
                matched_points_left.append(self.left_feature_points[ele[0]])
                matched_points_right.append(self.right_feature_points[ele[1]])

            return matched_points_left, matched_points_right
        except:
            return [], []

    #
    def _DetectingFeaturePoint(self, image, points):
        target = image[points[0][1]:points[1][1], points[0][0]:points[1][0]]
        kp, des = self.descriptor['ORB'].detectAndCompute(target, None)

        for ele in kp:
            ele.pt = (ele.pt[0] + points[0][0], ele.pt[1] + points[0][1])
        return kp, des

    #
    def _SearchSector(self, shape, points):
        top_y = 0 if points[0][1] - 50 < 0 else points[0][1] - 50
        bottom_y =points[1][1] + 50 if points[1][1] + 50 < shape[0] else shape[0] - 1

        left_x = points[1][0]
        return ((0, top_y),(left_x, bottom_y))
