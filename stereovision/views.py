from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.urls import reverse
from django.views import generic
from .camera import VideoCamera

from .models import CameraInfo, Userdata

# Stereovision View
#########################################################################

def gen(camera):    
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')  

def main(request):
    return render(request, 'stereovision/main.html')

#Streaming left-side video which player choose
def video_left(request):
    return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")

#Streaming right-side video which player choose
def video_right(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
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
    user_left = request.POST['left']
    user_right = request.POST['right']
    user_distance = request.POST['distance']
    user_width = request.POST['width']
    user_height = request.POST['height']

    try:        
        q = Userdata(left=user_left, right=user_right, distance=user_distance, user_width=user_width, user_height=user_height)
    except:
        return None
    else:
        q.save()
        return HttpResponseRedirect(reverse('stereovision:test_temp'))

def userdata_delete(request):
    q = Userdata.objects.first()
    q.delete()
    return HttpResponseRedirect(reverse('stereovision:test_temp'))

