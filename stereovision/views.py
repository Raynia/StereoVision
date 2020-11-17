import cv2
import numpy as np
import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse, JsonResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.conf import settings

from .camera import StereoCamera as sc

from .models import TargetImage, Userdata, CameraList, PreviewCamera

stereoCamera = sc.StereoCamera()

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

    if TargetImage.objects.all().exists():
        target_list = TargetImage.objects.all()

    else:
        target_list = None

    contents = {
        'userdata_list': userdata_list,
        'target_list': target_list,
    }

    stereoCamera.ReleaseOtherCamera(userdata_list.user_left_camera, userdata_list.user_right_camera)

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
    width = request.POST['resolution']
    height = int(width) // 4 * 3
    distance = request.POST['distance']

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
    x1, y1 = request.POST['x1'], request.POST['y1'] # start point
    x2, y2 = request.POST['x2'], request.POST['y2'] # destination point

    lr = 0 if camera_pos == "left" else 1
    frame = stereoCamera.GetLRFrame(lr)   
    
    image = np.asarray(bytearray(frame), dtype="uint8")
    image_encode = cv2.imdecode(image, cv2.IMREAD_COLOR)   
    
    q = TargetImage(target_bytes = frame, target_point_x1 = x1, target_point_y1 = y1, target_point_x2 = x2, target_point_y2 = y2)
    q.save()

    image_name = ".jpg"
    image_path = "media/" 
    
    t = TargetImage.objects.last()
    cv2.imwrite(image_path + str(t.id) + image_name, image_encode)
    t.target_image = str(t.id) + image_name
    t.save()

    distance = str(t.id)

    return HttpResponse(json.dumps({
        "distance": distance
        }), content_type="application/json")
  

# Load target list table
def open_target_list(request):
    return None #return target_list page

# Capture Image
def image_capture(request):
    return HttpResponseRedirect(reverse('stereovision:main'))

# Reverse Camera
def camera_reverse(request):
    return HttpResponseRedirect(reverse('stereovision:main'))


# Function Test View
######################################################################
def left(request):
    return HttpResponse("This is left camera page")

def right(request):
    return HttpResponse("This is right camera page")

def sshot(request):
    return HttpResponse("This is screenshot page")

def userdata_delete(request):
    q = Userdata.objects.first()
    q.delete()
    return HttpResponseRedirect(reverse('stereovision:test_temp'))

