################################################################
#         동아대학교 컴퓨터 공학과 2020년도 졸업 프로젝트      #
#                      픽셀 거리 계산 모듈                     #
################################################################
#import
################################################################

import math

################################################################
#변수 선언
################################################################

#해상도 값 <dict>
#UHD : 3840 x 2160
#QHD : 2560 x 1440
#FHD : 1920 x 1080
resolution = {'UHD':(3840, 2160),'QHD':(2560, 1440),'FHD':(1920, 1080),'CUS':(2592, 1944),}

class PixelCalculator:
    #
    def __init__(self, resolution, distance, fov=None, **camera_data):

        #이미지 높이,너비 <int>
        self.image_width, self.image_height = resolution

        #이미지 높이,너비 중심 <int>
        self.image_height_half, self.image_width_half = self.image_height // 2, self.image_width // 2

        self.camera_between = distance

        self.camera_between_half = distance // 2

        if not camera_data:
            #카메라 (통합?) 화각 <float>
            self.camera_fov = fov

            #화각의 절반 <float>
            self.camera_fov_half = fov / 2

        else:
            #카메라 센서 대각 길이 <int>
            self.camera_sensor_diagonal = camera_data['sensor_diagonal_len']

            #카메라 초점거리 <int>
            self.camera_focal_length = camera_data['focial_len']

            self.camera_fov = -1
            self.camera_fov_half = -1

            self.FovCalculate()

        self.pixel_height = self.image_width_half / math.tan(math.radians(self.camera_fov_half))

    #카메라 설정 수정
    #return <None>
    def SettingCamera(self, resolution, distance, fov=None, **camera_data):
        #이미지 높이,너비 <int>
        self.image_width, self.image_height = resolution

        #이미지 높이,너비 중심 <int>
        self.image_height_half, self.image_width_half = self.image_height // 2, self.image_width // 2

        self.camera_between = distance

        self.camera_between_half = distance // 2

        if not camera_data:
            #카메라 (통합?) 화각 <float>
            self.camera_fov = fov

            #화각의 절반 <float>
            self.camera_fov_half = fov / 2

        else:
            #카메라 센서 대각 길이 <int>
            self.camera_sensor_diagonal = camera_data['sensor_diagonal_len']

            #카메라 초점거리 <int>
            self.camera_focal_length = camera_data['focial_len']

            self.camera_fov = -1
            self.camera_fov_half = -1

            self.FovCalculate()

        self.pixel_height = self.image_width_half / math.tan(math.radians(self.camera_fov_half))

    #카메라 정보로 화각계산
    #return <None>
    def FovCalculate(self):
        #화각 공식
        # 2 * tan-1( 카메라센서 대각길이 / (2 * 카메라 초점 거리) )
        self.camera_fov = math.degrees(math.atan(self.camera_sensor_diagonal / ( 2 * self.camera_focal_length ) ) )*2
        self.camera_fov_half = self.camera_fov / 2

    #픽셀이 이미지의 중심 y축을 기준으로 좌측, 우측 중 어디에 있는지 확인
    #args <int> 픽셀의 x 값
    #return <bool> True : 좌측 , False : 우측
    def WhereInScreen(self, x):
        return self.image_width_half >= x

    #두 픽셀을 이용하여 거리 계산
    #args <(int,int),(int,int)> 각 픽셀의 (y,x) 값
    #return <float> 거리
    def DistanceCalc(self, pixel_1, pixel_2):
        try:
            centerPosition_1, centerPosition_2 = self.WhereInScreen(pixel_1[0]), self.WhereInScreen(pixel_2[0])
            p_1 = pixel_1[0] >= self.image_width_half and pixel_1[0] - self.image_width_half or self.image_width_half - pixel_1[0]
            p_2 = pixel_2[0] >= self.image_width_half and pixel_2[0] - self.image_width_half or self.image_width_half - pixel_2[0]
            # print(pixel_1,pixel_2)
            #객체가 좌측에 위치
            if centerPosition_1 and centerPosition_2:
                cita_1 = 90 + self.CalcCita(p_1)
                cita_2 = 90 - self.CalcCita(p_2)

            elif not centerPosition_1:
                #객체가 중앙에 위치
                if centerPosition_2:
                    cita_1 = 90 - self.CalcCita(p_1)
                    cita_2 = 90 - self.CalcCita(p_2)

                #객체가 우측에 위치
                else:
                    cita_1 = 90 - self.CalcCita(p_1)
                    cita_2 = 90 + self.CalcCita(p_2)

            cita_3 = 180 - (cita_1 + cita_2)
            #print(f'citaA : {cita_1} citaB : {cita_2} citaR : {cita_3}')
            rc = self.camera_between*math.sin(math.radians(cita_1)) / math.sin(math.radians(cita_3)) * math.sin(math.radians(cita_2))
            if cita_1 > 90:
                
                ar = rc / (math.tan(math.radians(180 - cita_1)))
                rm = self.camera_between_half + ar
                mc = math.sqrt(rm**2 + rc**2)
            elif cita_2 > 90:
                br = rc / (math.tan(math.radians(180 - cita_2)))
                rm = self.camera_between_half + br
                mc = math.sqrt(rm**2 + rc**2)
            elif cita_1 > cita_2:
                bc = (self.camera_between*math.sin(math.radians(cita_2))) / math.sin(math.radians(cita_3))
                rm = self.camera_between_half - bc*math.cos(math.radians(cita_2))
                mc = math.sqrt(rm**2+rc**2)
            elif cita_1 < cita_2:
                ac = (self.camera_between*math.sin(math.radians(cita_1))) / math.sin(math.radians(cita_3))
                rm = self.camera_between_half - ac*math.cos(math.radians(cita_1))
                mc = math.sqrt(rm**2+rc**2)
            else:
                pass

            cita_3 = cita_3 < 0 and -cita_3 or cita_3
            # print(f'MC : {mc}, RC : {rc}')
            return math.floor(mc)
        except:
            return 0

    #이미지의 중심선과 픽셀까지의 선 사이에 끼인각을 구함
    #args <int> 중심선에서 x 까지의 거리
    #return <float> 끼인각의 radians 값
    def CalcCita(self, x):
        ci = (x / self.image_width_half)*math.tan(math.radians(self.camera_fov_half))
        #print(ci)
        return math.degrees(math.atan(ci))