import threading
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.urls import reverse
from django.views import generic
#from .camera import VideoCamera
import cv2 as cv

from .models import CameraInfo, Userdata

# Stereovision View
#########################################################################
def main(request):
    return render(request, 'stereovision/main.html')

def setting(request):
    return render(request, 'stereovision/setting.html')

class VideoCamera:
    def __init__(self):
        self.video = cv.VideoCapture(1 + cv.CAP_DSHOW)
        (self.grabbed, self.frame) = self.video.read()        
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        (self.grabbed, self.frame) = self.video.read()
        image = self.frame
        jpeg = cv.imencode('.jpg', image)
        return jpeg[1].tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):    
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')  

#Streaming left-side video which player choose
def video_left(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace;boundary=frame')
    except:  # This is bad! replace it with proper handling
        pass

#Streaming right-side video which player choose
def video_right(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace;boundary=frame')
    except:  # This is bad! replace it with proper handling
        pass

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
def test_temp(request):
    camera_list = CameraInfo.objects.all()
    userdata_list = Userdata.objects.all()
    context = {
        'camera_list': camera_list,
        'userdata_list': userdata_list,
    }
    return render(request, 'stereovision/test_temp.html', context)

def test_main(request):
        return render(request, 'stereovision/test_main.html')   

def left(request):
    return HttpResponse("This is left camera page")

def right(request):
    return HttpResponse("This is right camera page")

def sshot(request):
    return HttpResponse("This is screenshot page")

def userdata_update(request):    
    return HttpResponseRedirect(reverse('stereovision:main'))

def userdata_delete(request):
    q = Userdata.objects.first()
    q.delete()
    return HttpResponseRedirect(reverse('stereovision:test_temp'))

