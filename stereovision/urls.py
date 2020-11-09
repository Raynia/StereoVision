from django.urls import path
from . import views

app_name = 'stereovision'

urlpatterns = [
    path('', views.main, name='main'),    
    path('left/', views.left, name='left'),    
    path('right/', views.right, name='right'),    
    path('sshot/', views.sshot, name='sshot'),
    path('userdata_update/', views.userdata_update, name="userdata_update"),    
    path('userdata_delete/', views.userdata_delete, name="userdata_delete"),   
    path('test/temp/', views.test_temp, name="test"), 
    path('test/main/', views.test_main, name="test"),

    #Streaming Path
    path('video_left', views.video_left, name='video_left'),
    path('video_right', views.video_right, name='video_right'),]
