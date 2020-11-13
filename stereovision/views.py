import threading
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.urls import reverse
from django.views import generic
from .camera import StereoCamera as sc
import cv2 as cv

from .models import CameraInfo, TargetImage, Userdata, CameraList

stereoCamera = sc.StereoCamera()

# Stereovision View
#########################################################################
def init(request):
    init_list = [CameraInfo.objects.all(), Userdata.objects.all(), TargetImage.objects.all(), CameraList.objects.all()]

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

    camera_list = CameraList.objects.all()
    contents = {
        'list' : camera_list,
    }
        
    # stereoCamera.ReleaseOtherCamera(0,1)

    return render(request, 'stereovision/setting.html', contents)
    # return HttpResponseRedirect(reverse('stereovision:setting')) 

def main(request):
    u = Userdata.objects.all()
    if u.exists():
        userdata_list = Userdata.objects.first()    
    else:
        userdata_list = None
    contents = {
        'userdata_list': userdata_list,
    }

    stereoCamera.ReleaseOtherCamera(userdata_list.user_left_camera, userdata_list.user_right_camera)

    return render(request, 'stereovision/main.html', contents)

def setting(request):
    camera_list = CameraList.objects.all()
    camera_list.delete()
    for idx, cam in enumerate(stereoCamera.cam_list):
        q = CameraList(camera_index = idx)
        q.save()
    
    #camera_list = CameraList.objects.all()
    contents = {
        'list' : camera_list,
    }
    return render(request, 'stereovision/setting.html', contents)

def gen(lr):
    while True:
        frame = stereoCamera.GetLRFrame(lr)
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')  

#Streaming left-side video which player choose
def video_left(request):
    try:
        return StreamingHttpResponse(gen(0), content_type='multipart/x-mixed-replace;boundary=frame')
    except:  # This is bad! replace it with proper handling
        pass

#Streaming right-side video which player choose
def video_right(request):
    try:
        return StreamingHttpResponse(gen(1), content_type='multipart/x-mixed-replace;boundary=frame')
    except:  # This is bad! replace it with proper handling
        pass

def userdata_update(request): 
    left_camera = request.POST['left_camera']
    right_camera = request.POST['right_camera']
    width = request.POST['resolution']
    height = int(width) // 4 * 3
    distance = request.POST['distance']

    q = Userdata.objects.all()
    if q.exists():
        q.delete()
    
    d = Userdata(user_left_camera = left_camera, user_right_camera = right_camera, user_width = width, user_height = height, user_distance = distance)
    d.save()
    
    return HttpResponseRedirect(reverse('stereovision:main'))
    
def border_selection(request):
    x1, y1 = request.POST[''], request.POST[''] # start point
    x2, y2 = request.POST[''], request.POST[''] # destination point
    return HttpResponseRedirect(reverse('stereovision:main'))

# Save target image to target list table
def save_target(request):
    return HttpResponseRedirect(reverse('stereovision:main'))

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

