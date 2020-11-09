from django.http.response import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

from .models import CameraInfo, Userdata

# Create your views here.
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
        return HttpResponseRedirect(reverse('stereovision:main'))

def userdata_delete(request):
    q = Userdata.objects.first()
    q.delete()
    return HttpResponseRedirect(reverse('stereovision:main'))

def main(request):
    return render(request, 'stereovision/main.html')

def gen(camera):
    return None       

def video_left(request):
    return StreamingHttpResponse(request)
    
def video_right(request):
    return StreamingHttpResponse(request)
