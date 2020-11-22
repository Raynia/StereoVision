import json
import cv2
import numpy as np
from collections import OrderedDict

from django.conf import settings
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.core import serializers

from .camera import Frames
from .camera import PixelCalculator as pc
from .camera import StereoCamera as sc
from .camera import AdditionalFunction as af
from .models import CameraList, PreviewCamera, TargetImage, Userdata

pixelCalculator = pc.PixelCalculator((1280,960), 200, 80)
stereoCamera = sc.StereoCamera()
stereoCamera.AddSettingList('AutoFocus', 0)
stereoCamera.AddSettingList('Format', cv2.VideoWriter_fourcc('M','J','P','G'))
frames = Frames.Frames()

# Stereovision View
#########################################################################
def init(request):
    init_list = [Userdata.objects.all(), TargetImage.objects.all(), CameraList.objects.all(), PreviewCamera.objects.all()]

    #DB 초기화
    for i in init_list:
        if i.exists():
            i.delete()

    # camera_list = CameraList.objects.all()
    # if camera_list.exists():
    #     camera_list.delete()
        
    for idx, cam in enumerate(stereoCamera.cam_list):
        q = CameraList(camera_index = idx)
        q.save()
    
    if len(stereoCamera.cam_list) >= 2:
        q = PreviewCamera(camera_left = 0, camera_right = 1)
        q.save()
    stereoCamera.pre_flag = True
    camera_list = CameraList.objects.all()
    camera_preview_list = PreviewCamera.objects.all()
    contents = {
        'list' : camera_list,
        'preview' : camera_preview_list,
    }
        
    # stereoCamera.ReleaseOtherCamera(0,1)

    return render(request, 'stereovision/setting.html', contents)
    # return HttpResponseRedirect(reverse('stereovision:setting')) 

def main(request):
    CameraList.objects.all().delete()
    p = PreviewCamera.objects.all()
    for cam in p:
        if cam.camera_left >= 2:
            if cam.camera_right == 0:
                cam.camera_left = 1
            else:
                cam.camera_left = 0
        if cam.camera_right >= 2:
            if cam.camera_left == 0:
                cam.camera_right = 1
            else:
                cam.camera_right = 0
        cam.save()

    u = Userdata.objects.all()
    if u.exists():
        userdata_list = Userdata.objects.first()    
    else:
        userdata_list = None

    contents = {
        'userdata_list': userdata_list,
    }

    stereoCamera.ReleaseOtherCamera(userdata_list.user_left_camera, userdata_list.user_right_camera)
    stereoCamera.ApplySetting()
    stereoCamera.ReadStart()
    return render(request, 'stereovision/main.html', contents)

def setting(request):
    stereoCamera.pre_flag = True
    camera_list = CameraList.objects.all()
    for idx, cam in enumerate(stereoCamera.cam_list):
        q = CameraList(camera_index = idx)
        q.save()
    
    camera_list = CameraList.objects.all()
    camera_preview_list = PreviewCamera.objects.all()
    contents = {
        'list' : camera_list,
        'preview' : camera_preview_list,
    }
    return render(request, 'stereovision/setting.html', contents)

def genLR(lr):
    while True:
        frame = stereoCamera.GetLRFrame(lr)
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen(idx):
    while True:
        frame = stereoCamera.GetFrame(idx)
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')  

#Streaming left-side video which player choose
def video_left(request):
    try:
        return StreamingHttpResponse(genLR(0), content_type='multipart/x-mixed-replace;boundary=frame')
    except:  # This is bad! replace it with proper handling
        pass

def video_right(request):
    try:
        return StreamingHttpResponse(genLR(1), content_type='multipart/x-mixed-replace;boundary=frame')
    except:  # This is bad! replace it with proper handling
        pass

#Streaming right-side video which player choose
def pre_video_left(request):
    try:
        pre = PreviewCamera.objects.first()
        return StreamingHttpResponse(gen(pre.camera_left), content_type='multipart/x-mixed-replace;boundary=frame')
    except:  # This is bad! replace it with proper handling
        pass

def pre_video_right(request):
    try:
        pre = PreviewCamera.objects.first()
        return StreamingHttpResponse(gen(pre.camera_right), content_type='multipart/x-mixed-replace;boundary=frame')
    except:  # This is bad! replace it with proper handling
        pass


def camera_preview(request):
    left_camera = request.POST['left_camera']
    right_camera = request.POST['right_camera']

    camera_preview_list = PreviewCamera.objects.all()
    camera_preview_list.delete()

    q = PreviewCamera(camera_left = left_camera, camera_right = right_camera)
    q.save()

    camera_list = CameraList.objects.all()
    camera_preview_list = PreviewCamera.objects.all()
    contents = {
        'list' : camera_list,
        'preview' : camera_preview_list,
    }

    return render(request, 'stereovision/setting.html', contents)

def userdata_update(request): 
    left_camera = request.POST['left_camera']
    right_camera = request.POST['right_camera']
    width = int(request.POST['resolution'])
    height = int(width) // 4 * 3
    distance = int(request.POST['distance'])

    stereoCamera.AddSettingList('Resolution',(width, height))
    pixelCalculator.SettingCamera((width, height), distance, 80)

    stereoCamera.pre_flag = False

    q = Userdata.objects.all()
    if q.exists():
        q.delete()
    
    d = Userdata(user_left_camera = left_camera, user_right_camera = right_camera, user_width = width, user_height = height, user_distance = distance)
    d.save()
    
    return HttpResponseRedirect(reverse('stereovision:main'))
    
def border_selection(request):
    
    camera_pos = request.POST['camera_pos']
    test_bytes_var = b'\x00'
    x1, y1 = int(request.POST['x1']), int(request.POST['y1']) # start point
    x2, y2 = int(request.POST['x2']), int(request.POST['y2']) # destination point

    align = af.SortTopBottomPoint((x1,y1),(x2,y2))

    lr = 0 if camera_pos == "left" else 1
    frame = stereoCamera.GetLRFrame(lr)   
    ori_frame = stereoCamera.GetBothFrame()
    
    # frames.StoreFrame(ori_frame[0],ori_frame[1])
    if lr == 0:
        frames.AddTarget(ori_frame[0][align[0][1]:align[1][1],align[0][0]:align[1][0]])
    else:
        frames.AddTarget(ori_frame[1][align[0][1]:align[1][1],align[0][0]:align[1][0]])
    image = np.asarray(bytearray(frame), dtype="uint8")
    image_encode = cv2.imdecode(image, cv2.IMREAD_COLOR)   
    
    q = TargetImage(target_point_x1 = align[0][0], target_point_y1 = align[0][1], target_point_x2 = align[1][0], target_point_y2 = align[1][1])
    q.save()

    image_name = ".jpg"
    image_path = "media/" 
    
    t = TargetImage.objects.last()
    cv2.imwrite(image_path + str(t.id) + image_name, image_encode)
    t.target_image = str(t.id) + image_name
    t.save()

    distance = str(t.id)
    # distance_calculate()
    return HttpResponse(json.dumps({
        "distance": distance,
        }), content_type="application/json")

def distance_calculate():
    ori_frame = stereoCamera.GetBothFrame()
    
    frames.StoreFrame(ori_frame[0],ori_frame[1])
    frames.DetectAndMatch()
    distance_list = frames.CalculateDistance()
    border_points_list = frames.GetBorderPointsList()
    print(distance_list)
    print(border_points_list)
    return

# Load target list table
def target_table_check(request):
    ori_frame = stereoCamera.GetBothFrame()
    
    frames.StoreFrame(ori_frame[0],ori_frame[1])    
    frames.DetectAndMatch()
    distance_list = frames.CalculateDistance()
    border_points_list = frames.GetBorderPointsList()
    target_table = []
    # print(TargetImage.objects.count(),' = ',len(distance_list))
    if TargetImage.objects.all().exists() and TargetImage.objects.count() == len(distance_list):
        target_list = TargetImage.objects.all()
        target_list = list(target_list.values())
        for idx, val in enumerate(border_points_list):            
            target_table_dict = {
                'id': target_list[idx]['id'],
                'distance': distance_list[idx],
                'left_x1': val[0][0][0],
                'left_y1': val[0][0][1],
                'left_x2': val[0][1][0],
                'left_y2': val[0][1][1],
                'right_x1': val[1][0][0],
                'right_y1': val[1][0][1],
                'right_x2': val[1][1][0],
                'right_y2': val[1][1][1],
            }
            target_table.append(target_table_dict)
        # print(target_table)
        # print(distance_list)
        return HttpResponse(json.dumps(target_table), content_type="application/json")   

    else:        
        # print(TargetImage.objects.all())
        # print(distance_list)
        return HttpResponse(json.dumps({"flag":"empty", "text": "Empty table or Please clear the table",}), content_type="application/json")

def target_table_all_clear(request):
    t = TargetImage.objects.all()
    if t.exists():
        t.delete()
    frames.AllDeleteTarget()

    return HttpResponse(json.dumps({"dumy": "dumy",}), content_type="application/json")
